"""
[trend_hacker.py v4.0] 실제 작동하는 실시간 트렌드 수집기
- Google Trends 실시간 RSS (한국 + 미국): 실시간 급상승 검색어
- Naver 검색 트렌드 RSS: 한국 뉴스/이슈 키워드
- 수집한 원시 데이터를 구조화하여 Gemini AI 분석 재료로 반환
"""

import feedparser
import requests
import datetime
import time


class TrendHacker:
    """
    [v4.0] 실제 작동하는 실시간 트렌드 수집 엔진
    Google Trends 공식 RSS 피드를 통해 진짜 실시간 데이터를 수집합니다.
    """

    # ✅ 실제 작동이 확인된 데이터 소스
    SOURCES = {
        "google_trends_kr": "https://trends.google.com/trending/rss?geo=KR",
        "google_trends_us": "https://trends.google.com/trending/rss?geo=US",
        "naver_news":       "https://news.naver.com/main/rss/opinion.naver",
        "reddit_funny":     "https://www.reddit.com/r/funny/.rss",
        "reddit_korea":     "https://www.reddit.com/r/korea/.rss",
    }

    def __init__(self):
        self.today = datetime.date.today()
        self.headers = {"User-Agent": "Mozilla/5.0 (compatible; KucuralaBot/1.0)"}

    def fetch_google_trends_rss(self, geo: str) -> list:
        """
        Google Trends 공식 RSS에서 실시간 급상승 검색어를 수집합니다.
        geo: 'KR' (한국), 'US' (미국)
        """
        url = f"https://trends.google.com/trending/rss?geo={geo}"
        print(f"  📡 Google Trends RSS 수집 중... [geo={geo}]")
        try:
            feed = feedparser.parse(url)
            keywords = [entry.title for entry in feed.entries if entry.title]
            print(f"     → {len(keywords)}개 수집: {', '.join(keywords[:5])}{'...' if len(keywords) > 5 else ''}")
            return keywords
        except Exception as e:
            print(f"  ⚠️ Google Trends [{geo}] 실패: {e}")
            return []

    def fetch_reddit_trending(self, subreddit: str) -> list:
        """
        Reddit 공개 RSS에서 핫 포스트 제목을 수집합니다.
        영어권 트렌드 + 글로벌 공감 코드 파악용
        """
        url = f"https://www.reddit.com/r/{subreddit}/.rss"
        print(f"  📡 Reddit 트렌딩 수집 중... [r/{subreddit}]")
        try:
            feed = feedparser.parse(url)
            titles = [entry.title for entry in feed.entries[:10] if entry.title]
            print(f"     → {len(titles)}개 수집")
            return titles
        except Exception as e:
            print(f"  ⚠️ Reddit [{subreddit}] 실패: {e}")
            return []

    def fetch_naver_news_headlines(self) -> list:
        """
        네이버 뉴스 RSS에서 오늘의 주요 이슈 헤드라인을 수집합니다.
        한국 사회 현재 이슈 파악용
        """
        url = "https://news.naver.com/main/rss/opinion.naver"
        print(f"  📡 Naver 뉴스 헤드라인 수집 중...")
        try:
            feed = feedparser.parse(url)
            titles = [entry.title for entry in feed.entries[:10] if entry.title]
            print(f"     → {len(titles)}개 수집")
            return titles
        except Exception as e:
            print(f"  ⚠️ Naver 뉴스 실패: {e}")
            return []

    def collect_all_trends(self) -> dict:
        """
        모든 소스에서 실시간 트렌드 데이터를 수집하여 통합 보고서를 반환합니다.
        이 데이터가 Gemini AI의 주제 분석 재료가 됩니다.
        """
        print(f"\n🔍 [{self.today}] 실시간 트렌드 수집 시작...\n")

        result = {
            "date": self.today.isoformat(),
            "google_trends_kr": [],
            "google_trends_us": [],
            "reddit_funny": [],
            "reddit_korea": [],
            "naver_news": [],
        }

        # 1. Google Trends KR (핵심!)
        result["google_trends_kr"] = self.fetch_google_trends_rss("KR")
        time.sleep(1)

        # 2. Google Trends US (글로벌 공감 파악용)
        result["google_trends_us"] = self.fetch_google_trends_rss("US")
        time.sleep(1)

        # 3. Reddit 글로벌 유머 트렌드
        result["reddit_funny"] = self.fetch_reddit_trending("funny")
        time.sleep(0.5)

        # 4. Reddit 한국 커뮤니티
        result["reddit_korea"] = self.fetch_reddit_trending("korea")
        time.sleep(0.5)

        # 5. 네이버 뉴스 헤드라인
        result["naver_news"] = self.fetch_naver_news_headlines()

        # 수집 요약
        total = sum(len(v) for v in result.values() if isinstance(v, list))
        print(f"\n✅ 트렌드 수집 완료 — 총 {total}개 트렌드 신호")
        print(f"   Google Trends KR: {len(result['google_trends_kr'])}개")
        print(f"   Google Trends US: {len(result['google_trends_us'])}개")
        print(f"   Reddit r/funny: {len(result['reddit_funny'])}개")
        print(f"   Reddit r/korea: {len(result['reddit_korea'])}개")
        print(f"   Naver 뉴스: {len(result['naver_news'])}개\n")

        return result

    @staticmethod
    def get_latest_viral_patterns():
        """레거시 호환용"""
        return [
            {"name": "Visual Transformation", "viral_score": 9.9},
            {"name": "Deceptively Simple Fail", "viral_score": 9.7},
            {"name": "Frozen Comedy", "viral_score": 9.6},
            {"name": "Absurdist Chaos", "viral_score": 9.4},
        ]


if __name__ == "__main__":
    hacker = TrendHacker()
    data = hacker.collect_all_trends()

    print("\n=== 🔥 오늘 한국 실시간 트렌드 ===")
    for kw in data["google_trends_kr"]:
        print(f"  • {kw}")

    print("\n=== 🌍 오늘 미국 실시간 트렌드 ===")
    for kw in data["google_trends_us"][:5]:
        print(f"  • {kw}")
