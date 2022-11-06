import pandas as pd
import nltk
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def sentiment_analysis(df):
    df = df.dropna()
    sentiments=SentimentIntensityAnalyzer()
    df["Positive"]=[sentiments.polarity_scores(i)["pos"] for i in df["message"]]
    df["Negative"]=[sentiments.polarity_scores(i)["neg"] for i in df["message"]]
    df["Neutral"]=[sentiments.polarity_scores(i)["neu"] for i in df["message"]]

    return df

def sentiment_overall(df):
    a=sum(df["Positive"])
    b=sum(df["Negative"])
    c=sum(df["Neutral"])

    if (a>b) and (a>c):
        return "Positive "
    if (b>a) and (b>c):
        return "Negative"
    if (c>a) and (c>b):
        return "Neutral"
    