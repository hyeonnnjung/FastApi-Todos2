# Python 3.9-slim 이미지를 기반으로 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 먼저 복사하고 설치
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 코드 복사
COPY . .

# 비루트 유저 생성
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser /app

# 비루트 유저로 전환
USER appuser

# FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]
