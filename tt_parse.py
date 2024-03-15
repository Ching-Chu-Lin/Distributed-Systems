import pandas as pd

df = pd.read_csv('./tiktok_app_reviews.csv',
                 usecols=['app_version', 'review_text'])
df = df.dropna()
df = df.review_text.str.replace('[^a-zA-Z 0-9]', '')

df.to_csv('tiktok_parsed.csv', header=True, index=False)
