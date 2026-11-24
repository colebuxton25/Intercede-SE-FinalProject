from app import create_app
from app.news.base import NewsProvider


def client():
    return create_app().test_client()


def test_paris_returns_relevant_deduped_stories():
    data = client().get("/api/stories?city=Paris&country=France").get_json()
    assert len(data) == 3                       # duplicate and sports story removed
    assert {s["category"] for s in data} == {"unrest", "persecution", "disaster"}
    assert all(len(s["prayer_points"]) == 3 and s["url"] for s in data)


def test_missing_city_is_400():
    assert client().get("/api/stories").status_code == 400


def test_news_failure_gives_friendly_error():
    class Down(NewsProvider):
        def fetch_stories(self, city, country):
            raise ConnectionError()
    resp = create_app(news=Down()).test_client().get("/api/stories?city=Paris")
    assert resp.status_code == 502 and "unavailable" in resp.get_json()["error"]


def test_home_page_loads():
    assert client().get("/").status_code == 200
