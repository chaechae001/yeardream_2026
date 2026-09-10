from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

# 같은 폴더에 있는 ollama_router.py 파일 불러옴
# 구체적인 API 기능들이 정의되어 있음
import ollama_router

app = FastAPI()

# CORS(교차 출처 리소스 공유) 설정 추가
# 프론트엔드 주소와 백엔드 주소가 달라서 브라우저가 보안상 요청을 차단하는 에러가 자주 발생해서
# allow_origins=["*"] : 세상에 모든 주소()에서 내 서버로 접속하는 걸 허락
# allow_methods=["*"] : GET, POST 등 모든 방식의 요청 허락
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

# 웹 서버에 view라는 폴더를 연결(mount)하는 작업
app.mount("/view", StaticFiles(directory="view"))
# 위에서 불러온 ollama_router의 기능들을 메인 app에 끼워 넣음
app.include_router(ollama_router.router)


# 서버의 기본주소로 접속 (GET 요청)했을 때 아래 함수 실행
@app.get("/")
def main():
    # 접속하자마자 메인화면(HTML)이 뜨도록 자동이동 (리다이렉트) 시킴
    return RedirectResponse("/view/index.html")