# 1. 원하는 공유 저장소에 접근

# 2. git 초기화

# 3. 변경한 파일 staged
# git add [원하는 파일]
git add readme.md
# 변경사항 모두
git add .

# 상태 확인
git status

# commit 하기
git commit -m "first commit"

# commit의 상태 확인
git log --graph --oneline --all

# 이후 vs code로 활용 가능

# 원격 저장소 등록
git remote add origin https://github.com/chaechae001/yeardream_2026.git

# 기본 브랜치 이름 변경 (main이라고 이름 잡아줌)
git branch -M main

