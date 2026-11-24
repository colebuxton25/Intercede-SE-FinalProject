"""Shared data shapes. Keep these small: every module depends on them."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
import hashlib


@dataclass
class RawStory:
    title: str
    url: str
    source: str
    published_at: str = ""
    text: str | None = None

    @property
    def id(self) -> str:
        return hashlib.sha1(self.url.encode()).hexdigest()[:12]


@dataclass
class Story:
    id: str
    title: str
    url: str
    source: str
    category: str
    summary: str
    prayer_points: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)
