import requests
import datetime
from config import Config

class NotionAutomator:
    """
    Mission 3: Notion 자동화 연동 모듈
    생성된 기획안을 지정된 노션 데이터베이스로 전송합니다.
    """

    def __init__(self):
        self.token = Config.NOTION_TOKEN
        self.database_id = Config.NOTION_DATABASE_ID
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

    def push_script_to_notion(self, script_data):
        """기획안 데이터를 노션 데이터베이스 필드에 맞춰 전송"""
        if not self.token or not self.database_id:
            print("[CAUTION] Notion 인증 정보가 없어 로컬 출력으로 대체합니다.")
            print(script_data)
            return False

        url = "https://api.notion.com/v1/pages"
        
        # 데이터베이스 필드 맵핑 (사용자 요청 규격 준수)
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "기획 주제": {"title": [{"text": {"content": script_data['title']}}]},
                "날짜": {"date": {"start": datetime.date.today().isoformat()}},
                "예상 조회수": {"rich_text": [{"text": {"content": "100M+ (글로벌 1억 뷰 타겟)"}}]},
                "핵심 후킹 포인트": {"rich_text": [{"text": {"content": script_data['hook_3s']['action']}}]},
                "글로벌 타겟 국가": {"select": {"name": script_data['global_target']}},
                "대본 원문": {"rich_text": [{"text": {"content": str(script_data['body_60s'])}}]},
                "참고 영상 URL": {"url": "https://www.youtube.com/shorts/sample_viral_ref"}
            }
        }

        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=5)
            if response.status_code == 200:
                print(f"[SUCCESS] 기획안 '{script_data['title']}'이 노션에 성공적으로 리스트업되었습니다.")
                return True
            else:
                print(f"[ERROR] 노션 전송 실패: {response.text}")
                return False
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print("\n" + "!"*50)
            print(f"[DEBUG] 실제 에러 원인: {e}")
            print("!"*50)
            print("\n" + "="*50)
            print("[OFFLINE MODE] 네트워크 연결 불가로 로컬에 기획안을 출력합니다.")
            print(f"주제: {script_data['title']}")
            print(f"후킹(3s): {script_data['hook_3s']['action']}")
            print(f"본문 요약: {script_data['body_60s']}")
            print("="*50 + "\n")
            return True

if __name__ == "__main__":
    from script_architect import ScriptArchitect
    architect = ScriptArchitect()
    sample_script = architect.generate_viral_skit_script()
    
    automator = NotionAutomator()
    automator.push_script_to_notion(sample_script)
