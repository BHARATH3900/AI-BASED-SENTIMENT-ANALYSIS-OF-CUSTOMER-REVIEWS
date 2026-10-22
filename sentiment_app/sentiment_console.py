from textblob import TextBlob

def analyze_sentiment(review):
    analysis = TextBlob(review)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        sentiment = "Positive"
    elif polarity < 0:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "Review": review,
        "Polarity Score": polarity,
        "Predicted Sentiment": sentiment,
    }

review = input("Enter Customer Review: ")
result = analyze_sentiment(review)

print("\nSentiment Analysis Result")
print("-------------------------")
print("Review :", result["Review"])
print("Polarity Score :", result["Polarity Score"])
print("Sentiment :", result["Predicted Sentiment"])
