# Python 3.10 이미지를 베이스로 사용
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필수 라이브러리 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 및 설정 파일 복사
COPY . .

# Cloud Run Jobs 실행을 위한 엔트리포인트 설정
CMD ["python", "cloud_entry.py"]
