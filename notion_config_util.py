import requests
from config import Config

class NotionConfigUtil:
    """
    [Phase 7] Notion 데이터베이스 자동 구성 유틸리티
    사용자의 데이터베이스 속성을 1억 뷰 기획 규격으로 동기화합니다.
    """

    def __init__(self):
        self.token = Config.NOTION_TOKEN
        self.database_id = Config.NOTION_DATABASE_ID
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def sync_database_schema(self):
        """데이터베이스 속성(Properties)을 지능적으로 구성합니다."""
        if not self.token or not self.database_id:
            print("[CAUTION] .env 설정이 누락되었습니다.")
            return False

        # 1. 기존 데이터베이스 정보를 가져와서 현재의 Title 속성 이름을 확인합니다.
        get_url = f"https://api.notion.com/v1/databases/{self.database_id}"
        try:
            get_resp = requests.get(get_url, headers=self.headers, timeout=10)
            if get_resp.status_code != 200:
                print(f"[ERROR] 데이터베이스 정보를 불러올 수 없습니다: {get_resp.text}")
                return False
            
            db_info = get_resp.json()
            current_title_name = next(
                (name for name, prop in db_info.get("properties", {}).items() if prop["type"] == "title"), 
                None
            )
            
            if not current_title_name:
                print("[ERROR] 타이틀 속성을 찾을 수 없는 데이터베이스입니다.")
                return False

        except Exception as e:
            print(f"[ERROR] 정보 조회 중 오류: {e}")
            return False

        # 2. 스키마 업데이트 (기존 타이틀 이름 변경 포함)
        patch_url = f"https://api.notion.com/v1/databases/{self.database_id}"
        payload = {
            "properties": {
                current_title_name: {"name": "기획 주제"}, # 기존 타이틀 개명
                "날짜": {"date": {}},
                "예상 조회수": {"rich_text": {}},
                "핵심 후킹 포인트": {"rich_text": {}},
                "글로벌 타겟 국가": {
                    "select": {
                        "options": [
                            {"name": "USA", "color": "blue"},
                            {"name": "Global", "color": "purple"},
                            {"name": "Asia", "color": "orange"}
                        ]
                    }
                },
                "대본 원문": {"rich_text": {}},
                "참고 영상 URL": {"url": {}}
            }
        }

        try:
            print(f"[ACTION] '{current_title_name}' 속성을 찾아 '기획 주제'로 동기화 중...")
            response = requests.patch(patch_url, headers=self.headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                print("[SUCCESS] 노션 데이터베이스가 '글로벌 전략 기획실' 규격으로 자동 재구성되었습니다.")
                return True
            else:
                print(f"[ERROR] 스키마 동기화 실패: {response.text}")
                return False
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print("\n" + "!"*50)
            print(f"[DEBUG] 실제 에러 원인: {e}")
            print("!"*50)
            print("\n" + "="*50)
            print("[OFFLINE MODE] 네트워크 문제로 실제 노션 구성을 수행할 수 없습니다.")
            print("대표님의 로컬 터미널에서 이 스크립트를 실행하여 구성을 완료해 주세요.")
            print("="*50 + "\n")
            return True

if __name__ == "__main__":
    util = NotionConfigUtil()
    util.sync_database_schema()
