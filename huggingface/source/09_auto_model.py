import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

os.environ["HF_HUB_DISABLE_SYMLINK_WARNING"] = "1"
model_id = "distilbert-base-uncased-finetuned-sst-2-english"

# 1. 토크나이저 생성
tokenizer = AutoTokenizer.from_pretrained(model_id)

# 2. 모델 생성
model = AutoModelForSequenceClassification.from_pretrained(model_id, dtype=torch.float16)

# 3. 전처리 (토크나이징 -> tensor([])형태로 바꿔줌)
# pt : 파이토치 호환 텐서형태
inputs = tokenizer("Today is a good day!!", return_tensors="pt")
print(f'inputs: {inputs}')

# 4. 모델 추론 (추론에서는 경사하강 알고리즘을 사용 안함)
# 블록 안에서 실행되어, 역전파와 경사하강법 연산에 필요한 메모리 저장을 차단하고 오직 추론 속도만 극대화
with torch.no_grad():
    # inputs는 딕셔너리 형태라 **inputs
    # 딕셔너리 형태의 입력값을 압축 해제하여 모델에 전달
    outputs = model(**inputs)

print(f'outputs: {outputs}')
# logits = 반환된 순수 숫자

# 5. 후처리 (사람이 이해할 수 있는 문자화)
# 모델이 뱉어낸 순수 숫자(Logits)를 0과 1 사이의 확률 값으로 변환하여 최종 출력
# dim=-1 : 다차원 데이터(텐서)에서 '가장 마지막 차원'을 기준으로 연산 수행
# outputs.logits의 구조 : 모델이 텍스트를 분석하면 보통 2차원 표(Tensor)로 결과 점수 반환
# [배치크기, 클래스 개수(ex. 부정/긍정 2개)] 형태
prob = torch.softmax(outputs.logits, dim=-1).tolist()
print(f'probability : {prob[0]}')
print(f'POSITIVE : {prob[0][1] * 100:.2f}%')    # prob[0] 첫번째 문장의 결과 배열에서 두번째 값인 긍정확률
print(f'NEGATIVE : {prob[0][0] * 100:.2f}%')    # prob[0] 첫번째 문장의 결과 배열에서 첫번째 값인 부정확률

# :.2f 의미
# :이 붙는 이유 => 파이썬의 f-string 안에서 변수 출력할 때, 변수 이름 뒤에 서식(포맷)규칙을 지정하기 위해
# {변수이름:서식지정자}
# : 뒤에는 그 숫자를 어떻게 꾸며서 보여줄 지 규칙을 적음
# {prob[0][1] * 100:.2f}
# 계산된 숫자에 콜론(:) 뒤의 규칙(.2f, 소수점 둘째자리까지 표시)을 적용해서 출력