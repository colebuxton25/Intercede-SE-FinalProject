class Summarizer:
    """Seam: the only module that may talk to an AI model."""

    def summarize(self, story, category: str) -> tuple[str, list[str]]:
        """Return (summary, exactly three prayer points)."""
        raise NotImplementedError
