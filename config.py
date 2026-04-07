import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Config:
    """에이전트 쿠라 전역 설정 관리 클래스"""
    
    # Notion API 설정
    NOTION_TOKEN = os.getenv("NOTION_TOKEN", "")
    NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "")
    
    # 글로벌 타겟 설정 (1순위: 북미, 2순위: 글로벌)
    PRIMARY_TARGET_REGION = "USA"
    GLOBAL_VIRAL_THRESHOLD = 50_000_000  # 최소 5,000만 뷰 이상 성공 사례 분석
    
    # 숏츠 기획 로직 상수
    MIN_HOOK_DURATION_SEC = 1.5
    MAX_HOOK_DURATION_SEC = 3.0
    LOOP_ENDING_DELAY = 1.0  # 무한 루프 유도를 위한 엔딩 딜레이
    
    # 데일리 리포트 시간 (KST)
    REPORT_TIME_KST = "09:00"

    @classmethod
    def validate(cls):
        """필수 설정값 유효성 검증"""
        if not cls.NOTION_TOKEN or not cls.NOTION_DATABASE_ID:
            print("[CAUTION] Notion API 정보가 누락되었습니다. .env 파일을 확인해 주세요.")
            return False
        return True
