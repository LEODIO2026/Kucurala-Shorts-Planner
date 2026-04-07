import requests
import datetime
from config import Config

class NotionAutomator:
    """
    [v5.0] 프로덕션 최적화 포매터: 대본을 페이지 본문에 직접 배치하여 가독성을 극대화합니다.
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
        """[v5.0] 프로덕션용 본문(Body) 중심 레이아웃으로 전송"""
        if not self.token or not self.database_id:
            print("[CAUTION] Notion 인증 정보가 없어 로컬 출력으로 대체합니다.")
            return False

        url = "https://api.notion.com/v1/pages"
        
        # 1. 속성(Properties) 정의: 미니멀리즘 적용
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "기획 주제": {"title": [{"text": {"content": script_data['title']}}]},
                "날짜": {"date": {"start": datetime.date.today().isoformat()}},
                "장르": {"select": {"name": script_data['genre']}}, # 핵심 키워드 매칭
                "참고 영상 URL": {"url": script_data['reference_url']}
            },
            # 2. 본문(Children) 정의: 대본 가독성 극대화
            "children": [
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {"rich_text": [{"text": {"content": "🔥 핵심 후킹 포인트"}}]}
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [
                            {
                                "text": {"content": script_data['hook_3s']['action']},
                                "annotations": {"bold": True, "color": "orange"}
                            }
                        ]
                    }
                },
                {
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                },
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {"rich_text": [{"text": {"content": "🎬 촬영 콘티 (Story Flow)"}}]}
                }
            ]
        }

        # 3. 본문에 스토리 라인 블록별로 추가
        for scene in script_data['story_flow']:
            payload["children"].append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"text": {"content": scene}}]}
            })

        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=5)
            if response.status_code == 200:
                print(f"[SUCCESS] 기획안 '{script_data['title']}'이 생산용 본문 레이아웃(v5.0)으로 전공되었습니다.")
                return True
            else:
                print(f"[ERROR] 노션 전송 실패: {response.text}")
                return False
        except Exception as e:
            print(f"[DEBUG] 예외 발생: {e}")
            return False
