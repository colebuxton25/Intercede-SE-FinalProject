"""No-AI summarizer: fixed prayer points per category. Also the fallback."""
from .base import Summarizer

POINTS = {
    "unrest": [
        "For peace in the streets and safety for everyone caught in the unrest.",
        "For the injured, and for families whose homes or livelihoods are at risk.",
        "For wisdom for leaders and for local churches to be a calm, loving presence.",
    ],
    "persecution": [
        "For protection and courage for believers who are being targeted.",
        "For those who have been harmed, and for their families.",
        "For hearts of persecutors to be changed, and for justice and religious freedom.",
    ],
    "disaster": [
        "For the safety of those affected and for the work of rescuers.",
        "For comfort for the grieving and care for the displaced.",
        "For provision, rebuilding, and for the church to serve its neighbours.",
    ],
}


class TemplateSummarizer(Summarizer):
    def summarize(self, story, category):
        return story.title, list(POINTS[category])
