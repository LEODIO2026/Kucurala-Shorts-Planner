import os
import sys
from main import KuraOrchestrator

def run_cloud_mission():
    """
    클라우드 환경(Cloud Run Job)에서 실행되는 메인 로직입니다.
    매일 아침 자동화된 기획 및 노션 전송을 담당합니다.
    """
    print("--- [에이전트 쿠라] 클라우드 무인 기획실 가동 ---")
    
    # 환경 변수 체크 (Cloud Run에서 주입)
    if not os.getenv("NOTION_TOKEN") or not os.getenv("NOTION_DATABASE_ID"):
        print("[ERROR] 필수 환경 변수(NOTION_TOKEN, NOTION_DATABASE_ID)가 설정되지 않았습니다.")
        sys.exit(1)

    try:
        orchestrator = KuraOrchestrator()
        orchestrator.run_daily_mission()
        print("--- [SUCCESS] 클라우드 데일리 미션 완료 ---")
    except Exception as e:
        print(f"--- [FAILED] 미션 수행 중 오류 발생: {e} ---")
        sys.exit(1)

if __name__ == "__main__":
    run_cloud_mission()
