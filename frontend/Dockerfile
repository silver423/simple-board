FROM nginx:alpine

# 1. 사용자 정의 설정 파일을 Nginx 설정 경로에 복사
# Nginx는 보통 /etc/nginx/conf.d/default.conf 파일을 사용합니다.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 2. 정적 웹 파일 복사
COPY index.html /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/
# 기타 모든 정적 파일 복사...

# COPY . /usr/share/nginx/html  <-- 모든 파일을 복사하는 경우