from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate, structured
from langchain_ollama import ChatOllama
from starlette.responses import RedirectResponse

from review_model import ReviewAnalysis

app = FastAPI()

@app.get("/")
def main():
    return RedirectResponse("/docs")

# 1. ollama model 호출
model = ChatOllama(model = "exaone3.5:2.4b")

# 2. 프롬프트 템플릿 생성
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 리뷰 분석가 입니다. 리뷰를 분석하여 지정된 형식으로 반드시 한글로만 답변하세요."),
    ("human", "리뷰 : {review}")
])

# 3. 출력 구조화 선언
structured_model = model.with_structured_output(ReviewAnalysis)

@app.get("/review/analysis")
def get_structured(review:str):
    # 4. 파이프라인 조립
    # structured_model에서 이미 model을 불러오기 때문에 model은 뺌
    chain = prompt | structured_model
    # 5. 출력
    result = chain.invoke({'review':review})
    print(result)
    # 일반적으로는 model_dump() / 보내는 내용이 복잡하면 model_dump_json()
    # return result.model_dump_json() # json 형태의 문자열 (받는 쪽에서 JSON.parse()써줘야 함)
    return result.model_dump()  # dict 형태로 변환 -> fastapi에선 dict로 반환하면 json으로 자동 변환
