import torch
from transformers import AutoTokenizer, AutoModel

# 한국어(KLUE) 자연어 이해 성능이 뛰어난 대표적인 양방향 인코더 모델 (BERT)
# 주로 문맥 파악하거나 텍스트 분류, 마스크드 언어 모델링 등의 작업에 쓰임
model_id = "klue/bert-base" # task=fill-mask

# 1. 토크나이저 불러오기
tokenizer = AutoTokenizer.from_pretrained(model_id)

# 2. 모델 불러오기
model = AutoModel.from_pretrained(model_id)

# 3. 토큰화
text = "파이썬이라는 언어는 참 재미있습니다."
inputs = tokenizer(text, return_tensors="pt")
print(f'token화된 tensor : {inputs}')

# 4. 모델 추론
with torch.no_grad():
    # output_hidden_States = True로 하면, 모든 레이어의 hidden state를 받는다.
    # 모델 내부의 모든 트랜스포머 레이어가 거쳐 간 모든 중간 은닉상태를 전부 저장할 지 여부
    # False로 지정했기 때문에 가장 마지막 레이어의 최종 결과(last_hidden_state)와
    # 문장 전체를 대표하는 요약 벡터(pooler_out)만 받아옴
    outputs = model(**inputs, output_hidden_states=False)

# last_hidden_state
lhs = outputs.last_hidden_state
print(f'last_hidden_state shape : {lhs.shape}') # [1, 13, 768]
# 1
# : 배치크기 (한 번에 처리한 문장의 개수)
# 문장 1개를 넣어서 1이됨
# 13
# : 시퀀스 길이 (입력한 문장이 토크나이저에 의해 쪼개진 총 토큰의 개수)
# special token을 포함한 토큰의 수
# 특수토큰(문장 시작[CLS], 문장 끝[SEP])이 모두 포함되어 총 13개의 토큰으로 변환
# 768 : BERT 모델의 표현 차원
# 모델이 단어 하나의 의미를 768개의 숫자로 이루어진 벡터로 표현했다는 의미

# => 문장 1개 안에 총 13개의 토큰이 들어있고, 각각의 토큰은 768개의 숫자로 된 의미 표를 가지고 있다.

# 5. 활용 예시 - 특정 단어의 벡터 가져오기
# 토크나이징된 결과물(inputs) 중 모델에 입력되는 정수 ID 모음인 input_ids를 가져옴
# convert_ids_to_tokens() 함수 : 반대로 숫자 ID 배열을 다시 사람이 읽을 수 있는 토큰 형태로 되돌려주는 역변환 메서드
print(inputs['input_ids'][0])
tokens = tokenizer.convert_ids_to_tokens(inputs['input_ids'][0])
print(tokens)

# 토큰별로 768차원의 벡터를 가져와보기 (앞 3차원만..)