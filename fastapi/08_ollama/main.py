from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

import ollama_router

app = FastAPI()

# CORSMiddleware : 서로 다른 출처(도메인) 간의 자원 공유를 허용/제한하기 위해 웹서버에서 사용하는 미들웨어
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])
app.mount("/view", StaticFiles(directory="view"))

@app.get("/")
def main():
    return RedirectResponse("/index.html")

# router 등록
# ollama_router에 있는 router 가져오기
app.include_router(ollama_router.router)
