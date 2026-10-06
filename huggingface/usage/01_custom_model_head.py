import os
# 윈도우 심볼릭 링크 경고 메시지 숨기기
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
"""
    사전학습모델은 본체(Backbone)와 헤드(Head)로 구분된다.
    - Backbone (몸통): 문장을 읽고 문맥적 의미를 파악해 768개의 숫자(임베딩 벡터)로 요약하는 역할
    - Head (머리): 몸통이 만든 요약본을 넘겨받아 우리가 원하는 최종 정답(긍정/부정)으로 결론 내리는 역할
"""
import torch
from torch import nn, no_grad
from transformers import PreTrainedModel, AutoModel, AutoTokenizer, AutoConfig


# === 1단계: 커스텀 모델 클래스 정의 ===
# 허깅페이스가 제공하는 PreTrainedModel이라는 기본 클래스를 물려받기(상속)
# why? 뼈대를 물려받으면 모델 저장이나 불러오는 등 허깅페이스의 편리한 기본 기능들을 그대로 사용 가능하기 때문
class CustomClassifier(PreTrainedModel):
    def __init__(self, config):  # 생성자 (클래스가 객체화 될 때 가장먼저 실행)
        super().__init__(config)  # 부모 초기화를 위해 전달

        # 2. 베이스 모델(몸통) 불러오기
        # 문장의 의미를 깊이있게 파악하는 똑똑한 '몸통'역할을 할 기본 모델을 뼈대 위에 얹는 과정
        # (1) backbone 생성
        # config가 뭐죠 ?? -> config.json (모델 설계도)
        self.backbone = AutoModel.from_config(config)

        # backbone이 출력하는 벡터 차원 알아내기
        hidden_size = config.hidden_size   # 768 차원

        # (2) 커스텀 헤드 만들기 - 받아온 벡터들을 원하는 결과로 추출
        # 영화 리뷰를 가지고 긍정/부정 등을 구분하는 것을 할 예정
        self.custom_head = nn.Sequential(
            nn.Linear(hidden_size, hidden_size//2),  # 768 -> 384
            nn.ReLU(),  # 활성함수 (for 복잡한 패턴 학습)
            nn.Dropout(0.3),  # 훈련 중 30%의 신경망 무작위로 끔 (for 과적합 방지)
            nn.Linear(hidden_size//2, 2)  # 384 -> 2로 최종 출력 (긍정, 부정)
        )
        self.post_init()  # 가중치 초기화

    # model() 하면 forward()가 실행된다.
    def forward(self, input_ids, attention_mask=None):
        # 1. 입력받은 텍스트 숫자 배열을 backbone에 넣어서 결과를 받는다.
        outputs = self.backbone(input_ids=input_ids, attention_mask=attention_mask)
        print(f'outputs shape : {outputs.last_hidden_state.shape}')  # [문장수, 토큰수, 벡터수]
        # outputs.last_hidden_state는 [문장수, 토큰수, 768] 형태의 모든 단어별 의미표를 담고 있음
        # 우리는 문장 전체의 의미가 필요하므로 첫 번째 단어인 [CLS] 토큰의 768개 숫자만 가져옴

        # [CLS] - 시작토큰 (해당 문장에 대표되는 내용을 담고 있다)
        cls_vec = outputs.last_hidden_state[:, 0, :]
        print(f'[CLS] vector : {cls_vec}')

        # [CLS] 요약본을 우리가 만든 커스텀 머리에 넣고 최종 점수(Logits)를 반환
        # 2. 커스텀헤드에 보내서 최종 결과값을 받아낸다.
        # 3. 결과값 반환
        return self.custom_head(cls_vec)

# === 2단계: 토크나이저와 모델 준비 ===
model_id = "distilbert-base-uncased"  # 가볍고 빠른 영어 모델
tokenizer = AutoTokenizer.from_pretrained(model_id)  # 글자를 숫자로 바꿀 토크나이저 준비
# 해당 모델의 설계도 불러옴
config = AutoConfig.from_pretrained(model_id)  # 해당 모델의 뼈대 설계도 다운로드
model = CustomClassifier(config)  # 해당 설계도 전달


# === 3단계: 동작 확인 및 추론(Inference) ===
sentences = [
    "I really loved this movie, it was fantastic!",
    "This was a waste of time, I hated it.",
]

# 1. 텍스트를 숫자로 변환 (전처리)
# 빈칸은 채우고(padding) 긴 건 자름(truncation)
inputs = tokenizer(sentences, padding=True, truncation=True, max_length=128, return_tensors="pt")
print(inputs)

# 2. 검증(평가) 모드로 변경
# 훈련용으로 넣어둔 Dropout 기능 등을 끄고 실전 모드 돌입
model.eval()  # 학습 과정은 필요없이 추론 결과만 보고자 할 때

# 3. 기울기 계산 비활성화 (추론 모드)
# 역전파(기울기 계산)용 메모리 저장을 차단해 추론 속도를 높임
with no_grad():
    # 3. 모델에 데이터 넣고 순수 원시형태의 출력 점수 결과(Logit) 받기
    logit = model(inputs['input_ids'], inputs['attention_mask'])

print(f'model 출력 : {logit}')
"""
출력 예시:
[-0.2721, -0.1642] -> 첫 번째 문장의 [부정 점수, 긍정 점수]
[-0.2169, -0.1564] -> 두 번째 문장의 [부정 점수, 긍정 점수]
* 주의: 아직 훈련(파인튜닝)을 안 한 백지상태라 점수가 무작위로 나옴.
"""

# 4. 후처리: 사람이 이해하기 쉽게 0~1 사이의 확률로 변환
# dim=1|-1 : 가로방향으로 연산
# dim=0 : 세로방향으로 연산
# dim=-1 의 의미: "데이터 구조가 어떻든, 가장 마지막 차원(끝 축)을 기준으로 계산해라!"
# 여기서는 마지막 축이 [부정, 긍정] 2개이므로, 이 두 숫자의 합이 1(100%)이 되도록 비율을 조정해줌
prob = torch.softmax(logit, dim=-1)
print(f'최종 확률 : {prob}')
# prob 출력 예시: [0.5308, 0.4692] -> 부정일 확률 53%, 긍정일 확률 46%

# 5. argmax 함수로 확률이 더 큰 쪽의 인덱스(0번이냐 1번이냐)를 찾아냄.
# dim=-1 을 썼으므로 가장 마지막 차원([부정, 긍정]) 중에서 더 큰 값의 '순번'을 뽑아줌
pred = torch.argmax(prob, dim=-1)
print(f"예측 결과 (0:NEG / 1:POS : {pred}")

# 모델과 토크나이저 저장: 커스텀 모델의 구조, 설정, 가중치를 로컬 폴더에 영구 저장
save_path = './my_custom_model'
model.save_pretrained(save_path)
tokenizer.save_pretrained(save_path)
