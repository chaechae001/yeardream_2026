# 인공지능 모델의 예측 결과가 얼마나 정확한지 (정확도) 채점

# uv pip install evaluate scikit-learn
import evaluate

# 1. 평가지표 로딩
# 여러 평가지표 중에서 가장 기본이 되는 '정확도' 채점관 불러오기
acc = evaluate.load('accuracy')

# 2. 예측값과 정답을 주고 결과 계산
# 모델의 예측값과 실제 정답을 비교하여 점수 산출
result = acc.compute(
    predictions=[0,1,1,0], # 인공지능 모델이 예측한 결과 값들의 목록
    references = [0,1,0,0]  # 데이터가 가진 실제 정답 목록
)
# 총 4개의 샘플 중 0, 1, 3번째 값은 맞췄고, 2번째 값은 틀렸으므로 정확도는 75%
# {'accuracy': 0.75} 형태의 딕셔너리 구조로 결과가 반환
print(result)