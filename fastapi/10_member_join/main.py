import logging
from enum import verify
from typing import Dict, Any

from fastapi import FastAPI
from sqlalchemy import text
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles

from bcrypt_utils import encode_pass, matches, get_token, verify_token
from db import get_conn

app = FastAPI()
app.mount("/view", StaticFiles(directory="view"))

# 서버에서 발생하는 이벤트나 에러를 기록하기 위한 로거(Logger) 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:     [%(name)s] %(message)s - %(asctime)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

@app.get("/")
def main():
    return RedirectResponse("/view/login.html")

# 로그인 요청을 처리하는 API (POST 방식)
@app.post("/login")
def login(info:Dict[str,str], req:Request):
    # 기본 응답 형태 설정 (로그인 실패 상태로 초기화)
    json = {'success': False, 'token': ''}
    logger.info(f'info={info}')

    # 이 사람이 회원이라는 것을 어떻게 증명?
    # 아이디 비밀번호가 모두 일치하면 True, 아니면 False
    # 특정 id에 대한 pw값을 가져와서 매칭여부를 파악하기

    # 1. 입력받은 id를 통해 pw 가져옴
    # 데이터베이스 연결 가져오기
    conn = get_conn()
    sql = text("SELECT pw FROM member WHERE id = :id")

    try :
        # 2. 입력받은 pw와 가져온 pw를 비교
        result = conn.execute(sql, {"id": info['id']}).mappings().fetchone()
        success = matches(info['pw'], result['pw'])

        # 3. True일 경우 로그인 성공으로 가정
        if success:
            token = get_token({"id": info["id"], "ip": req.client.host})
            json.update({'success': success, 'token': token})

    except Exception as e:
        logger.error(e)
    finally:
        conn.close()

    return json

# 아이디 중복 확인을 처리하는 API (GET 방식, 쿼리 파라미터로 id를 받음)
@app.get("/overlay")
def overlay(id:str):
    cnt = 1
    logger.info(id)

    # 1. 데이터베이스에 접속할 수 있는 연결 객체(Connection) 가져오기
    conn = get_conn()

    # 2. 전달받은 id와 일치하는 회원의 수를 세는 SQL 쿼리문 준비
    sql = text('SELECT COUNT(id) AS cnt FROM member WHERE id = :id')

    # 3. 쿼리 실행 및 결과를 딕셔너리 형태로 가져오기 (fetchone()은 단 하나의 결과 행을 가져옴)
    result = conn.execute(sql, {'id': id}).mappings().fetchone()
    logger.info(f'result : {result}')

    # 4. 조회된 결과에서 아이디 개수 추출 (0이면 사용 가능, 1 이상이면 이미 존재하는 아이디)
    cnt = result['cnt']

    # 5. 사용을 마친 데이터베이스 연결 종료
    conn.close()

    # 결과를 클라이언트에게 반환 (예: {"use": 0})
    return {"use": cnt}

# 회원가입 요청을 처리하는 API (POST 방식, 다양한 타입의 데이터를 받기 위해 Dict[str, Any] 사용)
@app.post("/join")
def join(info:Dict[str,Any]): # POST 방식은 파라메터를 Dict 또는 class 로 받아야 한다.
    logger.info(f'info={info}')

    # DB 접속
    conn = get_conn()
    row = 0

    # 보안을 위해 사용자가 입력한 비밀번호를 암호화(bcrypt)한 뒤 다시 저장
    info['pw'] = encode_pass(info['pw'])

    # 회원 정보를 테이블에 추가(INSERT)하기 위한 SQL 쿼리문 준비
    sql = text("""INSERT INTO member(id,pw,name,age,gender,email)
                VALUES(:id,:pw,:name,:age,:gender,:email)""")
    try:
        # 쿼리 실행 (딕셔너리 형태의 info 데이터가 SQL의 바인드 변수로 자동 매핑됨)
        result = conn.execute(sql,info)# 실행
        # 쿼리 실행 결과로 영향받은 행(row)의 개수 확인
        logger.info(f"result={result.rowcount}")
        row = result.rowcount
        # 데이터가 정상적으로 추가되었다면 DB에 변경사항 확정(Commit)
        if row > 0:
            conn.commit()

    except Exception as e:
        # 에러 발생 시 로그를 남기고 트랜잭션을 취소(Rollback)하여 데이터 무결성 유지
        logger.error(e)
        conn.rollback()

    finally:
        # 성공하든 실패하든 관계없이 무조건 데이터베이스 연결 종료 (자원 반환)
        conn.close() # DB 접속 종료

    # 처리된 행의 개수를 반환 (1이면 가입 성공)
    return {'row':row}


@app.get("/list/{page}")
def list_page(page:int, req:Request):
    logger.info(f'page={page}')
    login_id = req.query_params.get("id")
    client_ip = req.client.host
    token = req.headers.get("Authorization")
    logger.info(f"id={login_id}")
    logger.info(f"ip={client_ip}")
    logger.info(f"token={token}")
    msg = "로그인이 필요한 서비스입니다."

    try:
        payload = verify_token(token)
        logger.info(f'payload : {payload}')
        if payload is not None:
            if payload.get("id") == login_id and payload.get("ip") == client_ip:
                msg = "로그인된 회원이 맞습니다. 계속 진행"
        else:
            msg = "토큰 정보가 일치하지 않습니다."

    except Exception as e:
        logger.error(e) # 비밀키가 변경되거나 토큰 만료시간이 지났을 때
        msg = "토큰이 만료되었습니다. 다시 로그인을 해주세요."

    return {"msg":msg}