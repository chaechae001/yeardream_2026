import os

from transformers import pipeline

# window 경고메시지 지우기 (선택사항)
# 윈도우 운영체제에서 허깅페이스 모델을 내 컴퓨터로 다운로드할 때 발생하는 경고메시지를 숨겨줌
os.environ["HF_HUB_DISABLE_SYMLINK_WARNING"] = "1"

# 텍스트 분류
# 숨겨진 작동원리
# 1. 토큰화(Tokenizing)
# 2. 모델추론(Inference)
# 3. 후처리(Post-processing) : 연산결과를 사람이 알아보기 쉽게 POSITIVE/NEGATIVE 라는 라벨과 확률 딕셔너리로 변환
"""
clf = pipeline(task="text-classification")
print(f'model_name : {clf.model.name_or_path}')
print(clf('Hugging Face is Amazing!!'))
"""

# 질의응답
# 모델명을 넣었더니 해당 task가 없다고 한다.
# transformers의 버전을 낮춰주면 가능하다.
# pip install transformers==4.57.6
"""
# 특정 한국어 모델 직접 지정
# monologg : 이 모델을 허깅페이스에 올려둔 개발자 이름
# koelectra-base-v3: 한국어(ko)를 학습한 ELECTRA라는 인공지능 구조의 3번째 버전
qa = pipeline(model = 'monologg/koelectra-base-v3-finetuned-korquad')

result = qa(
    question="대한민국의 수도는 어디입니까?",
    context="대한민국의 수도는 서울입니다."
)
print(result)
"""
# ================================================================
# 이미지 분류 (컴퓨터 비전)
# ================================================================
# 필수 라이브러리 설치 - 이미지 다루기 위해 필요한 도구
# pillow (PIL) : 파이썬에서 이미지를 열고, 자르고, 크기를 조절하는 등 이미지 파일 조작할 때 사용하는 기본 라이브러리
# torchvision : 파이토치 생태계에서 컴퓨터 비전 작업을 돕는 전용 도구 모음, 모델이 이미지를 학습할 수 있도록 변환(Transform)해주는 기능 포함
# uv pip install pillow torchvision

# 모델 이름
# vit (Vision Transformer) : 과거 이미지 분석 CNN(합성곱 신경망) 방식 대신 텍스트를 다루던 Transformer 기술을 이미지에 적용한 구조
# base : 모델의 크기(파라미터 수) 의미 (base < Large < Huge)
# patch16 : 가로세로 16x16 픽셀 크기의 작은 조각(Patch) 들로 쪼개서 순서대로 읽음
# 224 : 학습할 때 가로세로 224x224 픽셀 크기의 이미지를 기준으로 공부
vision = pipeline(model="google/vit-base-patch16-224")
print(vision('dog.png'))

