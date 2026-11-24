from ..models import RawStory


class NewsProvider:
    """Seam: the rest of the app only calls fetch_stories()."""

    def fetch_stories(self, city: str, country: str) -> list[RawStory]:
        raise NotImplementedError
