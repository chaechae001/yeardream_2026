# uv pip install ollama
# Ollama 라이브러리에서 AI와 대화를 주고받을 수 있게 해주는 핵심기능인 chat함수 불러옴
from ollama import chat

text = input('ollama와 대화해 보세요!\n')

# 한 번에 답변 받기
def chat_generate(input):
    print(f'입력 내용 : {input}')
    print('생각중...')
    resp = chat(
        model="exaone3.5:2.4b",
        messages=[{"role":"user", "content":input}]
    )
    print(resp.message.content)

# chat_generate(text)

# 실시간 답변 받기
def chat_stream(input):
    print(f'입력 내용 : {input}')
    print('생각중...')
    resp = chat(
        model="exaone3.5:2.4b",
        messages=[{"role": "user", "content": input}],
        stream = True
    )

    # 데이터가 조각(chunk)으로 올 때 마다 실시간으로 출력
    for chunk in resp:
        # end=''가 없으면 한글자가 찍힐 때마다 줄바꿈이 된다.
        # flush=True : 화면에 버퍼링 없이 즉시 출력되도록 설정하여 타자치는 듯한 효과
        print(chunk.message.content, end='', flush=True)

chat_stream(text)