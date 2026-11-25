"""GDELT DOC 2.0 adapter.

Written against GDELT's documented DOC 2.0 API (artlist mode, JSON). Behaviours
this adapter handles because the service needs them:
  * GDELT asks for roughly one request per 5 seconds -> spaced out here.
  * Repeat page loads should not hit GDELT again -> short in-memory cache.
  * Bad queries can come back as plain text, not JSON -> turned into GdeltError.
"""
import time
import requests
from .base import NewsProvider
from ..models import RawStory

URL = "https://api.gdeltproject.org/api/v2/doc/doc"
TERMS = "(riot OR protest OR unrest OR persecution OR flood OR earthquake OR wildfire)"


class GdeltError(RuntimeError):
    pass


class GdeltNews(NewsProvider):
    def __init__(self, session=None, max_records=25, timespan="7d",
                 min_interval=5.0, cache_ttl=600,
                 clock=time.monotonic, sleep=time.sleep):
        self.session = session or requests
        self.max_records = max_records
        self.timespan = timespan
        self.min_interval = min_interval
        self.cache_ttl = cache_ttl
        self.clock, self.sleep = clock, sleep
        self._last_call = None
        self._cache = {}

    def build_params(self, city):
        return {
            "query": f'"{city}" {TERMS}',
            "mode": "artlist",
            "format": "json",
            "maxrecords": self.max_records,
            "sort": "datedesc",
            "timespan": self.timespan,
        }

    def fetch_stories(self, city, country):
        key = (city.lower(), country.lower())
        now = self.clock()
        hit = self._cache.get(key)
        if hit and now - hit[0] < self.cache_ttl:
            return list(hit[1])

        if self._last_call is not None:
            wait = self.min_interval - (now - self._last_call)
            if wait > 0:
                self.sleep(wait)
        self._last_call = self.clock()

        try:
            resp = self.session.get(URL, params=self.build_params(city), timeout=10)
            resp.raise_for_status()
            payload = resp.json()
        except ValueError as e:
            raise GdeltError("GDELT returned a non-JSON response") from e
        except Exception as e:
            raise GdeltError("Could not reach GDELT") from e

        stories = [
            RawStory(title=a.get("title", "").strip(), url=a["url"],
                     source=a.get("domain", ""), published_at=a.get("seendate", ""))
            for a in payload.get("articles", []) if a.get("url") and a.get("title")
        ]
        self._cache[key] = (self.clock(), stories)
        return list(stories)
