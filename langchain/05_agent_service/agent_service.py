import logging  # 실행 로그(기록) 관리하는 기본 라이브러리

from langchain.agents import create_agent   # LangChain에서 AI 에이전트를 쉽게 생성해주는 함수 가져옴
from langchain_core.tracers import langchain    # LangChain 내부 동작을 추적하고 디버깅하기 위한 모듈 가져옴
from langchain_ollama import ChatOllama # 내컴퓨터(로컬)에서 실행 중인 Ollama모델과 연동하기 위한 클래스를 가져옴

from tools import check_weather, now_date, check_stock  # 내가 만든 외부 도구 파일에서 함수들을 가져옴

# 파이썬의 기본 로깅(기록) 시스템의 출력 기준을 INFO레벨로 설정
# 프로그램이 실행되면서 '서버가 켜졌다', '어떤 요청이 들어왔다' 같은 중요한 정보성 메시지(INFO)들을 터미널 화면에 출력
# 이보다 더 낮은 단계인 디버그 기록은 숨기고, 주요 흐름만 보여줌
logging.basicConfig(level=logging.INFO)
# 랭체인 라이브러리의 디버그 모드 켬
# AI 에이전트가 작동할 때, "어떤 프롬프트를 주고받았는지", "LLM에게 정확히 어떤 요청을 보냈는 지" 등 전과정을 터미널에 출력
langchain.debug = True

# ollama 모델 생성
llm = ChatOllama(model="gemma4:e4b")

# 도구 등록
tools = [check_stock, check_weather, now_date]

# 시스템 명령
sys_prompt = """
당신은 도구를 사용할수 있는 AI 비서 입니다.
질문에 답하기 위해서 필요하다면 도구를 활용하세요.
[출력규칙]
1. 답변은 오직 한글로 해 주세요.
2. 문장에 '실시간 데이터가 아니다.', 'API가 필요하다.', '가정된 결과다' 같은 불필요한 주의사항(Note)
또는 추가설명은 붙이지 마세요.
3. 도구를 활용한 결과는 오직 결과만 깔끔하게 한국어 문장으로 정리해서 답하세요.
"""

# 에이전트 생성
agent = create_agent(llm, tools=tools, system_prompt=sys_prompt)

# 프롬프트 생성 + 대답 듣기
def start_agent(query:str):
    # stream_mode = "update" <- 주요 과정이 종료될 때마다 출력
    # stream_mode = "messages"  <- 기본(타이핑 하듯이 출력)
    mode = "messages"
    for chunk in agent.stream({"messages" : [("user", query)]}, stream_mode=mode):
        # messages로 처리할 경우 chunk  구조가 달라지므로 해당 내용으로 변경해줘야 함
        if mode == 'updates' and 'model' in chunk:
            message = chunk['model']['messages'][-1].content
            # print(message, end="", flush=True)
            yield message

        if mode == 'messages':
            # print(chunk[0])
            # chunk 객체 안에 tool_calls라는 속성이 있으면,
            # 있으면 AIMessage, 없으면 ToolMessage
            if hasattr(chunk[0],"tool_calls"):
                text = chunk[0].content
                if text != '':
                    yield text