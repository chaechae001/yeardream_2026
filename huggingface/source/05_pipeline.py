"""
전처리    : 사람의 글자를 컴퓨터가 인식하기 좋게 쪼개고 숫자화 시키는 과정 (tokenizing)
모델 추론  : 이 숫자들(ids)을 딥러닝 모델에 넣어서 계산
후처리    : 모델로부터 받아온 숫자를 사람이 알 수 있는 문자로 변환하는 과정
"""
# pipeline 함수는 [텍스트 -> 토큰화 -> 모델 연산 -> 정답 라벨 변환] 과정을 하나로 묶어줌
from transformers import pipeline

# 1. task와 model 명을 입력해서 원하는 모델 불러오기
# task만 입력해도 관련된 모델을 자동으로 불러온다.
# 특정 모델의 이름을 명시하지 않으면, 허깅페이스가 해당 작업에 널리 쓰이는 기본모델과 토크나이저를 알아서 다운로드하여 메모리에 올려줌
model = pipeline(task="text-classification")

# 2-1. 불러온 모델 이름 확인
# 내가 직접 모델을 고르지 않아서 어떤 모델을 가져왔는 지 확인해보는 과정
model_name = model.model.name_or_path
print(f'사용되는 기본 모델 이름: {model_name}')

# 2-2. 모델의 타입 정보 확인
print(f'모델 클래스 타입 : {type(model.model)}')

# 3. 모델 추론 후 결과 받기
# 가져온 모델 객체에 분석하고 싶은 문장을 텍스트 그대로 넣음
# 기몬 모델이 영어로 학습되어 있어서 한국어 문장에 대해 엉뚱한 결과가 나올 수 있음
# result = model("오늘 hugging face를 공부하는 둘째 날인데, 신기하다.")
result = model("I learned a hugging face.")

# 4. 디코딩 필요없이 출력
print(result)

