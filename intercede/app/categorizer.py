"""Decides whether a story deserves prayer and which category it falls in."""
from __future__ import annotations

from .models import RawStory

KEYWORDS = {
    "unrest": ["riot", "protest", "clash", "unrest", "tear gas", "looting"],
    "persecution": ["persecut", "church attack", "church arson", "blasphemy",
                    "christians killed", "religious freedom", "threat to church"],
    "disaster": ["flood", "earthquake", "wildfire", "storm", "hurricane",
                 "explosion", "famine", "evacuat"],
}


def categorize(story: RawStory) -> str | None:
    """Return a category name, or None if the story should be dropped."""
    text = f"{story.title} {story.text or ''}".lower()
    for category, words in KEYWORDS.items():
        if any(w in text for w in words):
            return category
    return None


def dedupe(stories: list) -> list:
    """Drop stories with the same URL or the same lower-cased title."""
    seen, out = set(), []
    for s in stories:
        keys = {s.url, s.title.strip().lower()}
        if keys & seen:
            continue
        seen |= keys
        out.append(s)
    return out
