import tweepy
import os
from kafka import KafkaProducer
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Twitter API keys
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# Set up logger
logger = logging.getLogger(__name__)

# Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092') 

# Define topic and search input
topic_name = "twitter_topics"
search_input = "nba, #NBA, NBA, #nba, Nba"

class TwitterStreamer():
    def stream_data(self):
        # Start stream
        logger.info(f"{topic_name} Stream starting for {search_input}...")
        twitter_stream = MyListener(consumer_key, consumer_secret, access_token, access_token_secret)
        twitter_stream.filter(track=[search_input])

class MyListener(tweepy.StreamListener):
    # Receive data from stream
    def on_data(self, data):
        try:
            # Send data to Kafka
            logger.info("Sending data to Kafka...")
            producer.send(topic_name, data)
        except BaseException as e:
            # Log any errors
            logger.error(f"Error on_data: {str(e)}")
            return True

    # Handle stream errors
    def on_error(self, status):
        logger.error(f"Stream error: {status}")
        return True

if __name__ == "__main__":
    # Start streaming data
    TS = TwitterStreamer()
    TS.stream_data()
