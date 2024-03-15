#!/usr/bin/env python3

import sys
import nltk
nltk.downloader.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()
for line in sys.stdin:
    app_version, review_text = line.strip().split(',')
    sentiment = sia.polarity_scores(review_text)
    print(f'{app_version},{sentiment["compound"]}')
