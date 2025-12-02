FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 종속성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY app.py .

# SQLite DB 파일이 저장되는 디렉토리를 VOLUME으로 선언
# Docker나 Kubernetes가 이 경로를 호스트 시스템 또는 영구 저장소에 마운트할 수 있게 함
VOLUME /app/data

EXPOSE 5000

# Flask 애플리케이션 실행 (컨테이너 내부 포트 5000)

CMD ["python", "app.py"]
