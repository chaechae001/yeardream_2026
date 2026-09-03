import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "google/gemma-2b-it"

# ==================================================================
# 토크나이저 생성
# ==================================================================
# google/gemma-2b-it 모델 전용 토크나이저 객체 가져옴
tokenizer = AutoTokenizer.from_pretrained(model_id)

# ==================================================================
# 대화 내용을 정의
# ==================================================================
# role과 content 키를 가진 딕셔너리 구조의 리스트
msg_list = [
    {"role": "user", "content":"파이썬에서 변수가 뭐야?"},
    {"role": "assistant", "content":"변수는 데이터를 저장하는 상자와 같습니다."},
    {"role": "user", "content":"그럼 리스트는 뭐야?"}
]

# ==================================================================
# 채팅 템플릿 적용 (apply_chat_template)
# ==================================================================
# 정의된 대화 리스트를 해당모델(Gemma)이 학습할 때 사용했던 고유의 대화 포맷 문자열로 자동 변환
prompt = tokenizer.apply_chat_template(
    msg_list,
    # 토큰 ID로 바로 바꾸지 않고, 모델이 인식할 수 있는 구분자가 포함된 텍스트 문자열 형태로 반환
    tokenize = False, # False: 토큰화된 내용을 문자열로 반환
    add_generation_prompt = True,  # True : msg_list 이후 assistant가 이어 쓸 수 있을 지 여부
)

# print(f'모델에 입력될 최종 텍스트 포맷: {prompt}')

# ==================================================================
# 모델 입력용 텐서 변환 (tokenizer)
# 문자열화된 토큰을 숫자(ids)로 변환
# ==================================================================
# Pytorch 텐서 형식으로 만들고, .to("cuda")를 붙여 GPU 연산이 가능하도록 장치에 올림
inputs = tokenizer(prompt, return_tensors = "pt").to("cuda")
print(f'{prompt} \n\n {inputs}')


# ==================================================================
# 1. 모델 호출 (AutoModelForCausalLM.from_pretrained)
# ==================================================================
# gemma는 멀티모달이라 AutoModelForCausalLM 사용 가능 (사전 학습된 언어모델을 불러옴)
# 이 메서드는 내부적으로 config.json을 읽어 모델 아키텍처 구조를 먼저 생성한뒤,
# 가중치 파일(.safetensors, ,bin)을 로드하여 파라미터를 채워넣음
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    # 모델의 가중치를 32비트 부동소수점 데이터 타입으로 불러옴
    dtype = torch.float32,
    # 시스템 하드웨어(GPU, CPU 메모리 등)를 자동 분석하여, 가용한 장치에 모델 파라미터를 최적화해 분산 로드해주는 옵션
    device_map="auto"
)

# ==================================================================
# 2. 답변을 생성 (model.generate)
# ==================================================================
# model.generate() 함수는 텍스트 입력(토큰)을 받아 다음 텍스트를 추론하고 생성
# generate, streamlit 방식이 있음 / generate (한번에 답변)

# pip install accelerate
with torch.no_grad():
    outputs = model.generate(
        # inputs는 딕셔너리 형태여서 ** (cf. *는 튜플)
        # 토크나이저를 통해 만든 딕셔너리 데이터를 압축 해제(**)하여 전달
        # 여기에 실제 단어 ID인 input_ids와 길이가 다른 문장들의 길이를 맞추기 위해 패딩 ([PAD])된 위치를
        # 연산에서 제외하도록 알려주는 attention_mask등이 포함되어 있음
        **inputs,
        max_new_tokens = 256,   # 생성할 최대 토큰 수
        temperature = 0.7,  # 창의성 (0~1), 0: 있는 그대로 / 1: 창의적
        do_sample = True    # 항상 가장 확률이 높은 단어만 뻔하게 고르는 것 (Greedy Search)을 방지
    )

print(outputs[0])
resp_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
# 현재 resp_text는 질문내용 + 답변의 형태이다.
# 답변만 출력하고 싶다면 outputs[0][입력내용 제외한 나머지] 형태로 해야한다.
print(resp_text)





