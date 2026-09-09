# uv pip install -r requirements.txt

# 1. 라이브러리 임포트 및 초기 설정
import shutil
import logging
import os
import traceback
import uuid
from typing import List

from fastapi import FastAPI, UploadFile
from starlette.middleware.cors import CORSMiddleware    # 외부 도메인(웹페이지)에서 서버로 요청할 수 있게 허용(CORS)
from starlette.responses import RedirectResponse    # 페이지 이동
from starlette.staticfiles import StaticFiles   # 정적 파일(이미지 등)을 웹에서 바로 볼 수 있게 경로 열어줌

app = FastAPI() # FastAPI 애플리케이션 객체를 생성하여 웹 서버 뼈대 만듬

# 2. 로거(Logger) 설정
# 일반 print 로그의 단점
# 로그가 찍힌 시간, 위치 등을 알 수 없다.
# DEBUG > INFO > WARNING > ERROR > CRITICAL
# 체계적인 로그(시간, 로그 레벨, 메시지)를 남기기 위한 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:     [%(name)s] %(message)s - %(asctime)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)
logger.info("logger test!!")

# 3. 업로드 폴더 준비 및 미들웨어 설정
FILE_PATH = './upload'

# 특정 경로에 폴더 생성
if not os.path.exists(FILE_PATH):
    os.makedirs(FILE_PATH)
    logger.info(f"{FILE_PATH} 생성!")

# CORS 설정 : 웹 프론트엔드와 백엔드 서버의 주소가 달라도 파일 전송 등 통신이 원할하게 이루어지도록 모든 접근(*)을 허용
app.mount("/view",StaticFiles(directory="view"))
app.mount("/images",StaticFiles(directory=FILE_PATH))
app.add_middleware(CORSMiddleware,allow_origins=["*"], allow_methods=["*"])

# 4. 기본 라우팅 설정
# 사용자가 웹 서버의 메인 주소로 접속하면, 곧바로 파일 업로드를 할 수 있는 화면인 페이지로 자동 이동
@app.get("/")
def main():
    return RedirectResponse("/view/upload.html")

# 5. 파일 업로드 핵심 로직 (/upload)
@app.post("/upload")
def upload(files: List[UploadFile]):    # 다중파일 수신 - 클라이언트가 보낸 여러 개의 파일을 한 번에 리스트 형태로 받음

    msg= "파일업로드가 실패 했습니다."

    try:
        for file in files:
            logger.info(f'file name : {file.filename}') # img.png -> 12345679.png
            ori_filename = file.filename

            # 1. 파일명과 확장자 분리
            # name,ext = ori_filename.split('.')    # .을 기준으로 나눔
            name, ext = os.path.splitext(ori_filename)  # ext: 확장자를 기준으로 나눔
            logger.info(f'{name} / {ext}')
            # 2. 파일명 변경 (UUID - 중복이름 방지)
            # 중복 이름 방지를 위해 유일한 무작위 문자열 생성하고 기존 확장자(ext)를 붙여 새로운 파일 이름으로 만듬
            new_filename = f'{uuid.uuid4()}{ext}'
            # 3. 새로운파일명 + 확장자
            logger.info(f'new file name = {new_filename}')
            # 4. 파일 저장
            save_path = f'{FILE_PATH}/{new_filename}'
            # open (파일을 읽는 함수)
            # w: write, r:read, b:binary, t:text, +:read&write
            # with: 자원을 사용한 후 로직이 종료되면 함께 닫아준다
            with open(save_path, 'wb') as file_obj:
                shutil.copyfileobj(file.file, file_obj)

            msg = "파일 업로드에 성공했습니다."

    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())    # 상세 에러로그 보기

    return {"msg": msg}

@app.get("/files")
def files():
    # 특정 경로의 파일 리스트를 가져옴
    file_list = os.listdir(FILE_PATH)
    logger.info(file_list)
    return {"files":file_list}

@app.get("/delete")
def delete(filename:str):
    path = f'{FILE_PATH}/{filename}'
    if os.path.exists(path):
        os.remove(path)
    return RedirectResponse("/view/file_list.html")

@app.get("/download")
def download(filename:str):
    path = f'{FILE_PATH}/{filename}'
    if os.path.exists(path):
        return RedirectResponse(path, media_type="application/octet-stream", filename=filename)
    else:
        return {"msg":"해당 파일이 없습니다."}