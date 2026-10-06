from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama

# 로컬 LLM(Ollama) 모델 객체 생성
model = ChatOllama(model = "exaone3.5:2.4b")

# 대화 저장 리스트
# 서버가 켜져있는 동안 이전 대화 내용을 기억하기 위한 리스트
conversation_history = []

# 프롬프트 템플릿 작성
prompt = ChatPromptTemplate.from_messages([
    ("system","당신은 답변 전문 AI 모델 입니다. 주워진 질문에 대해서 핵심만 간단히 대답하세요"),
    MessagesPlaceholder(variable_name="history"), # 대화내용을 history 라는 이름으로 줄께
    ("user","{query}")
])

# 파이프라인 조립
chain = prompt|model 

# 실행 및 출력
def get_answer(info:Dict[str, str]):
    # 클라이언트로부터 {"q": "질문내용"} 형태의 JSON을 받음
    # output_str 제너레이터를 StreamingResponse로 감싸서 클라이언트에게 실시간으로 쏴줌
    return StreamingResponse(output_str(info['q']),media_type="text/plain")

# 6. 텍스트 스트리밍 및 메모리 저장 함수 (제너레이터)
def chat_answer(query:str):
    answer = ''
    for chunk in chain.stream({'query':query,'history':conversation_history}):
        # print(chunk.content,end='', flush=True) # StrOutputParser() 안써서 .content 붙이는 것
        answer += chunk.content
        yield chunk.content

    conversation_history.append(HumanMessage(content=query))
    conversation_history.append(AIMessage(content=answer))
    print(f'history length : {len(conversation_history)}')