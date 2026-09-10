from typing import Dict

from fastapi import APIRouter
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from starlette.responses import StreamingResponse

# 1. 라우터 설정 (URL 접두사를 /ask로 지정)
router = APIRouter(prefix="/ask", tags=["ask"])

# 2. 로컬 LLM(Ollama) 모델 객체 생성
model = ChatOllama(model = "exaone3.5:2.4b")

# 3. 대화 저장 리스트
# 서버가 켜져있는 동안 이전 대화 내용을 기억하기 위한 리스트
conversation_history = []

# 4. 프롬프트 템플릿 작성
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 답변 전문 AI 모델입니다. 주워진 질문에 대해서 핵심만 간단히 대답하세요."),
    MessagesPlaceholder(variable_name="history"),   # 이전 대화 기록이 이곳에 통째로 삽입
    ("user", "{query}") # 사용자의 현재 질문 들어감
])

# 5. 채팅 API 엔드포인트
@router.post("/chat")
def get_answer(info:Dict[str, str]):
    # 클라이언트로부터 {"q": "질문내용"} 형태의 JSON을 받음
    # output_str 제너레이터를 StreamingResponse로 감싸서 클라이언트에게 실시간으로 쏴줌
    return StreamingResponse(output_str(info['q']),media_type="text/plain")

# 6. 텍스트 스트리밍 및 메모리 저장 함수 (제너레이터)
def output_str(query: str):
    # LangChan LCEL 문법 : 프롬프트와 모델을 연결
    chain = prompt | model
    answer = ''

    # 실행 및 출력
    # 체인을 스트리밍 모드(stream)로 실행 -> 토큰이 생성될 때마다 하나씩 받아옴
    for chunk in chain.stream({'query': query, 'history': conversation_history}):
        # yield를 사용해 FastAI가 토큰을 클라이언트에게 즉시 보냄
        yield chunk.content
        # 서버 콘솔 창에도 실시간으로 출력해서 확인
        # print(chunk.content, end="", flush=True) # StrOutputParser() 안써서 .content 붙임
        answer += chunk.content  # 완성된 전체 답변을 저장하기 위해 토큰을 누적

    # 7. 대화가 완전히 끝난 후 히스토리에 기록
    conversation_history.append(HumanMessage(content=query))
    conversation_history.append(AIMessage(content=answer))
    print(f'\n [history length] : {len(conversation_history)}')