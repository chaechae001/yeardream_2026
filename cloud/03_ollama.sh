# Ollama 설치
curl -fsSL https://ollama.com/install.sh | sh

# 설치 확인
sudo systemctl status ollama

# 모델 설치
ollama run gemma4:e2b

# /bye로 종료 후..

# 사용 IP 확인
sudo lsof -i :11434
# localhost:11434 (LISTEN)

# 다른 IP에서 사용할 수 있도록 개방
sudo systemctl edit ollama.service

# 커서 옮겨서 아래 내용 입력
[Service]
Environment = "OLLAMA_HOST=0.0.0.0" 

# ctrl + O -> Enter(저장) -> ctrl + X (종료)

# Ollama 재시동
sudo systemctl daemon-reload
sudo systemctl restart ollama

# http://43.202.251.63:11434/ 에서 확인 가능
# Ollama is running

# 소스 이동 (main.py, ollama_service.py, view, requirements.txt)
vim ollama_service.py
# 모델명 수정 후 ESC -> : wq

# 가상환경 생성
python3.14 -m venv .venv
# 가상환경 실행
source venv/bin/activate

# requirements.txt 설치
pip install --upgrade pip
pip install uv
uv pip install -r requirements.txt

# 서버시작
uvicorn main:app --host=0.0.0.0 --port=8000

# 종료
# ctrl + c
deactivate  # 가상화 종료
cd ../      # 현재 위치에서 한단계 올라가서
rm -rf app  # app 폴더 삭제
