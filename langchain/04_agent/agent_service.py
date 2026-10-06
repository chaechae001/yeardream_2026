import logging
import langchain
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from tools import plus, minus, multiply, divide

# 추론 과정을 확인하기 위한 로그 설정
logging.basicConfig(level=logging.INFO)
langchain.debug = True


# 모델 불러오기
# ollama run gemma4:e4b
model_id = "gemma4:e4b"
model = ChatOllama(model=model_id, temperature=0)

# 도구 등록
# 등록인 경우 plus / plus()처럼 ()가 있으면 즉시 실행되니, ()지우기
tools = [plus, minus, multiply, divide]

# 에이전트 생성
agent = create_agent(model=model, tools=tools)

# 프롬프트 제작
# 3+3은?
# a=5, b=10일 경우 a+b
msg = input('사칙 연산을 해보세요')
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 사칙연산 전문가입니다. 값 a와  값 b, 연산자가 주어지면 연산 후 답을 반환하는 작업을 수행하세요."),
    ("user", "{message}")
])

def calc_tool(msg):
    chain = prompt|agent # 파이프라인 조합
    resp = chain.invoke({"message",msg}) # 실행
    print('---AI의 생각 과정 및 도구 실행 모니터링---')
    for i,message in enumerate(resp['messages']):
        print(f'[STEP{i}]     {message}')

    return resp['messages'][-1].content