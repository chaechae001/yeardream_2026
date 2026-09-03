import os

from transformers import pipeline

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

model_id = "Bllossom/llama-3.2-Korean-Bllossom-3B"

# pip install accelerate
# 사용이유 : GPU 때문

pipe = pipeline(task="text-generation", model=model_id, device_map="auto")

q = input("아무거나 질문하세요!\n")

# 새롭게 만들어낼 답변길이 최대 1024단어(토큰)
# 창의성 스위치 키기
# 답변의 무작위성 조절
# 무작위성 허용하되, 누적 확률이 상위 90% 안에 드는 후보군 안에서 고르기
result = pipe(q, max_new_tokens = 1024, do_sample=True, temperature=0.7, top_p=0.9)
print(result[0]['generated_text'])

