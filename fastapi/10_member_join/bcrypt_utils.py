import datetime
import secrets
from typing import Any, Dict

import bcrypt
import jwt

#=========================
# Hash 암호화
#=========================
def encode_pass(plain:str) -> str:
    # 1. 문자열을 byte 형태로 변환
    plain_bytes = plain.encode('utf-8')
    # 2. 해시 암호화 진행
    # salt 값 : 같은 입력을 하여도 결과값이 다르게 나오게 하는 하나의 값
    enc_bytes = bcrypt.hashpw(plain_bytes, bcrypt.gensalt())
    # 3. 문자 형태로 변경 (DB에 저장하기 위해)
    return enc_bytes.decode('utf-8')
"""
plain_text = input('암호화 하려는 문자열을 입력하세요')
hash_text = encode_pass(plain_text)
print(hash_text)
"""
# 실행 후 hello라고 저장 2번했을 때 2번 다 암호화 내용이 바뀜
# $2b$12$wmkLIQ1dybvyt/dycE28a.9QhOlFRmkNhQl4ud6B9NaOefR5rTRzq
# $2b$12$OURoVnCL8znEx7aYnksjUeLQ0ZopofFAfAElur.w2GxCh.s8Ar9xy

#=========================
# 암호화 확인
#=========================
def matches(plain:str, hash:str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hash.encode("utf-8"))

"""
plain_text = input('암호화 하려는 문자열을 입력하세요')
hash_text = encode_pass(plain_text)
print(hash_text)

confirm_text = input('방금 입력한 암호를 다시 입력해보세요')
yn = matches(confirm_text, hash_text)
print(f'일치 여부 : {yn}')
"""

"""
# 결과
암호화 하려는 문자열을 입력하세요hello
$2b$12$6YpO7Oso.uRmvqMvOq4zTul295PE3c346tsx3ZKdY.jhuNTrrx5L2
방금 입력한 암호를 다시 입력해보세요hello
일치 여부 : True
"""

# JWT
# 비밀키, 알고리즘 종류, 유지시간
SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
TOKEN_EXPIRE_MIN = 30

def get_token(data: dict[str,Any]) -> str:
    """특정한 내용을 넣으면 토큰으로 생성
    :param data : 토큰에 저장할 내용
    :return : 토큰 문자열
    """
    # 내용에는 토큰 수명도 추가해야 한다.
    # 현재시간으로부터 30분이 지난걸 더해줌
    expire_time = datetime.datetime.now() + datetime.timedelta(minutes=TOKEN_EXPIRE_MIN)
    data.update({'exp':expire_time})  # exp라는 이름으로 expire_time을 data에 업데이트 해줌
    # jwt.encode(내용, 비밀키, 알고리즘)
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token:str)-> Dict[str, Any]:
    """
    토큰 문자열을 넣으면 토큰에 저장된 데이터를 반환
    :param token: 토큰 문자열
    :return: 토큰의 내용이 담긴 Dict 반환
    """
    payload = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

    except Exception as e:  # 비밀키가 틀렸거나, 토큰 시간이 만료된 경우
        print(e)

    return payload
"""
result_token = get_token({"id": "admin", "name": "김지훈"})
print(f'생성된 토큰 : {result_token}')
result_payload = verify_token(result_token)
print(f'payload : {result_payload}')


$2b$12$5cdPKBkHaHCLRs.0oj.OGOSSpmclc50SeqKdEHxi3IcqO4/NP6sBO
생성된 토큰 : eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImFkbWluIiwibmFtZSI6Ilx1YWU0MFx1YzljMFx1ZDZjOCIsImV4cCI6MTc5MDYwNDA4MH0.6qptDseuV9IK8CrjSU36diV1jmP9vJPt_saSyekpQxo
payload : {'id': 'admin', 'name': '김지훈', 'exp': 1790604080}
"""






