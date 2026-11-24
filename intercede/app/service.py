"""Orchestrator. Receives its collaborators as arguments (dependency injection)."""
from .categorizer import categorize, dedupe
from .models import Story
from .summarizer.template import TemplateSummarizer

_fallback = TemplateSummarizer()


def get_stories(city, country, news, summarizer, cache):
    raw = dedupe(news.fetch_stories(city, country))
    stories = []
    for r in raw:
        category = categorize(r)
        if category is None:
            continue
        cached = cache.get(r.id)
        if cached:
            stories.append(cached)
            continue
        try:
            summary, points = summarizer.summarize(r, category)
        except Exception:
            summary, points = _fallback.summarize(r, category)
        story = Story(r.id, r.title, r.url, r.source, category, summary, points)
        cache.set(r.id, story)
        stories.append(story)
    return stories
