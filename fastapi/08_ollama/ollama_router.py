# uvicorn main:app
# ollama model 확인 방법
# 1. huggingface.co에서 App이 ollama이거나 파일 뒤 GGUF가 붙은 모델 사용
# 2. ollama.com/search
from typing import Dict, Any

from fastapi import APIRouter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# ask라는 요청이 오면 여기로 들어와
router = APIRouter(prefix="/ask", tags=["ask"])

# 모델 생성
model = ChatOllama(model="exaone3.5:2.4b")

# 프롬프트 틀 제작 (system & user)
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 정확한 정보를 전달해주는 AI 분야 전문가입니다., 알기 쉽게 예시를 주면서 설명하세요"),
    ("user", "{topic}에 대해서 설명해 주세요.")
])

# app이 아닌 router
@router.post("/batch")  # /ask/batch 로 해야 올 수 있음
# post로 받을 땐 단일 변수로 받을 수 없다.
# dict 또는 class (model)로 받음 cf) 일반적으로 class(model)로 받음
    # : 은 타입힌트
def get_answer(info:Dict[str,Any]):
    # 파이프라인 조립 LCEL(Lang Chain Express Language)
    # | : 파이프라인을 통해 전달
    # StrOutputParser : 문자열로 바꿔서 전달
    chain = prompt | model | StrOutputParser()

    # 추론 실행
    query = info['q']
    result = chain.invoke({"topic":query})
    return {"msg": result}




