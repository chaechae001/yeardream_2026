from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama

# 모델 호출
model = ChatOllama(model = "exaone3.5:2.4b")

# 대화 저장 리스트
conversation_history = []

# 프롬프트 작성
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 답변 전문 AI 모델입니다. 주워진 질문에 대해서 핵심만 간단히 대답하세요."),
    MessagesPlaceholder(variable_name="history"),   # 대화내용을 history라는 이름으로 줄게. 참고해서 대답해봐
    ("user", "{query}")
])

# 파이프라인 조립
chain = prompt | model

# 실행 및 출력
while True:
    query = input('\n 당산')

    if query == '/exit' or query == '/bye':
        print('대화를 종료합니다.')
        break
    answer = ''
    for chunk in chain.stream({'query': query, 'history': conversation_history}):
        print(chunk.content, end="", flush=True) # StrOutputParser() 안써서 .content 붙임
        answer += chunk.content

    conversation_history.append(HumanMessage(content=query))
    conversation_history.append(AIMessage(content=answer))
    print()
    print(f'\n [history length] : {len(conversation_history)}')