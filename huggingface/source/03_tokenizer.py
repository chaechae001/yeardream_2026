# Tokenizer를 불러와야 하는데 어떤 클래스를 쓸 지 잘 모르겠다.
from transformers import AutoTokenizer

# 토크나이저 호출
# AutoTokenizer : 실행될 때 auto로 찾아줘서, 자동완성이 안뜸
model_id = "tabularisai/multilingual-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(model_id)


# 입력 받기
user_input = input('문장입력: \n')
print(f'1. 입력받은 문장 : {user_input}')

token = tokenizer.tokenize(user_input)
print(f'2. 토큰들 : {token}')

input_ids = tokenizer.convert_tokens_to_ids(token)
# 받은 토큰을 그대로 숫자화 함
print(f'3-1. AI가 인식할 수 있는 숫자로 변환 : {input_ids}')

input_ids = tokenizer.encode(user_input)
# 문자를 받아 자체적으로 토큰화 하고, 특수토큰도 넣어서 반환 ([CLS][SEP])
# 앞에 101번 넣어서 문장 시작 뜻함, 끝에 102번 넣어서 문장 끝을 뜻함
print(f'3-2. AI가 인식할 수 있는 숫자로 변환 : {input_ids}')
