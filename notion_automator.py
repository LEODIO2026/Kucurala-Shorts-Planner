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
        """[v6.0] 보고서형 레이아웃: 테이블 및 섹션화된 가독성 중심 전송"""
        if not self.token or not self.database_id:
            print("[CAUTION] Notion 인증 정보가 없어 로컬 출력으로 대체합니다.")
            return False

        url = "https://api.notion.com/v1/pages"
        
        # 1. 속성(Properties)
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "기획 주제": {"title": [{"text": {"content": script_data['title']}}]},
                "날짜": {"date": {"start": datetime.date.today().isoformat()}},
                "장르": {"select": {"name": script_data['genre']}},
                "참고 영상 URL": {"url": script_data['reference_url']}
            },
            "children": [
                # 섹션 1: 글로벌 트렌드 데이터 분석
                {"object": "block", "type": "heading_2", "heading_2": {
                    "rich_text": [{"text": {"content": "📊 글로벌 트렌드 데이터 분석 (Trend Analysis)"}}]
                }},
                {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {
                    "rich_text": [{"text": {"content": "핵심 트렌드: "}, "annotations": {"bold": True}}, {"text": {"content": script_data['trend_analysis']['core_trend']}}]
                }},
                {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {
                    "rich_text": [{"text": {"content": "성공 공식: "}, "annotations": {"bold": True}}, {"text": {"content": script_data['trend_analysis']['success_formula']}}]
                }},
                {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {
                    "rich_text": [{"text": {"content": "타겟 시청층: "}, "annotations": {"bold": True}}, {"text": {"content": script_data['trend_analysis']['target_audience']}}]
                }},
                {"object": "block", "type": "divider", "divider": {}},
                
                # 섹션 2: 100M 뷰 타겟 숏츠 기획안 (테이블)
                {"object": "block", "type": "heading_2", "heading_2": {
                    "rich_text": [{"text": {"content": "🎬 100M 뷰 타겟 숏츠 기획안 (Script Table)"}}]
                }},
                {
                    "object": "block",
                    "type": "table",
                    "table": {
                        "table_width": 4,
                        "has_column_header": True,
                        "has_row_header": False,
                        "children": [
                            # 헤더 로우
                            {
                                "type": "table_row",
                                "table_row": {
                                    "cells": [
                                        [{"type": "text", "text": {"content": "시간"}}],
                                        [{"type": "text", "text": {"content": "화면 (Visual)"}}],
                                        [{"type": "text", "text": {"content": "오디오 (Audio)"}}],
                                        [{"type": "text", "text": {"content": "비고"}}]
                                    ]
                                }
                            }
                        ]
                    }
                },
                {"object": "block", "type": "divider", "divider": {}},
                
                # 섹션 3: 실행 보고 및 데이터베이스 연동 현황
                {"object": "block", "type": "heading_2", "heading_2": {
                    "rich_text": [{"text": {"content": "✅ 실행 보고 및 전략 제안 (Execution Report)"}}]
                }},
                {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {
                    "rich_text": [{"text": {"content": "노션 리스트업: "}, "annotations": {"bold": True}}, {"text": {"content": script_data['execution_strategy']['listing_status']}}]
                }},
                {"object": "block", "type": "bulleted_list_item", "bulleted_list_item": {
                    "rich_text": [{"text": {"content": "전략 제안: "}, "annotations": {"bold": True}}, {"text": {"content": script_data['execution_strategy']['strategy_proposal']}}]
                }}
            ]
        }

        # 테이블 로우 추가
        for row in script_data['script_table']:
            payload["children"][6]["table"]["children"].append({
                "type": "table_row",
                "table_row": {
                    "cells": [
                        [{"type": "text", "text": {"content": row['time']}}],
                        [{"type": "text", "text": {"content": row['visual']}}],
                        [{"type": "text", "text": {"content": row['audio']}}],
                        [{"type": "text", "text": {"content": row['remarks']}}]
                    ]
                }
            })

        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=5)
            if response.status_code == 200:
                print(f"[SUCCESS] 기획안 '{script_data['title']}'이 v6.0 보고서 스타일로 전송되었습니다.")
                return True
            else:
                print(f"[ERROR] 노션 전송 실패: {response.text}")
                return False
        except Exception as e:
            print(f"[DEBUG] 예외 발생: {e}")
            return False

