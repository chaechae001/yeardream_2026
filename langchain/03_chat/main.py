from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

import chat_router

app = FastAPI()

# 1. CORS(Cross-Origin Resource Sharing) 설정
# ["*"]: 모든 도메인에서의 접근 허용
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

# 2. 정적 파일 마운트
# 브라우저에서 '/view' 경로로 접속하면, 서버의 'view'폴더 내의 파일들(chat.html 등)을 제공
app.mount("/view", StaticFiles(directory="view"))

# 3. 라우터 연결
# chat_router.py에 정의된 API 엔드포인트들을 FastAPI 앱에 포함시킴
app.include_router(chat_router.router)

# 4. 루트 도메인('/') 접속 시 리다이렉트
@app.get("/")
def main():
    return RedirectResponse("/view/chat.html")

"""
@app.post("/ask/chat")
def ask_chat(info:Dict[str, str]):
    print(f'input : {info['q']})
    
    return StreamingResponse(chat_answer(info['q']), media_type="text/plain")
"""