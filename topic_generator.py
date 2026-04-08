"""
[topic_generator.py] AI 기반 실시간 주제 생성기
실제로 수집된 트렌드 데이터를 Gemini AI가 분석하여
오늘 날짜에 최적화된 Kucurala 숏츠 주제 5개를 생성합니다.
"""

import json
import time
from google import genai
from config import Config
from trend_hacker import TrendHacker


KUCURALA_GENRES = ["가족", "친구", "커플", "일상"]

# Kucurala 채널 고유 스타일
CHANNEL_DNA = """
Kucurala 채널 정체성:
- 타겟: 10~30대 한국인 + 글로벌 (North America 1순위)
- 장르: 가족, 친구, 커플, 일상 코믹 상황극
- 핵심 공식: 3초 후킹 → 공감 빌드업 → 예상 밖 반전 펀치라인
- 톤: 현실 과장 코미디 (대사는 짧고 강렬, 표정 연기 중심)
- 절대 원칙: 자막 없이도 전 세계인이 이해할 수 있는 시각적 스토리텔링
"""


class TopicGenerator:
    """
    [v3.0] 실시간 트렌드 기반 AI 주제 생성기
    사전 정의된 목록이 아닌, 오늘의 실제 트렌드에서 주제를 뽑아냅니다.
    """

    def __init__(self):
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.hacker = TrendHacker()

    def _format_trends_for_prompt(self, trend_data: dict) -> str:
        """수집된 트렌드 데이터를 AI 프롬프트용 텍스트로 변환"""
        lines = []

        # trend_hacker v4.0: 값이 list 형태로 반환됨
        kr_kws = trend_data.get("google_trends_kr", [])
        us_kws = trend_data.get("google_trends_us", [])
        reddit_funny = trend_data.get("reddit_funny", [])
        reddit_korea = trend_data.get("reddit_korea", [])
        naver = trend_data.get("naver_news", [])

        if kr_kws:
            lines.append("【Google 급상승 검색어 - 한국 (실시간)】")
            lines.append(", ".join(kr_kws[:10]))

        if us_kws:
            lines.append("\n【Google 급상승 검색어 - 미국 (실시간)】")
            lines.append(", ".join(us_kws[:10]))

        if reddit_funny:
            lines.append("\n【Reddit r/funny 글로벌 유머 트렌딩 포스트】")
            for t in reddit_funny[:5]:
                lines.append(f"  - {t}")

        if reddit_korea:
            lines.append("\n【Reddit r/korea 한국 관련 해외 커뮤니티 트렌드】")
            for t in reddit_korea[:5]:
                lines.append(f"  - {t}")

        if naver:
            lines.append("\n【Naver 뉴스 헤드라인 (오늘 한국 주요 이슈)】")
            for t in naver[:5]:
                lines.append(f"  - {t}")

        return "\n".join(lines) if lines else "트렌드 데이터 수집 실패 (폴백 모드)"

    def generate_topics(self, trend_data: dict) -> list:
        """
        실제 트렌드 데이터를 Gemini에 넘겨 오늘의 최적 주제 5개를 생성합니다.
        반환 형식: [{"topic": str, "genre": str, "trend_reason": str}, ...]
        """
        trend_text = self._format_trends_for_prompt(trend_data)

        prompt = f"""당신은 Kucurala 채널의 수석 콘텐츠 전략가이자 데이터 분석가입니다.

{CHANNEL_DNA}

아래는 오늘 ({trend_data.get('date', '오늘')}) 실시간으로 수집한 트렌드 데이터입니다:

{trend_text}

[미션]
위 트렌드 데이터를 분석하여 Kucurala 채널에 최적화된 숏츠 주제 5개를 선정하세요.

선정 기준:
1. 트렌드 키워드와 연관성이 있거나, 트렌드에서 공감 감정을 추출해 활용
2. Kucurala 4대 장르(가족/친구/커플/일상) 중 최적 매칭
3. 오늘 한국 + 북미 시청자가 동시에 공감할 수 있는 보편적 상황
4. 3초 안에 후킹 가능한 시각적 아이디어가 있는 주제
5. 5개 중 장르가 다양하게 분산될 것 (같은 장르 최대 2개)

반드시 아래 JSON 배열 형식으로만 응답하세요 (설명 텍스트 없이):
[
  {{
    "topic": "구체적인 숏츠 주제명 (15자 이내, 호기심 유발)",
    "genre": "가족 또는 친구 또는 커플 또는 일상",
    "trend_reason": "이 트렌드 데이터에서 이 주제를 선택한 이유 한 줄"
  }},
  ...5개 총
]"""

        print("  🤖 Gemini AI 트렌드 분석 + 주제 생성 중...")
        try:
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            raw = response.text.strip()

            # JSON 파싱 (마크다운 코드블록 제거)
            if "```" in raw:
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]

            topics = json.loads(raw.strip())

            # 유효성 검증
            valid_topics = []
            for t in topics:
                if isinstance(t, dict) and "topic" in t and "genre" in t:
                    genre = t["genre"] if t["genre"] in KUCURALA_GENRES else "일상"
                    valid_topics.append({
                        "topic": t["topic"],
                        "genre": genre,
                        "trend_reason": t.get("trend_reason", "")
                    })
            if valid_topics:
                print(f"  ✅ AI 주제 {len(valid_topics)}개 생성 완료!")
                return valid_topics[:5]
            else:
                raise ValueError("유효한 주제 없음")

        except Exception as e:
            print(f"  ⚠️ AI 주제 생성 실패, 기본 검색어 기반 폴백 사용: {e}")
            return self._fallback_topics(trend_data)

    def _fallback_topics(self, trend_data: dict) -> list:
        """AI 실패 시 수집된 키워드를 기반으로 기본 주제 생성"""
        # trend_hacker v4.0: list 형태로 반환
        kr_kws = trend_data.get("google_trends_kr", [])

        genres = ["가족", "친구", "일상", "커플", "일상"]
        fallback = []
        for i, genre in enumerate(genres):
            signal = kr_kws[i] if i < len(kr_kws) else f"오늘의 {genre} 상황"
            fallback.append({
                "topic": f"{str(signal)[:10]} 공감 상황",
                "genre": genre,
                "trend_reason": f"AI 실패로 실시간 트렌드 키워드 직접 활용: {signal}"
            })
        return fallback


def pick_daily_missions(trend_data: dict = None) -> list:
    """
    실시간 트렌드 수집 → AI 분석 → 오늘 최적 미션 5개 반환
    generate_5_skits.py 및 main.py에서 호출되는 통합 인터페이스
    """
    generator = TopicGenerator()

    # 트렌드 데이터가 없으면 직접 수집
    if trend_data is None:
        trend_data = generator.hacker.collect_all_trends()

    missions = generator.generate_topics(trend_data)
    return missions, trend_data  # trend_data도 함께 반환 (script_architect에서 활용 가능)


if __name__ == "__main__":
    print("=== Kucurala 실시간 트렌드 분석 테스트 ===\n")
    missions, trend_data = pick_daily_missions()

    print("\n📋 오늘의 AI 선정 미션:")
    for i, m in enumerate(missions, 1):
        print(f"  #{i} [{m['genre']}] {m['topic']}")
        print(f"       └ 이유: {m['trend_reason']}")
