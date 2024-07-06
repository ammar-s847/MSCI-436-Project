import finnhub
from datetime import datetime, timedelta
from transformers import pipeline
import os

# Initialize Finnhub client
finnhub_api_key = os.getenv("FINNHUB_API_KEY")
if not finnhub_api_key:
    raise ValueError("No FINNHUB_API_KEY found in environment variables")
finnhub_client = finnhub.Client(api_key=finnhub_api_key)

# Load the sentiment analysis model
sentiment_pipeline = pipeline("sentiment-analysis", model="mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")

def load_news_data(ticker):
    current_date = datetime.now()
    from_date = current_date - timedelta(days=1)
    news_data = finnhub_client.company_news(ticker, _from=from_date.strftime("%Y-%m-%d"), to=current_date.strftime("%Y-%m-%d"))
    return news_data

def analyze_sentiment(news_data):
    num_positive = 0
    num_neutral = 0
    num_negative = 0

    news_articles = []

    for article in news_data:
        combined_text = article['headline'] + " " + article['summary']
        prediction = sentiment_pipeline(combined_text)[0]

        if prediction['score'] >= 0.9:
            if prediction['label'] == 'positive':
                num_positive += 1
            elif prediction['label'] == 'negative':
                num_negative += 1
            elif prediction['label'] == 'neutral':
                num_neutral += 1
        else:
            # Default to neutral if model confidence is low
            num_neutral += 1

        news_articles.append({
                    "headline": article['headline'],
                    "description": article['summary'],
                    "timestamp": article['datetime'],
                    "sentiment": prediction['label'],
                    "url": article['url']
                })

    # Determine the overall sentiment based on the highest count
    if num_positive > num_neutral and num_positive > num_negative:
        overall_sentiment = 'positive'
    elif num_negative > num_neutral and num_negative > num_positive:
        overall_sentiment = 'negative'
    else:
        overall_sentiment = 'neutral'

    return {
        "overall_sentiment": overall_sentiment,
        "news_articles": news_articles
    }
