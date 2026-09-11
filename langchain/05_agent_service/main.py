# 웹/인터페이스 레이어
# AI가 어떻게 생각하고 동작하는 지 전혀 알 필요가 없고, 오직 "요청을 받아 agent_service에 넘겨주고 응답을 돌려주는 통로"
from fastapi import FastAPI
from starlette.responses import RedirectResponse, StreamingResponse
from starlette.staticfiles import StaticFiles

from agent_service import start_agent
from chat_model import ChatModel

app = FastAPI()
app.mount("/view", StaticFiles(directory="view"))

@app.get("/")
def index():
    return RedirectResponse("/view/chat.html")

@app.post("/ask/chat")
def ask_chat(param:ChatModel):
    print(param.q)
    return StreamingResponse(
        start_agent(param.q),
        media_type="text/plain",
    )