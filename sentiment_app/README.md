# AI-Based Sentiment Analysis of Customer Reviews

Frontend: HTML, CSS, JavaScript | Backend: Python (Flask) | NLP: TextBlob

## Project structure
sentiment_app/
├── app.py                # Flask backend + TextBlob analysis
├── sentiment_console.py  # Console version (sample code from the report)
├── requirements.txt
└── static/
    └── index.html        # Frontend (HTML + CSS + JS)


## API
POST /analyze        body: {"review": "text"}
POST /analyze-bulk   body: {"reviews": ["text1", "text2"]}

## Classification rule
Polarity > 0 -> Positive | Polarity < 0 -> Negative | Polarity = 0 -> Neutral
