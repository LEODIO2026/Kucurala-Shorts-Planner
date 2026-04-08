"""
[main.py v5.0] KuraOrchestrator — 통합 제어 시스템
Cloud Run Job의 엔트리포인트이자 전체 파이프라인 관리자.
"""
import datetime
import time
from trend_hacker import TrendHacker
from script_architect import ScriptArchitect
from notion_automator import NotionAutomator
from topic_generator import pick_daily_missions


class KuraOrchestrator:
    """
    [v5.0] 실시간 트렌드 분석 → AI 주제 선정 → AI 스크립트 창작 → 노션 전송
    모든 단계가 실제 데이터와 AI 판단에 의해 동적으로 결정됩니다.
    """

    def __init__(self):
        self.hacker = TrendHacker()
        self.architect = ScriptArchitect()
        self.automator = NotionAutomator()

    def run_daily_mission(self):
        """
        Cloud Run Job에서 매일 실행되는 메인 파이프라인.
        1. 실시간 트렌드 수집 (Google Trends + YouTube RSS)
        2. Gemini AI가 트렌드 분석 → 오늘의 주제 5개 선정
        3. Gemini AI가 각 주제로 스크립트 창작
        4. 노션에 전송
        """
        today = datetime.date.today()
        print(f"[{datetime.datetime.now()}] 에이전트 쿠라 v5.0, 실시간 트렌드 분석 파이프라인 가동...")

        # 1. 트렌드 수집 + AI 주제 분석
        missions, trend_data = pick_daily_missions()

        print(f"\n📋 [{today}] AI 선정 미션 라인업:")
        for i, m in enumerate(missions, 1):
            print(f"   #{i} [{m['genre']}] {m['topic']}")
            if m.get("trend_reason"):
                print(f"       └ {m['trend_reason']}")
        print()

        # 2. AI 스크립트 창작 + 노션 전송
        success_count = 0
        scripts = []

        for i, mission in enumerate(missions, 1):
            print(f"--- 🎬 스크립트 #{i}: [{mission['genre']}] {mission['topic']} ---")
            script = self.architect.generate_viral_skit_script(
                topic=mission['topic'],
                genre=mission['genre']
            )
            result = self.automator.push_script_to_notion(script)
            if result:
                success_count += 1
            scripts.append(script)

            if i < len(missions):
                print("  ⏳ API 레이트 리밋 대기 (5초)...")
                time.sleep(5)
            print("-" * 40 + "\n")

        # 3. 리포트 카드 생성
        report_card = f"""
--- [kucurala v5.0] Daily Pipeline Report ---
- Date: {today}
- Trend Sources: Google Trends KR/US + YouTube KR/US
- AI Engine: Gemini 2.0 Flash (Topic Analysis + Script Creation)
- Scripts Generated: {len(scripts)}
- Notion Sync: {success_count}/{len(scripts)} completed
- Scripts:
"""
        for i, s in enumerate(scripts, 1):
            report_card += f"  #{i} {s['title']}\n"

        report_card += f"""- Next Run: {today + datetime.timedelta(days=1)} 09:00 KST
----------------------------------------------"""

        print(f"✅ 완료! {success_count}/{len(missions)} 기획안 노션 전송 성공")
        return report_card


if __name__ == "__main__":
    orchestrator = KuraOrchestrator()
    report = orchestrator.run_daily_mission()
    print(report)
