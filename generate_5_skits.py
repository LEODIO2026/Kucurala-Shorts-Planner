from main import KuraOrchestrator
from script_architect import ScriptArchitect
import datetime

def run_5_missions():
    """5가지 고효율 바이럴 콘텐츠를 연속 기획하고 리토팅합니다."""
    orchestrator = KuraOrchestrator()
    # 장르별 5대 핵심 주제 선정
    missions = [
        {"topic": "엄마의 소리 없는 눈빛", "genre": "가족"},
        {"topic": "눈치 없는 친구의 조언", "genre": "친구"},
        {"topic": "배터리 1%의 극한 상황", "genre": "일상"},
        {"topic": "남친의 후드티 실종 사건", "genre": "커플"},
        {"topic": "택배 상자의 반전", "genre": "일상"}
    ]
    
    print(f"[{datetime.datetime.now()}] 에이전트 쿠라: v2.0 지능형 글로벌 숏츠 배치 실행...\n")
    
    for i, mission in enumerate(missions, 1):
        print(f"--- [기획안 #{i}: {mission['genre']}] ---")
        script = orchestrator.architect.generate_viral_skit_script(
            topic=mission['topic'], 
            genre=mission['genre']
        )
        orchestrator.automator.push_script_to_notion(script)
        print("-" * 30 + "\n")

if __name__ == "__main__":
    run_5_missions()
