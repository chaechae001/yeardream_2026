# PuTTY 에서 복사 붙여넣기 할 때는 Ctrl C, V가 아님
# 마우스 우클릭 : 붙여넣기

# PuTTY에서 아래 순서대로 설치
# 1. python 설치
sudo yum install -y python3.14 python3.14-pip
python3.14 --version

# 현재 경로
pwd

# 현재 디렉토리의 리스트
ls -al

# 2. 디렉토리 생성
mkdir app
# 생성된 디렉토리로 들어가기
cd app

# 3. 가상환경 생성 및 실행
python3.14 -m venv venv
source venv/bin/activate

# pip 업그레이드 / uv 설치
pip install --upgrade pip
pip install uv

# requirements.txt 생성 및 수정
vim requirements.txt
# 한칸 띄어서 작업하고 싶을 때는 o 누르고 타이핑
# i (Insert) 누른 후 아래 내용 타이핑
fastapi
uvicorn
# ESC 누른 후 -> :wq 타이핑
# :wq (저장하고 나가기) / :q (저장안하고 그냥 나가기)
cat requirements.txt

# 라이브러리 설치
uv pip install -r requirements.txt

# 실행
# --workers는 스레드 수 (CPU Core가 2개라서 지금은 2개로 진행)
uvicorn main:app --host=0.0.0.0 --port=8000 --workers 2

# 멈추지 않고 실행하는 방법
# nohup : no hang up "전화끊지 마라", 즉 종료되지 않고 계속 실행할 수 있게 해준다.
# > uvicorn.log : uvicorn.log 실행 내용을 uvicorn.log로 남기겠다.
# 2>&1: 2는 에러로그, 1은 표준출력로그 (에러로그도 표준출력 로그처럼 출력해라)
# 2>1로 하면 에러로그를 파일명 1에 저장하라고 오해할 수 있어 특수문자 &를 붙임
# & : 백그라운드로 실행해라 (내 UI 가리지마)
nohup uvicorn main:app --host=0.0.0.0 --port=8000 --workers 2 > uvicorn.log 2>&1 &

# 로그확인 방법
# 실시간 : 뒷부분만 -f (follow) 쫓아다니면서 보기
tail -f uvicorn.log
# 전체 읽기
cat uvicorn.log
vim uvicorn.log

# 5. 끄기
# 8000번을 누가 사용하고 있는지?
# List Open File - 있는 거 다 열어
# -i : Internet
# :8000 -> :8000 이라는 문자가 나오는 거
sudo lsof -i :8000

# 해당 프로세스 종료
# -9 : 상관없다 (-f)
kill -9 [PID]

# 가상환경 종료
deactivate

# main.py 파일 삭제
rm -rf main.py