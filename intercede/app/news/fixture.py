"""Offline provider that reads saved sample data. Used for demos and tests."""
import json
from pathlib import Path
from .base import NewsProvider
from ..models import RawStory

DEFAULT = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "sample_news.json"


class FixtureNews(NewsProvider):
    def __init__(self, path=DEFAULT):
        self.path = Path(path)

    def fetch_stories(self, city, country):
        data = json.loads(self.path.read_text())
        return [RawStory(**item) for item in data.get(city, [])]
