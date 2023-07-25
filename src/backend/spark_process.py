from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Set up Spark session
spark = SparkSession.builder.appName("TwitterStreamApp").getOrCreate()

# Read from Kafka stream
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "twitter_topics") \
    .load()

# Cast data to string
df = df.selectExpr("CAST(value AS STRING)")

# Define data schema
schema = StructType([
    StructField("created_at", StringType()),
    StructField("id", StringType()),
    StructField("text", StringType()),
])

# Convert JSON string to data using the defined schema
df = df.withColumn("data", from_json(df.value, schema)).select("data.*")

# Remove URLs and mentions from the text
df = df.withColumn('text', regexp_replace('text', r'http\S+', ''))
df = df.withColumn('text', regexp_replace('text', '@\w+', ''))

# Split the text into words and count each word
wordCounts = df.select(explode(split(df.text, " ")).alias("word")).groupBy('word').count()

# Filter for words that have a count greater than 10
hotTopics = wordCounts.filter(wordCounts['count'] > 10)

# Write the word counts to a Parquet file, checkpointing the progress
query = hotTopics.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "/twitterData") \
    .option("checkpointLocation", "/checkpoint") \
    .start()

# Wait for the streaming query to end
query.awaitTermination()
