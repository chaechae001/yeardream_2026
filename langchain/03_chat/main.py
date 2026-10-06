from typing import Dict

from fastapi import FastAPI
from starlette.responses import RedirectResponse, StreamingResponse
from starlette.staticfiles import StaticFiles

from ollama_service import chat_answer

app = FastAPI()

# 정적 파일 마운트
# 브라우저에서 '/view' 경로로 접속하면, 서버의 'view'폴더 내의 파일들(chat.html 등)을 제공
app.mount("/view",StaticFiles(directory="view"))

# 루트 도메인('/') 접속 시 리다이렉트
@app.get("/")
def main():
    return RedirectResponse("/view/chat.html")

@app.post("/ask/chat")
def ask_chat(info:Dict[str,str]):
    print(f'input : {info['q']}')
    return StreamingResponse(chat_answer(info['q']), media_type="text/plain")