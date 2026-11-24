from app.categorizer import categorize, dedupe
from app.models import RawStory


def story(title, url="u"):
    return RawStory(title=title, url=url, source="s")


def test_categorizes_unrest():
    assert categorize(story("Riots erupt in suburbs")) == "unrest"


def test_categorizes_disaster():
    assert categorize(story("Flood warning issued")) == "disaster"


def test_irrelevant_story_is_dropped():
    assert categorize(story("Local team wins match")) is None


def test_dedupe_by_title_and_url():
    items = [story("Same", "1"), story("same", "2"), story("Other", "1"), story("New", "3")]
    assert [s.url for s in dedupe(items)] == ["1", "3"]
