from textblob import TextBlob
import pandas as pd

def analyze_sentiment(message):
    try:
        blob = TextBlob(message)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            return 'Positive'
        elif polarity < -0.1:
            return 'Negative'
        else:
            return 'Neutral'
    except:
        return 'Neutral'

def add_sentiment_column(df):
    """
    Adds a 'sentiment' column to the DataFrame based on each message.
    """
    df = df.copy()
    if 'message' in df.columns:
        df['sentiment'] = df['message'].apply(analyze_sentiment)
    else:
        raise KeyError("DataFrame must contain a 'message' column.")
    return df
