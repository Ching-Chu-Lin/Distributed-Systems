import pandas as pd

df = pd.read_csv('./tiktok_app_reviews.csv',
                 usecols=['app_version', 'review_text'])
df.dropna()

df.to_csv('tiktok_parsed.csv', header=True, index=False)
