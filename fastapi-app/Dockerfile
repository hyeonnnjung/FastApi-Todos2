# Python 3.9 슬림 이미지 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 설치와 사용자 생성은 root 권한으로 실행
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    adduser --disabled-password --gecos '' appuser

# 이후 명령은 일반 사용자로 실행
USER appuser

# 애플리케이션 파일 복사 (이미 사용자 전환되었기 때문에 권한 이슈 방지 필요)
COPY --chown=appuser:appuser . .

# FastAPI 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]
