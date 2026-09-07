from datasets import load_dataset

# 전체 훈련 데이터 중 앞에서 딱 200개만 샘플로 가져옴
# split='train[:200]' : train의 0~199까지만 가져와라
# 허깅페이스 허브에서 영화 리뷰 데이터셋(로튼 토마토)을 다운로드
dataset = load_dataset('cornell-movie-review-data/rotten_tomatoes', split='train[:200]')
# label, text

# 1. label = 0.1 -> negative, positive
"""
def add_label_text(item):
    if item['label'] == 1:
        item['label_text'] = 'positive'
    else:
        item['label_text'] = 'negative'
        
    # return item['label_text'] = 'positive' if item['label'] == 1 else "negative"
    return item
"""

ds = dataset.map(
    # 기존 데이터에는 정답이 숫자 (1 or 0)로만 들어있음
    # 사람이 읽기 편하도록 이를 해석해주는 새로운 컬럼(label_text)을 추가
    # 라벨이 1이면 'positive',  아니면 'negative'로 변환하여 새로운 컬럼에 넣어줌
    lambda item: {'label_text': 'positive' if item['label']==1 else "negative"}
)

# 2. text -> review 컬럼명 변경
# 기존에 text라는 이름을 리뷰 본문 컬럼에 맞게 review라는 이름으로 변경
ds = ds.rename_column('text', 'review')

# 3. 10자 미만의 리뷰는 거른다.
# (item) => len(item['review']) >=10
ds = ds.filter(lambda item: len(item['review']) >=10)

print(f'columns : {ds.column_names}')
print(f'data: {ds[0]}')


# HF에 업로드
# hf auth login --force
# 내가만든 데이터를 고유저장소 주소(내아이디/저장소이름)에 저장
REPO_ID = 'chaeeun01/upload_test_ds'
ds.push_to_hub(REPO_ID, split="train")
print(f'업로드 완료: https://huggingface.co/datasets/{REPO_ID}')