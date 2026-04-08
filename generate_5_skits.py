"""
[generate_5_skits.py v5.0]
실시간 트렌드 수집 → AI 주제 분석 → AI 스크립트 창작 → 노션 전송
완전 자동화 파이프라인
"""
import datetime
import time
from main import KuraOrchestrator
from topic_generator import pick_daily_missions


def run_5_missions():
    """
    실시간 트렌드를 분석하여 오늘의 5가지 바이럴 콘텐츠를 창작하고 노션에 전송합니다.
    """
    orchestrator = KuraOrchestrator()
    today = datetime.date.today().strftime("%Y년 %m월 %d일")

    print(f"{'='*50}")
    print(f"  🚀 에이전트 쿠라 v5.0 — {today}")
    print(f"  실시간 트렌드 분석 기반 AI 창작 엔진")
    print(f"{'='*50}\n")

    # 1단계: 실시간 트렌드 수집 + AI 주제 분석
    missions, trend_data = pick_daily_missions()

    print(f"\n📋 AI가 선정한 오늘의 미션 라인업:")
    for i, m in enumerate(missions, 1):
        print(f"   #{i} [{m['genre']}] {m['topic']}")
        if m.get("trend_reason"):
            print(f"       └ 트렌드 근거: {m['trend_reason']}")
    print()

    # 2단계: 각 주제로 AI 스크립트 창작 + 노션 전송
    success_count = 0
    for i, mission in enumerate(missions, 1):
        print(f"--- 🎬 스크립트 창작 #{i}: [{mission['genre']}] {mission['topic']} ---")
        script = orchestrator.architect.generate_viral_skit_script(
            topic=mission['topic'],
            genre=mission['genre']
        )
        result = orchestrator.automator.push_script_to_notion(script)
        if result:
            success_count += 1

        # API Rate Limit 방지 (Gemini 무료 티어: 분당 15회)
        if i < len(missions):
            print("  ⏳ API 레이트 리밋 대기 (5초)...")
            time.sleep(5)

        print("-" * 40 + "\n")

    print(f"{'='*50}")
    print(f"  ✅ 완료! {success_count}/{len(missions)} 기획안 노션 전송 성공")
    print(f"{'='*50}")


if __name__ == "__main__":
    run_5_missions()
