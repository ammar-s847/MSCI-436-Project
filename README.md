# MSCI 436 Decision Support Systems

## Finnhub API Key is required to be added to .env file
https://finnhub.io/

## Sentiment Analysis
Overall sentiment is calculated by analyzing news articles related to a specific company. The function processes each article by combining the headline and summary, converting the text to lowercase, and checking for the presence of the company's ticker or name. The sentiment of each article is predicted using a [sentiment analysis model](https://huggingface.co/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis?text=Operating+profit+totaled+EUR+9.4+mn+%2C+down+from+EUR+11.7+mn+in+2004+.). Articles mentioning the company name or ticker directly are given additional weight: articles mentioning the company get a weight of 2, and if the sentiment is negative and highly confident, an extra weight of 1 is added. Sentiment scores are categorized as positive, neutral, or negative based on model predictions and confidence levels. The overall sentiment (positive, neutral, or negative) is determined by the highest count of these categories, and the function returns this overall sentiment along with a list of analyzed news articles and their respective sentiments.
