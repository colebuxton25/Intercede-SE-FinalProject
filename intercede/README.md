# Intercede (walking skeleton)

News stories from a chosen city that deserve prayer, with prayer points and a saved prayer list.

## Run
    python -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    flask --app app run          # then open http://127.0.0.1:5000

By default the app reads saved sample data (offline). For live news:
    NEWS_PROVIDER=gdelt flask --app app run
(The GDELT adapter is written against GDELT's documented DOC 2.0 API but is not covered by automated tests.)

## Test
    pytest

## Structure
- `app/news/` news providers behind one interface (`fetch_stories`)
- `app/categorizer.py` relevance filter and dedupe
- `app/summarizer/` summarizers behind one interface (template now; an AI adapter plugs in here)
- `app/service.py` orchestrator; `app/routes.py` the API
- `static/app.js` frontend and local-storage prayer list
