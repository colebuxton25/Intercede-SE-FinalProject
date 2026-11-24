class Cache:
    """In-memory cache so each story is summarized once."""

    def __init__(self):
        self._items = {}

    def get(self, story_id):
        return self._items.get(story_id)

    def set(self, story_id, story):
        self._items[story_id] = story
