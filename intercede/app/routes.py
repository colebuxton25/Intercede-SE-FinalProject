from flask import Blueprint, current_app, jsonify, render_template, request
from .service import get_stories

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return render_template("index.html")


@bp.get("/api/stories")
def stories():
    city = request.args.get("city", "").strip()
    country = request.args.get("country", "").strip()
    if not city:
        return jsonify(error="city is required"), 400
    cfg = current_app.config
    try:
        result = get_stories(city, country, cfg["NEWS"], cfg["SUMMARIZER"], cfg["CACHE"])
    except Exception:
        return jsonify(error="News source unavailable. Please try again later."), 502
    return jsonify([s.to_dict() for s in result])
