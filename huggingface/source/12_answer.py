import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer

model_id = 'Qwen/Qwen2.5-1.5B-Instruct'

# 1. 토크나이저
tokenizer = AutoTokenizer.from_pretrained(model_id)
# 2. 모델
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    trust_remote_code=True,
    # dtype=torch.bfloat16 <- 메모리 절약 및 안정성 확보 (GPU에서 지원되어야 함)
    dtype=torch.float16,
    # attn_implementation="flash_attention_2",  # "eager", "sdpa"
    device_map='auto'
)

prompt = input('AI에게 질문하고 싶은 내용은?\n')
print(prompt)

# 3. 토큰화
message = [
    {"role":"system", "content":"너는 IT 전문가야, AI 지식을 주로 다루고 있으며, 알기 쉽게 예를 들어서 설명해주는 것을 잘해"},
    {"role":"user", "content": prompt}
]

chat = tokenizer.apply_chat_template(
    message,
    tokenize = False,
    add_generation_prompt=True

)
print(chat)

# to() : 무엇을 이용해서 토큰화 할거야.
# 생성된 입력 데이터 텐서를 모델이 올라와있는 동안 동일 하드웨어 장치(GPU 등)로 이동시킴
inputs = tokenizer(chat, return_tensors="pt").to(model.device)
print('생각하는 중...')

# 4. 추론
# 추론모델에서는 경사하강 알고리즘 사용하지 않음
# with torch.no_grad():
#     outputs = model.generate(
#         **inputs,
#         max_new_tokens=1024,
#         do_sample=True,
#         temperature=0.7,
#         eos_token_id=tokenizer.eos_token_id   # 문장이 끝났음을 알리는 종료 토큰 지정 역할
#     )
#     # 모델이 뱉어낸 복잡한 숫자(토큰ID) 배열 -> 자연스러운 문자열 텍스트로 되돌려 출력
#     print(tokenizer.decode(outputs[0]))

# 실시간 출력을 위해서는 Streamer가 필요하다
# 모델이 텍스트를 한 글자씩 생성할 때마다 기다리지 않고 즉시 창에 출력해줌
# skip_prompt : 내가 했던 질문은 빼고 ai 답변만 스트리밍 되게 해줌
streamer = TextStreamer(tokenizer, skip_propmt=True)

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=1024,
        do_sample=True,
        temperature=0.7,
        eos_token_id=tokenizer.eos_token_id,
        streamer = streamer # 모델이 답변을 만들어내는 과정 자첵 실시간으로 눈에 보이게 연결
    )
    # 스트리머 사용 시 model.generate()안에서 실시간 출력하므로
    # 아래는 주석 처리 또는 삭제해야함 -> 안그러면 결과가 중복처럼 보이게 됨
    # print(tokenizer.decode(outputs[0]))