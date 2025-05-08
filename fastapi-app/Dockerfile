# Python 3.9 베이스 이미지 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성은 root 권한으로 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 비루트 사용자 생성
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# 필요한 파일 복사
COPY . .

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]