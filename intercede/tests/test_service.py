from app.cache import Cache
from app.models import RawStory
from app.news.base import NewsProvider
from app.service import get_stories
from app.summarizer.base import Summarizer


class FakeNews(NewsProvider):
    def fetch_stories(self, city, country):
        return [RawStory("Riots in town", "u1", "s"), RawStory("Cake recipe", "u2", "s")]


class CountingSummarizer(Summarizer):
    calls = 0

    def summarize(self, story, category):
        CountingSummarizer.calls += 1
        return "sum", ["a", "b", "c"]


class BrokenSummarizer(Summarizer):
    def summarize(self, story, category):
        raise RuntimeError("model down")


def test_filters_and_summarizes():
    out = get_stories("X", "Y", FakeNews(), CountingSummarizer(), Cache())
    assert len(out) == 1 and out[0].category == "unrest" and out[0].summary == "sum"


def test_summary_is_cached():
    CountingSummarizer.calls = 0
    cache = Cache()
    get_stories("X", "Y", FakeNews(), CountingSummarizer(), cache)
    get_stories("X", "Y", FakeNews(), CountingSummarizer(), cache)
    assert CountingSummarizer.calls == 1


def test_falls_back_when_summarizer_fails():
    out = get_stories("X", "Y", FakeNews(), BrokenSummarizer(), Cache())
    assert len(out) == 1 and len(out[0].prayer_points) == 3
