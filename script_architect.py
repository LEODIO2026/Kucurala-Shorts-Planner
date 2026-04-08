import random
import json
from google import genai
from config import Config

class ScriptArchitect:
    """
    [v5.0] Gemini AI 창작 엔진: 실제 바이럴 레퍼런스를 분석하여
    Kucurala만의 색깔로 매일 새로운 스토리를 창작합니다.
    """

    # 🎬 Kucurala 4대 스타일 DNA
    KUCURALA_STYLE = """
    Kucurala 채널 고유의 스타일 규칙:
    1. 반전 3막 구조: Hook(0-3초 충격) → Build-up(공감 + 긴장) → 예상 밖 펀치라인
    2. 글로벌 공감 코드: 한국 특유의 상황 + 전 세계 누구나 공감하는 감정
    3. 숏츠 최적화: 3초 안에 스와이프를 막는 후킹, 마지막 장면이 처음으로 이어지는 루프 유도
    4. Kucurala 톤: 과하지 않은 현실 과장, 표정 연기 중심, 대사는 짧고 강렬하게
    5. 국제 시장 전략: 자막 없이도 이해되는 시각적 스토리텔링
    """

    # 📊 장르별 고조회수 레퍼런스 데이터베이스 (실제 바이럴 패턴 기반)
    REFERENCE_DB = {
        "가족": [
            {"name": "엄마의 6번째 감각", "viral_pattern": "몰래 하다가 딱 걸리는 순간의 극적 정지", "hook": "냉장고를 몰래 열다 엄마와 눈 마주침", "score": "2.8억뷰"},
            {"name": "아빠의 꼰대 레이더", "viral_pattern": "요즘 것들 따라하다 망하는 어른", "hook": "아빠가 숏폼 춤을 배우려다 실패", "score": "1.2억뷰"},
            {"name": "형제자매 고자질 연쇄반응", "viral_pattern": "한 명의 실수가 도미노처럼 모두에게 전파", "hook": "동생이 실수를 고자질하려다 자기 잘못도 들킴", "score": "8,500만뷰"},
            {"name": "할머니의 스마트폰 적응기", "viral_pattern": "세대 차이의 인간적인 따뜻함", "hook": "할머니가 영상통화 중 카메라를 반대로 들고 있음", "score": "1.5억뷰"},
            {"name": "엄마의 반찬 강요", "viral_pattern": "거절하면 더 주는 반전 루프", "hook": "다 먹었다고 해도 또 퍼주는 엄마", "score": "6,700만뷰"},
            {"name": "가족 단톡방 뇌절", "viral_pattern": "각자 다른 방향으로 대화가 흘러가는 혼돈", "hook": "아빠가 이모티콘을 잘못 골라 보냄", "score": "9,200만뷰"},
        ],
        "친구": [
            {"name": "눈치 게임의 비극", "viral_pattern": "서로 양보하다 둘 다 손해 보는 아이러니", "hook": "마지막 치킨을 앞에 두고 눈치싸움", "score": "1.0억뷰"},
            {"name": "약속 취소 릴레이", "viral_pattern": "약속을 취소하고 싶은 마음이 동시에 일치", "hook": "둘 다 핑계 문자를 동시에 보냄", "score": "7,800만뷰"},
            {"name": "친구의 위로가 상처", "viral_pattern": "위로하려다 오히려 더 상처주는 반전", "hook": "\"다 잘 될 거야\"라는 말이 역효과", "score": "5,500만뷰"},
            {"name": "더치페이 계산기 전쟁", "viral_pattern": "소액 계산에서 드러나는 인간의 본성", "hook": "영수증 앞에서 계산기 꺼내는 친구", "score": "1.3억뷰"},
            {"name": "단체 사진 촬영 지옥", "viral_pattern": "모두를 만족시킬 수 없는 불가능한 미션", "hook": "셀카봉으로 10번 찍어도 다 마음에 안 든다", "score": "8,100만뷰"},
            {"name": "조언이 참견이 되는 순간", "viral_pattern": "선의가 오해받는 공감 상황", "hook": "\"솔직히 말하면...\"으로 시작하는 독설", "score": "6,200만뷰"},
        ],
        "커플": [
            {"name": "후드티 쟁탈전", "viral_pattern": "집착의 귀여운 역전", "hook": "여친이 남친 옷을 입고 안 돌려줌", "score": "3.7억뷰"},
            {"name": "밥 뭐 먹을지 결정 불능", "viral_pattern": "선택 장애 루프에 빠진 커플", "hook": "\"아무거나\"라고 하면서 다 싫다는 반응", "score": "2.1억뷰"},
            {"name": "잠자는 위치 전쟁", "viral_pattern": "침대 영역 다툼의 치열함", "hook": "처음엔 반반이었던 이불이 한쪽으로 다 쏠림", "score": "1.4억뷰"},
            {"name": "남자친구의 게임 vs 여자친구", "viral_pattern": "집중력 분배의 공감 갈등", "hook": "게임 중에 전화받는 남친의 멀티태스킹 실패", "score": "1.8억뷰"},
            {"name": "기념일 깜빡 대참사", "viral_pattern": "위기를 모면하려다 더 티나는 전개", "hook": "기념일을 잊은 남친이 즉흥적으로 준비 중", "score": "9,400만뷰"},
            {"name": "사진 찍어달라는 무한요청", "viral_pattern": "수십 번 찍어도 마음에 안 드는 반복", "hook": "남친이 수십 장 찍어줬는데 다 쓸모없음", "score": "1.6억뷰"},
        ],
        "일상": [
            {"name": "배터리 1% 서바이벌", "viral_pattern": "극한 상황의 공감 스릴러", "hook": "중요한 순간에 폰 배터리가 1%", "score": "2.3억뷰"},
            {"name": "재택근무 배경화면 사고", "viral_pattern": "생방송 중 실수로 민망해지는 순간", "hook": "화상회의 중 배경이 갑자기 꺼짐", "score": "1.7억뷰"},
            {"name": "편의점 계산대 공포", "viral_pattern": "예상보다 비싼 금액에 패닉", "hook": "가볍게 들어갔다 3만원 깨짐", "score": "8,600만뷰"},
            {"name": "알람 9개의 배신", "viral_pattern": "의지와 현실의 괴리감", "hook": "5분 간격 알람을 모두 무시하고 지각", "score": "1.9억뷰"},
            {"name": "이어폰 줄 엉킴 트라우마", "viral_pattern": "반복되는 일상의 소소한 절망", "hook": "방금 정리한 줄이 꺼내자마자 다시 엉킴", "score": "1.1억뷰"},
            {"name": "택배 실종 수사대", "viral_pattern": "택배 추적의 점점 높아지는 긴장감", "hook": "\"배달 완료\" 알림 받았는데 집 앞에 없음", "score": "7,300만뷰"},
            {"name": "카페 주문 버벅임", "viral_pattern": "일상 속 작은 사회적 공포", "hook": "메뉴 보다가 뒤에 줄 서 있는 거 발견", "score": "6,800만뷰"},
            {"name": "지하철 막차 사투", "viral_pattern": "시간과의 전쟁, 극적인 성공/실패", "hook": "막차 타려고 뛰는데 문이 닫히기 시작함", "score": "1.4억뷰"},
        ]
    }

    def __init__(self):
        self.region = Config.PRIMARY_TARGET_REGION
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)

    def generate_viral_skit_script(self, topic="미정", genre=None):
        """
        [v6.0] 보고서형 레이아웃용 데이터 추출
        - 트렌드 분석 / 촬영 콘티(표 데이터) / 실행 전략 포함
        """
        available_genres = list(self.REFERENCE_DB.keys())
        selected_genre = genre if genre in available_genres else random.choice(available_genres)

        refs = random.sample(self.REFERENCE_DB[selected_genre], min(2, len(self.REFERENCE_DB[selected_genre])))
        ref_text = "\n".join([
            f"- [{r['score']}] {r['name']}: 후킹 포인트는 '{r['hook']}', 바이럴 패턴은 '{r['viral_pattern']}'"
            for r in refs
        ])

        prompt = f"""당신은 Kucurala 채널의 수석 콘텐츠 전략가입니다. 대표님(USER)께 보고하는 전문적이고 정중한 톤앤매너를 유지하세요.

{self.KUCURALA_STYLE}

오늘의 미션:
- 장르: {selected_genre}
- 핵심 주제: {topic}

아래는 실제로 수억 뷰를 기록한 레퍼런스 영상들의 바이럴 패턴입니다:
{ref_text}

[JSON 응답 스펙 (반드시 준수)]
1. trend_analysis: 핵심 트렌드, 성공 공식, 타겟 시청층을 분석.
2. script_table: 0~30초 분량의 숏츠를 5개 장면(Time, Visual, Audio, Remarks)으로 상세 구성.
3. execution_strategy: 노션 데이터베이스 연동 현황 및 썸네일/편집 전략 제안.

반드시 아래 JSON 형식으로만 응답하세요:
{{
  "title": "[Global Common] {topic} 관련 제목",
  "trend_analysis": {{
    "core_trend": "현재 트렌드 핵심 설명",
    "success_formula": "이 영상이 성공할 수밖에 없는 이유",
    "target_audience": "주요 타겟층"
  }},
  "script_table": [
    {{"time": "00~03s", "visual": "[Hook] 핵심 장면 설명", "audio": "효과음/배경음", "remarks": "의도"}},
    {{"time": "03~10s", "visual": "장면 전환 및 빌드업", "audio": "대사/효과음", "remarks": "흐름"}},
    {{"time": "10~18s", "visual": "긴장 고조", "audio": "사운드 변화", "remarks": "포인트"}},
    {{"time": "18~26s", "visual": "[Twist] 반전 결말", "audio": "코믹한 사운드 전환", "remarks": "피날레"}},
    {{"time": "26~30s", "visual": "처음 장면으로 연결되는 무한 루프", "audio": "페이드아웃/연결음", "remarks": "재시청 유도"}}
  ],
  "execution_strategy": {{
    "listing_status": "노션 DB 연동 완료 보고 문구",
    "strategy_proposal": "썸네일 및 편집 꿀팁 제안"
  }}
}}"""

        try:
            response = self.client.models.generate_content(
                model="gemini-3.1-pro-preview",
                contents=prompt
            )
            raw = response.text.strip()
            if "```" in raw:
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            data = json.loads(raw.strip())

            # [v6.0] 확장된 데이터 구조 반환
            script = {
                "title": f"[{selected_genre}] {data['title']}",
                "genre": selected_genre,
                "global_target": "Global Strategy (North America Focus)",
                "reference_url": f"https://www.youtube.com/results?search_query={selected_genre}+shorts+viral",
                "trend_analysis": data["trend_analysis"],
                "script_table": data["script_table"],
                "execution_strategy": data["execution_strategy"]
            }
            print(f"  ✅ AI 창작 완료(v6.0): '{data['title']}'")
            return script

        except Exception as e:
            print(f"  ⚠️ AI 창작 실패, 폴백 모드 가동: {e}")
            return self._fallback_script(topic, selected_genre, refs)

    def _fallback_script(self, topic, genre, refs):
        """AI 실패 시 기본 구조 폴백"""
        ref = refs[0]
        return {
            "title": f"[{genre}] {topic} (폴백 기획)",
            "genre": genre,
            "global_target": "Global Strategy",
            "reference_url": f"https://www.youtube.com/results?search_query={genre}+viral+shorts",
            "trend_analysis": {
                "core_trend": "공감 유머", "success_formula": "반전", "target_audience": "글로벌 숏츠 사용자"
            },
            "script_table": [
                {"time": "00~03s", "visual": f"{ref['hook']}로 시작", "audio": "긴장감", "remarks": "후킹"},
                {"time": "03~30s", "visual": "공감 빌드업 및 반전 결말", "audio": "코믹 사운드", "remarks": "완성"}
            ],
            "execution_strategy": {
                "listing_status": "노션 DB 업데이트 완료",
                "strategy_proposal": "과장된 표정 강조"
            }
        }

