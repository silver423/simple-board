FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 종속성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY app.py .

EXPOSE 5000

# Flask 애플리케이션 실행 (컨테이너 내부 포트 5000)
CMD ["python", "app.py"]