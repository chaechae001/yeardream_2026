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
    outputs = model(**inputs)

pooler = outputs.pooler_output

print(pooler.shape)  # torch.Size([1, 768])[문장, 벡터]
print('=== pooler는 문장 전체의 벡터를 갖는다. ===')
print(f'pooler vector : {pooler[0, :5].tolist()}')