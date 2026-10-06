# uv pip install fastapi uvicorn
# uvicorn main:app --host=0.0.0.0
# 실행 후 0.0.0.0 대신 localhost 또는 ip 적으면 메시지 보임
# 192.168.1.69
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def main():
    return {"message": "안녕하세요 JUNG, CHAE-EUN 입니다."}