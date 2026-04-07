import random
from config import Config
from trend_hacker import TrendHacker

class ScriptArchitect:
    """
    [v2.0] Gemini 1.5 Pro 기반 고순도 대본 아키텍트
    커플, 일상, 친구, 가족 4대 장르별 최적화된 바이럴 블루프린트를 제공합니다.
    """

    def __init__(self):
        self.region = Config.PRIMARY_TARGET_REGION
        # 장르별 바이럴 블루프린트 데이터베이스 (Gemini 1.5 Pro 설계)
        self.blueprints = {
                "가족": [
                    {
                        "name": "엄마의 초능력 (The Super Mom Sense)",
                        "hook": "카메라가 몰래 간식을 먹으려는 자식의 뒷모습을 비춤. 0.5초 뒤, 뒤도 안 돌아본 엄마가 이름을 부름.",
                        "logic": "일상적인 마법 같은 순간에 대한 경외감과 공감 유도.",
                        "punchline": "자식이 '어떻게 알았어?'라고 묻자, 엄마가 천천히 고개를 돌리며 눈을 번뜩임."
                    },
                    {
                        "name": "아빠의 썰렁한 농담 (The Dad Joke Trap)",
                        "hook": "진지한 분위기에서 아빠가 아주 끔찍한 언어유희를 던짐. 사방이 정적에 휩싸임.",
                        "logic": "민망함(Cringe)을 통한 카타르시스 유도.",
                        "punchline": "무반응인 가족들 사이에서 아빠 혼자 숨 넘어가게 웃으며 루프 연결."
                    }
                ],
                "친구": [
                    {
                        "name": "현실 친구의 매운맛 (The Brutal Bestie)",
                        "hook": "인물 A가 한껏 멋을 내고 나타남. 인물 B(친구)가 0.1초 만에 팩트 폭격.",
                        "logic": "가식 없는 우정에 대한 전 세계적 공감.",
                        "punchline": "인물 A가 충격받은 표정으로 카메라를 응시하며 흑백 처리."
                    },
                    {
                        "name": "눈치 게임의 비극 (The Awkward Silence)",
                        "hook": "둘이서 마지막 남은 치킨 한 조각을 두고 눈치 싸움 시작. 긴장감 넘치는 BGM.",
                        "logic": "사소한 갈등의 극대화(Hyper-specific conflict).",
                        "punchline": "제 3자가 나타나 한 입에 먹어치우고 사라짐. 둘의 허망한 표정으로 루프."
                    }
                ],
                "일상": [
                    {
                        "name": "이어폰의 절망 (The No-Earphone Hell)",
                        "hook": "지하철에 앉아 이어폰을 끼려는 순간, 줄이 엉켜 있거나 배터리가 0%임.",
                        "logic": "현대인의 가장 보편적인 비극 형상화.",
                        "punchline": "주변 사람들의 시끄러운 소리가 증폭되며 인물의 얼굴이 붉어짐."
                    },
                    {
                        "name": "택배의 설레임 (The Delivery Dopamine)",
                        "hook": "문 밖에서 '택배요!' 소리가 들림. 인물이 빛 속도로 달려나감.",
                        "logic": "도파민 보상 심리 자극.",
                        "punchline": "상자를 열었는데 내가 주문한 게 아닌 다른 물건이 나옴. (예: 생수 24병)"
                    }
                ],
                "커플": [
                    {
                        "name": "후드티 쟁탈전 (The Hoodie Theft)",
                        "hook": "여친이 남친의 가장 아끼는 고가의 후드티를 입고 '예뻐?'라고 물음.",
                        "logic": "커플 간의 귀여운 권력 관계 묘사.",
                        "punchline": "남친이 '그건 안돼'라고 하려다 여친의 눈빛에 굴복하고 무릎 꿇음."
                    },
                    {
                        "name": "MBTI의 난 (The MBTI Clash)",
                        "hook": "영화 보고 감동받은 F 여친 vs 개연성 따지는 T 남친의 정면 충돌.",
                        "logic": "최신 트렌드 키워드 활용.",
                        "punchline": "결국 남친이 데이터를 들이밀지만 여친은 이미 차갑게 뒤 돌아섬."
                    }
                ]
        }

    def generate_viral_skit_script(self, topic="일상의 소리", genre=None):
        """
        Gemini 1.5 Pro의 지능적인 블루프린트를 기반으로 고퀄리티 대본을 생성합니다.
        """
        # 장르 자동 선택 (제공되지 않을 경우 랜덤)
        available_genres = list(self.blueprints.keys())
        selected_genre = genre if genre in available_genres else random.choice(available_genres)
        
        # 선택된 장르의 블루프린트 중 하나 선택
        blueprint = random.choice(self.blueprints[selected_genre])

        script = {
            "title": f"[{selected_genre}] {blueprint['name']} - {topic}",
            "genre": selected_genre,
            "global_target": "USA/Global (Universal Humor)",
            "hook_3s": {
                "action": blueprint['hook'],
                "visual_text": "절대 공감 😱" if selected_genre == "일상" else "현실 고증 100%"
            },
            "body_60s": [
                f"상황 설정: {topic}와 관련된 갈등 증폭.",
                f"바이럴 포인트: {blueprint['logic']}",
                "배우 표정: 0.5초 단위로 변하는 밈(Meme) 최적화 표정 연기.",
                "음향 가이드: 빠른 비트의 배경음과 임팩트 있는 리액션 효과음 삽입."
            ],
            "ending_loop": {
                "action": blueprint['punchline'],
                "loop_logic": "마지막 장면의 허무함이 첫 장면의 강렬함으로 자연스럽게 연결됨."
            },
            "filming_guide": {
                "lighting": "생동감 넘치는 하이라이트 위주 조명",
                "editing": "TikTok/Reels 스타일의 0.7초 컷 편집 가이드 적용"
            }
        }
        return script
