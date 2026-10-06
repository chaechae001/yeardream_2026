import time
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = 'Qwen/Qwen2.5-1.5B-Instruct'

tokenizer = AutoTokenizer.from_pretrained(model_id)

# 성능을 비교하기 위해 긴 테스트용 문장 반복해서 만들기
text = "SDPA 와 EAGER 중에 누가 더 빠른가? 확인해 봅시다." * 30
inputs = tokenizer(text,return_tensors="pt").to("cuda") # mps
print(f'입력 토큰 수 : {inputs['input_ids'].shape[1]}개')

# 벤치마크 측정 함수
def benchmark(attn_type,name):
    print(f'=== [{name}] 측정 시작 ===')
    # 모델 불러오기
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        dtype=torch.float16,
        low_cpu_mem_usage=True, # cpu, mem 절약
        attn_implementation=attn_type,
        device_map="auto"
    )

    # 실행
    start_time = time.time()
    with torch.no_grad():
        model(inputs['input_ids'])

    # CPU 가 GPU 작업 종료까지 기다리도록 동기화 시켜 준다.
    # GPU는 CPU와 별개로 비동기(병렬)로 작업을 처리하는 특성
    torch.cuda.synchronize()
    # torch.mps.synchronize()
    end_time = time.time() - start_time
    print(f'=== [{name}] 이 걸린시간 : {end_time} ===')

# 실행 및 결과 비교
# SDPA(Flash Attention) 방식이 EAGER 방식보다 더 빠르게 동작
benchmark('sdpa',"Flash Attention 방식(SDPA)") # 4.4578468799591064
# benchmark('eager',"Standard Attention 방식(EAGER)") # 4.561115264892578