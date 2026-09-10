from typing import Dict

from fastapi import APIRouter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from starlette.responses import StreamingResponse

## 라우터 설정
router = APIRouter(prefix="/ask", tags=["ask"])

# 1. 모델 만들기
model = ChatOllama(model="exaone3.5:2.4b")

# 2. 템플릿 만들기
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 어려운 기술을 알기쉽게 설명해주는 전문가입니다."),
    ("user", "{topic}에 대해서 설명해주세요.")
])

# q = input("질문 내용을 입력하세요: \n")

@router.post("/stream")
def get_answer(info:Dict[str, str]):
    # 사용자에게 보내기
    # content 부분은 지속적으로 데이터를 줘야한다.
    # return은 여러번 할 수 없다.
    # StreamingResponse 안에서 지속적으로 실행하며 데이터를 줄 함수가 필요하다. -> def output_str
    return StreamingResponse(output_str(info['q']), media_type="text/plain")

def output_str(q):
    chain = prompt | model | StrOutputParser()
    # topic이라는 이름으로 q에 있는 내용이 들어감
    # 실시간 -> for문을 통해 하나씩 받기
    for chunk in chain.stream({"topic": q}):
        # 한줄한줄 나오는 걸방지하고, 한번에 답변
        # print(chunk, end='', flush=True)
        # return은 한번 밖에 못던져줘서 yield 사용
        yield chunk    # return 후 완전히 종료된 게 아니면 대기한다.