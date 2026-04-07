from main import KuraOrchestrator
import datetime

def push_special_3_1_script():
    """
    Gemini 3.1 Pro Preview가 설계한 '전설적 기획안'을 노션에 즉시 고정합니다.
    """
    orchestrator = KuraOrchestrator()
    
    special_script = {
        "title": "[Gemini 3.1 Pro] 전설의 시작: 사회적 미소의 유통기한 (The Expiration of a Fake Smile)",
        "genre": "글로벌 일상 (Universal Daily)",
        "global_target": "Global (Top Tier Viral Logic)",
        "hook_3s": {
            "action": "[POV] 초근접 클로즈업. 억지로 만든 '자본주의 미소'와 파들거리는 입꼬리.",
            "visual_text": "전 세계 직장인 공감 😱"
        },
        "body_60s": [
            "1. 상황: 상대방의 재미없는 농담에 5초간 억지 미소 유지 (긴장감 증폭)",
            "2. 대화: 무의미한 리액션 '아 진짜요?' 반복",
            "3. 연출: 배경음이 잦아들며 째깍째깍 시계 소리만 강조",
            "4. 펀치라인: 상대가 뒤돌자마자 0.1초 만에 무표정 복구 (가면 벗기)"
        ],
        "ending_loop": {
            "action": "상대가 다시 돌아보자 기계적인 미소가 다시 장착되며 첫 장면 연결.",
            "loop_logic": "무한 반복되는 사회 생활의 굴레 형상화"
        },
        "filming_guide": {
            "lighting": "대조를 극대화하는 스포트라이트 조명",
            "editing": "미소가 무너지는 순간 0.1초 컷으로 카타르시스 부여"
        }
    }

    print("[ACTION] Gemini 3.1 Pro 전용 마스터피스 대본 전송 시작...")
    orchestrator.automator.push_script_to_notion(special_script)
    print("[SUCCESS] 대표님의 노션에 100M 전술 대본이 '고정'되었습니다.")

if __name__ == "__main__":
    push_special_3_1_script()
