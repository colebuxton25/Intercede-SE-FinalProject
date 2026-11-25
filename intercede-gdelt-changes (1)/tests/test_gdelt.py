import pytest
from app.news.gdelt import GdeltNews, GdeltError, URL

SAMPLE = {"articles": [
    {"url": "https://a.example/1", "title": " Riots in Paris suburbs ", "domain": "a.example", "seendate": "20261117T090000Z"},
    {"url": "", "title": "No url", "domain": "b.example", "seendate": "20261117T090000Z"},
    {"url": "https://c.example/3", "title": "", "domain": "c.example", "seendate": "20261117T090000Z"},
]}


class FakeResp:
    def __init__(self, payload=None, bad_json=False):
        self.payload, self.bad_json = payload, bad_json

    def raise_for_status(self):
        pass

    def json(self):
        if self.bad_json:
            raise ValueError("not json")
        return self.payload


class FakeSession:
    def __init__(self, resp):
        self.resp, self.calls = resp, []

    def get(self, url, params=None, timeout=None):
        self.calls.append((url, params))
        return self.resp


def make(resp, **kw):
    t = {"now": 0.0}
    sleeps = []
    g = GdeltNews(session=FakeSession(resp), clock=lambda: t["now"],
                  sleep=lambda s: sleeps.append(s), **kw)
    return g, t, sleeps


def test_parses_articles_and_skips_incomplete_ones():
    g, _, _ = make(FakeResp(SAMPLE))
    out = g.fetch_stories("Paris", "France")
    assert [s.title for s in out] == ["Riots in Paris suburbs"]
    assert out[0].source == "a.example" and out[0].url == "https://a.example/1"


def test_query_uses_city_and_documented_parameters():
    g, _, _ = make(FakeResp(SAMPLE))
    g.fetch_stories("Paris", "France")
    url, params = g.session.calls[0]
    assert url == URL and '"Paris"' in params["query"]
    assert params["mode"] == "artlist" and params["format"] == "json"


def test_repeat_request_is_served_from_cache():
    g, t, _ = make(FakeResp(SAMPLE))
    g.fetch_stories("Paris", "France")
    t["now"] = 60
    g.fetch_stories("Paris", "France")
    assert len(g.session.calls) == 1


def test_requests_are_spaced_out():
    g, t, sleeps = make(FakeResp(SAMPLE))
    g.fetch_stories("Paris", "France")
    t["now"] = 1.0
    g.fetch_stories("London", "UK")
    assert sleeps and sleeps[0] == pytest.approx(4.0)


def test_non_json_response_becomes_gdelt_error():
    g, _, _ = make(FakeResp(bad_json=True))
    with pytest.raises(GdeltError):
        g.fetch_stories("Paris", "France")
