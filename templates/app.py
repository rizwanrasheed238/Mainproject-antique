import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# initialize the sentiment analyzer
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

# define a function to perform sentiment analysis on a piece of text
def analyze_sentiment(text):
    scores = sia.polarity_scores(text)
    if scores['compound'] >= 0.05:
        return 'Positive'
    elif scores['compound'] <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# test the function on some sample text
text = "I love this product! It works great and makes my life so much easier."
print(analyze_sentiment(text))
# Output: Positive

text = "I hate this product. It's a complete waste of money and time."
print(analyze_sentiment(text))
# Output: Negative

text = "This book was okay. It had some good parts and some bad parts."
print(analyze_sentiment(text))
# Output: Neutral