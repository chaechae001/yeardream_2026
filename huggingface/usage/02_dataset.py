# uv pip install datasets
from datasets import load_dataset
from transformers import AutoTokenizer

# BERT 모델이 텍스트를 읽을 수 있도록 글자를 숫자로 쪼개주는 토크나이저 불러옴
tokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
# 텍스트(리뷰내용)를 모델이 이해할 수 있는 토큰 ID로 변환하고,
# 모델의 최대 입력 길이를 초과하지 않도록 자르는(truncation=True)규칙 정의
def token_func(ds):
    return tokenizer(ds['text'], truncation=True, max_length=128)

if __name__ == '__main__':  # 이름이 메인이라면 실행해라
    # 병렬처리를 할 때는 이 내용 자체를 메인스레드가 실행하도록 설정해줘야 한다.
    # 1. HF에서 데이터셋 불러오기
    # 영화 리뷰 감성 분석 데이터셋 (IMDB의 훈련용 데이터) 다운로드
    dataset = load_dataset('stanfordnlp/imdb', split='train')
    print(dataset)

    # 2. 데이터 전처리
    # map() : 데이터 변환하기
    # 데이터셋 안에 있는 모든 데이터(행)에 일괄적으로 어떤 함수나 작업을 적용할 때 씀
    encoded_ds = dataset.map(
        token_func,     # 해야할 일
        batched=True,   # 특정 단위로 작업을 몰아서 처리
        num_proc=4,     # 사용할 스레드 수
        remove_columns=['text'],    # 불필요한 컬럼 삭제
    )
    print('전처리 완료: ', encoded_ds)

    # filter: 특정 조건의 샘플만 가져오도록
    # 원하는 특정 조건을 만족하는 샘플만 남기고 나머지 전부 버림
    # item=> item.label == 1
    # positive
    pos_ds = encoded_ds.filter(
        lambda item : item['label'] == 1,
        num_proc=4
    )
    print(f'filtering : {pos_ds}')

    # map을 가지고 토큰 수를 length로 추가한다
    # function(item) {
    #   item['length'] = len(item['input_ids'])
    #   return item
    # }
    # 축약 : item => {'length' : len(item['input_ids'])}
    pos_ds = pos_ds.map(
        lambda item: {'length': len(item['input_ids'])},
        num_proc=4
    )
    print(f'pos_ds : {pos_ds}')

    # sort : 줄 세우기
    # 특정 컬럼의 값을 기준으로 데이터를 크기순이나 알파벳순으로 정렬
    sorted_ds = pos_ds.sort("length", reverse=True)

    # select() : 특정갯수 n개만 가져온다.
    # 데이터의 인덱스(순번)를 기준으로 원하는 샘플만 부분 추출
    top10_df = sorted_ds.select([0,1,2,3,4,5,6,7,8,9])  # range(10)

    # 상위 10개로 추려진 데이터셋을 반복문으로 돌면서, 각 리뷰의 토큰 길이와 라벨 값을 화면에 출력
    for i, item in enumerate(top10_df):
        print(f'[{i}] : 토큰길이 : {item['length']} / Label:{item['label']}')