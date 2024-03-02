# from pyspark.sql.functions import regexp_replace, col
# from pyspark.ml.feature import Tokenizer
# from pyspark.sql import SparkSession
from nltk.stem import *
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import pandas as pd
import concurrent.futures

# # Load review datasets
# dfr1 = pd.read_csv('./dataset1/rotten_tomatoes_critic_reviews.csv')
# dfr2 = pd.read_csv('./dataset2/rotten_tomatoes_movie_reviews.csv')
# # Load movie datasets
# dfm1 = pd.read_csv('./dataset1/rotten_tomatoes_movies.csv')
# dfm2 = pd.read_csv('./dataset2/rotten_tomatoes_movies.csv')
# # Check the shape of the datasets
# print(dfr1.shape)  # (1130017, 8)
# print(dfr2.shape)  # (1444963, 11)
# print(dfm1.shape)  # (17712, 22)
# print(dfm2.shape)  # (143258, 16)
# # Display the first row of each dataset
# for i in (dfr1, dfr2, dfm1, dfm2):
#     print(i.head(1))

# # Rename columns for consistency
# dfr1.rename(columns={'rotten_tomatoes_link': 'id'}, inplace=True)
# dfm1.rename(columns={'rotten_tomatoes_link': 'id'},  inplace=True)

# dfr2.rename(columns={'criticName': 'critic_name', 'creationDate': 'review_date', 'isTopCritic': 'top_critic', 'publicatioName': 'publisher_name',
#                      'reviewText': 'review_content', 'originalScore': 'review_score', 'reviewState': 'review_type'}, inplace=True)
# dfm2.rename(columns={'title': 'movie_title'}, inplace=True)
# # Check for missing values
# print('DFR1 NULL')
# print(dfr1.isnull().sum())
# print('DFR2 NULL')
# print(dfr2.isnull().sum())
# # Drop unnecessary columns
# dfr2.drop(columns=['reviewId', 'scoreSentiment', 'reviewUrl'], inplace=True)
# # Display the first two rows and data information
# for i in dfr1, dfm1, dfr2, dfm2:
#     print(i.head(2))
#     print(i.info())


# # Create a Spark session
# spark = SparkSession.builder \
#     .appName("New_NLP") \
#     .config("spark.driver.memory", "4g") \
#     .config("spark.executor.memory", "4g") \
#     .getOrCreate()
# # Create Spark DataFrames from pandas DataFrames
# sp_dfr1 = spark.createDataFrame(dfr1)
# sp_dfr2 = spark.createDataFrame(dfr2)
# sp_dfm1 = spark.createDataFrame(dfm1)
# sp_dfm2 = spark.createDataFrame(dfm2)
# # Drop rows with missing values
# sp_dfr1 = sp_dfr1.na.drop()
# sp_dfr2 = sp_dfr2.na.drop()
# # Tokenize the review content
# tokenizer = Tokenizer(inputCol="review_content", outputCol="tokens")
# sp_dfr1 = tokenizer.transform(sp_dfr1)
# sp_dfr2 = tokenizer.transform(sp_dfr2)
# # Remove non-alphanumeric characters from review content
# sp_dfr1 = sp_dfr1.withColumn("review_content", regexp_replace(
#     col("review_content"), "[^a-zA-Z0-9\s,;]", ""))
# sp_dfr2 = sp_dfr2.withColumn("review_content", regexp_replace(
#     col("review_content"), "[^a-zA-Z0-9\s,;]", ""))
# # Display a sample of the transformed data
# sp_dfr2.show(2)


# # Inner join to merge review data with movie data
# reviews1 = sp_dfr1.join(sp_dfm1, "id", "inner")
# reviews2 = sp_dfr2.join(sp_dfm2, "id", "inner")

# # Free up memory by unpersisting Spark DataFrames
# sp_dfr1.unpersist()
# sp_dfr2.unpersist()
# sp_dfm1.unpersist()
# sp_dfm2.unpersist()
# # Select only the necessary columns
# reviews1 = reviews1.select('movie_title', 'critic_name', 'top_critic', 'publisher_name',
#                            'review_type', 'review_score', 'review_date', 'review_content')
# reviews2 = reviews2.select('movie_title', 'critic_name', 'top_critic', 'publisher_name',
#                            'review_type', 'review_score', 'review_date', 'review_content')
# # Drop rows with missing values
# reviews1 = reviews1.na.drop()
# reviews2 = reviews2.na.drop()
# # Combine both review DataFrames into one for further analysis
# merged_df = reviews1.union(reviews2)
# # Display a sample of the merged DataFrame
# merged_df.show(1)
# # Save the merged data locally (this will be uploaded to HDFS)
# merged_df.coalesce(1).write.csv('reviewsjoined.csv', header=True)
# # Stop the Spark session
# spark.stop()

# ============================== #
# Load the integrated data
df = pd.read_csv(
    'reviewsjoined.csv/part-00000-ac59c93a-0efe-41da-a2bd-e160c861c62e-c000.csv')
# Drop rows with missing values
df.dropna(inplace=True)
# Sample data for parallel preprocessing
sample_df = df.sample(500000)
sample_df['review_content'] = sample_df['review_content'].astype(str)
# Define functions for preprocessing


def preprocess_text(text):
    text = text.lower()

    # Tokenize
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word not in stop_words]
    # Stemming
    stemmer = PorterStemmer()
    stemmed_words = [stemmer.stem(word) for word in filtered_words]
    # Lemmatizing
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in stemmed_words]
    processed_text = ' '.join(lemmatized_words)
    return processed_text


def parallel_preprocess(data):
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        processed_data = list(executor.map(preprocess_text, data))
    return processed_data


# Parallel preprocessing
sample_df['review_content'] = parallel_preprocess(sample_df['review_content'])
# sample_df['review_content'] = preprocess_text(sample_df['review_content'])
# Remove commas from review content
sample_df['review_content'] = sample_df['review_content'].apply(
    lambda x: x.replace(",", ""))
# Remove special characters from movie titles
sample_df['movie_title'] = sample_df['movie_title'].apply(
    lambda x: ''.join(e for e in x if e.isalnum() or e.isspace()))
# Display the preprocessed sample data
sample_df.head()


# Remove commas and special characters from review content and movie titles
df['review_content'] = df['review_content'].apply(lambda x: x.replace(",", ""))
df['movie_title'] = df['movie_title'].apply(
    lambda x: ''.join(e for e in x if e.isalnum() or e.isspace()))

# Save the cleaned and preprocessed data for Hadoop
df.to_csv('big_movies.csv', header=True, index=False)
