# uv pip install diffusers transformers accelerate torch
# pip uninstall -y diffusers transformers huggingface-hub
# uv pip install --no-cache-dir -U huggingface-hub transformers diffusers
# pip install -U accelerate safetensors

# 허깅페이스의 Diffusers 라이브러리를 활용해 텍스트 입력만으로 고품질 이미지 생성
from diffusers import StableDiffusionPipeline
import torch

model_id = "sd-legacy/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    dtype=torch.float32, # float16으로 안되면 float32로 다시해보기
    safety_checker=None #NSFW 필터 제거 (유해 콘텐츠나 부적절한 표현 걸러내는 필터)
)
pipe = pipe.to("cuda")

prompt = "a photo of an astronaut riding a horse on mars"
image = pipe(prompt).images[0]

image.save("img.png")
