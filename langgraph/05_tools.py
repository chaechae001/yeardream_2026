from typing import TypedDict, Annotated, Dict

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.constants import END
from langgraph.graph import add_messages, StateGraph

# 1. 상태 저장소 생성
# class를 Dictionary처럼 여기게 해줌
class AgentState(TypedDict):
    # Langgraph에서는 상태를 덮어쓰는 것을 원칙으로 하고 있음
    # Annotated[데이터타입, 규칙] 을 통해서 규칙을 변경하고자 함
    # Annotation(@) : 컴파일러에게 미리 힌트를 주는 개념 (참고, 규칙)
    # 즉 overwrite가 아닌 add message를 하도록 함
    # BaseMessage 객체가 담기는 리스트, 데이터가 들어올 때 add_messages 함수를 적용
    messages:Annotated[list[BaseMessage], add_messages]

# 2. 모델 생성
llm = ChatOllama(model="gemma4:e4b", temperature=0)

# 3. 툴 생성
@tool
def multiply(a:int, b:int) -> int:
    """
    두 정수를 곱하는 계산기 도구 입니다. 곱셈이 필요할 때문 이 도구를 사용 하세요.

    Args:
        a:첫번째 정수
        b:두번째 정수
    """
    print(f'{a}*{b} 를 구하는 도구 실행')
    return a * b

# 4. 툴 등록
tools = [multiply]
model = llm.bind_tools(tools)

# 5. 노드 및 라우트함수 선언
def agent_node(state:AgentState) -> Dict:
    """사용자의 질문을 받아 응답하는 노드"""
    print('사용자 메시지를 받아서 분석중...')
    resp = model.invoke(state['messages'])
    print(f"[AGENT NODE]    {resp}")
    return {'messages':[resp]}

def tool_node(state:AgentState) -> Dict:
    """LLM 의 요청에 따라서 필요한 툴을 실행하는 노드"""
    # 메시지들 중에서 직전의(마지막) 메시지인 AIMessage 를 가져온다.
    last_msg = state['messages'][-1]

    for call in last_msg.tool_calls:
        name = call['name']
        args = call['args']
        call_id = call['id']
        print(f'id : {call_id} 실행!!')
        print(f'{name}({args})')

    return {'messages':[]}


# 6. 저장소 및 노드 등록
wf = StateGraph(AgentState)
wf.add_node("agent",agent_node)
wf.add_node("tool",tool_node)

# 7. 엣지 조립
wf.set_entry_point("agent")
wf.add_edge("agent","tool")
wf.add_edge("tool",END)
app = wf.compile()# 8. 컴파일
# 9. 실행
resp = app.invoke({'messages':[HumanMessage(content="256 곱하기 4가 무엇인지 계산해 주세요")]})
"""
HumanMessage    : 사용자가 보내는 메시지(content)
AIMessage       : LLM 모델이 생성한 메시지(content,tool_calls)
ToolMessage     : Tool 이 수행후 반환하는 메시지(content,tool_call_id)
"""
print(f'최종 : {resp}')