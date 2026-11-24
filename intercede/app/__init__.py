import os
from flask import Flask
from .cache import Cache
from .routes import bp
from .summarizer.template import TemplateSummarizer


def create_app(news=None, summarizer=None):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    if news is None:
        if os.environ.get("NEWS_PROVIDER", "fixture") == "gdelt":
            from .news.gdelt import GdeltNews
            news = GdeltNews()
        else:
            from .news.fixture import FixtureNews
            news = FixtureNews()
    app.config.update(NEWS=news, SUMMARIZER=summarizer or TemplateSummarizer(), CACHE=Cache())
    app.register_blueprint(bp)
    return app
