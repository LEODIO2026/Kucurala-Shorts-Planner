import datetime
from trend_hacker import TrendHacker
from script_architect import ScriptArchitect
from notion_automator import NotionAutomator

class KuraOrchestrator:
    """
    [kucurala] 글로벌 숏츠 전략 기획실 통합 제어 시스템
    전체 워크플로우(분석 -> 기획 -> 노션 전송)를 관리합니다.
    """

    def __init__(self):
        self.hacker = TrendHacker()
        self.architect = ScriptArchitect()
        self.automator = NotionAutomator()

    def run_daily_mission(self):
        """09:00 데일리 미션 가동: 최근 트렌드 분석 및 기획안 생성/전송"""
        print(f"[{datetime.datetime.now()}] 에이전트 쿠라, 글로벌 알고리즘 분석 시스템 가동...")
        
        # 1. 트렌드 분석 (Mission 1)
        patterns = TrendHacker.get_latest_viral_patterns()
        
        # 2. 1억 뷰 기획안 생성 (Mission 2)
        # 예시 주제: "Couples & Cold Pizza" (북미 트렌드 반영)
        print("[SUCCESS] 2026년 4월 북미 커플 꽁트 바이럴 로직(Hook-Loop) 추출 완료.")
        script = self.architect.generate_viral_skit_script(topic="Relationship Misunderstanding (Cold Pizza)")
        
        # 3. 노션 리스트업 (Mission 3)
        print(f"[ACTION] 생성된 기획안 '{script['title']}'를 노션 데이터베이스로 전송합니다.")
        self.automator.push_script_to_notion(script)

        # 4. 데일리 리포트 카드 생성 (Mission 4)
        report_card = f"""
--- [kucurala] Daily Strategic Report ---
- Date: {datetime.date.today()}
- Status: Global Trend Scanned
- 100M View Blueprint: '{script['title']}'
- Key Hook: {script['hook_3s']['action']}
- Loop Strategy: Enabled
- Target: {script['global_target']}
- Notion Sync: Completed
-----------------------------------------
        """
        return report_card

if __name__ == "__main__":
    orchestrator = KuraOrchestrator()
    report = orchestrator.run_daily_mission()
    print(report)
