"""
AI-Based Sentiment Analysis of Customer Reviews
Backend : Python (Flask) + TextBlob
Frontend: HTML, CSS, JavaScript  (see static/index.html)

Architecture (three layers):
  1. Presentation Layer  -> static/index.html
  2. Application Layer   -> Flask routes in this file
  3. AI Processing Layer -> TextBlob sentiment analysis
"""

import re

from flask import Flask, jsonify, request, send_from_directory
from textblob import TextBlob

app = Flask(__name__, static_folder="static", static_url_path="/static")


# ---------------------------------------------------------------------------
# Text Processing Layer
# ---------------------------------------------------------------------------
def preprocess(text: str) -> str:
    """Clean the review: trim, collapse spaces, drop unusual special characters."""
    text = text.strip()
    # keep letters, digits, basic punctuation and apostrophes (needed for "don't")
    text = re.sub(r"[^\w\s.,!?'\-]", " ", text)
    # collapse multiple spaces / newlines into a single space
    text = re.sub(r"\s+", " ", text)
    return text


# ---------------------------------------------------------------------------
# AI & NLP Analysis + Sentiment Classification Layer
# ---------------------------------------------------------------------------
def analyze_sentiment(review: str) -> dict:
    cleaned = preprocess(review)

    analysis = TextBlob(cleaned)               # create TextBlob object
    polarity = analysis.sentiment.polarity     # -1.0 (negative) ... +1.0 (positive)
    subjectivity = analysis.sentiment.subjectivity  # 0.0 (factual) ... 1.0 (opinion)

    # Classification rule from the project report
    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "review": review,
        "cleaned_review": cleaned,
        "words": list(analysis.words),         # tokenization
        "polarity": round(polarity, 4),
        "subjectivity": round(subjectivity, 4),
        "sentiment": sentiment,
    }


# ---------------------------------------------------------------------------
# Routes (Application Layer)
# ---------------------------------------------------------------------------
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True) or {}
    review = (data.get("review") or "").strip()

    if not review:
        return jsonify({"error": "Please enter a customer review."}), 400

    return jsonify(analyze_sentiment(review))


@app.route("/analyze-bulk", methods=["POST"])
def analyze_bulk():
    """Analyse several reviews at once (one review per line)."""
    data = request.get_json(silent=True) or {}
    reviews = [r.strip() for r in data.get("reviews", []) if r and r.strip()]

    if not reviews:
        return jsonify({"error": "No reviews provided."}), 400

    results = [analyze_sentiment(r) for r in reviews]
    summary = {
        "Positive": sum(r["sentiment"] == "Positive" for r in results),
        "Negative": sum(r["sentiment"] == "Negative" for r in results),
        "Neutral": sum(r["sentiment"] == "Neutral" for r in results),
    }
    return jsonify({"results": results, "summary": summary})


if __name__ == "__main__":
    app.run(debug=True)
