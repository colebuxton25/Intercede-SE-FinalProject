"""GDELT DOC 2.0 adapter. Not exercised in the offline tests."""
import requests
from .base import NewsProvider
from ..models import RawStory

URL = "https://api.gdeltproject.org/api/v2/doc/doc"
TERMS = "(riot OR protest OR unrest OR persecution OR flood OR earthquake OR wildfire)"


class GdeltNews(NewsProvider):
    def __init__(self, session=None, max_records=25):
        self.session = session or requests
        self.max_records = max_records

    def fetch_stories(self, city, country):
        params = {
            "query": f'"{city}" {TERMS}',
            "mode": "artlist",
            "format": "json",
            "maxrecords": self.max_records,
            "sort": "datedesc",
        }
        resp = self.session.get(URL, params=params, timeout=10)
        resp.raise_for_status()
        articles = resp.json().get("articles", [])
        return [RawStory(title=a.get("title", ""), url=a.get("url", ""),
                         source=a.get("domain", ""), published_at=a.get("seendate", ""))
                for a in articles if a.get("url")]
