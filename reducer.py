#!/usr/bin/env python3

import sys

processing_app_version = None
sum_sentiment = 0.0
num_reviews = 0

for line in sys.stdin:
    app_version, sentiment = line.strip().split(',')

    if processing_app_version != app_version:
        if processing_app_version is not None:
            # Calculate the average sentiment
            average_sentiment = sum_sentiment / num_reviews
            print(f'{processing_app_version},{average_sentiment:.2f}')

        processing_app_version = app_version
        # reset
        sum_sentiment = 0.0
        num_reviews = 0

    sentiment_score = float(sentiment)
    sum_sentiment += sentiment_score
    num_reviews += 1

# average sentiment for the last app version
if processing_app_version is not None:
    average_sentiment = sum_sentiment / num_reviews
    print(f'{processing_app_version},{average_sentiment:.2f}')
