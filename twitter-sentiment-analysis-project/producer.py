import pandas as pd
from kafka import KafkaProducer
import logging
import json

logging.basicConfig(level=logging.INFO)
producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic_name = 'twitter'

def on_send_success(record_metadata):
    logging.info(f"Message sent to topic {record_metadata.topic} partition {record_metadata.partition} at offset {record_metadata.offset}")

def on_send_error(excp):
    logging.error('Message delivery failed: ', exc_info=excp)
    
def stream_csv_file(file_name):
    # Define the column names
    column_names = ["Tweet ID", "Entity", "Sentiment", "TweetContent"]

    # Read the CSV file and assign column names
    df = pd.read_csv(file_name, names=column_names)

    # Iterate over each row in the dataframe
    for index, row in df.iterrows():
        # Print the data being sent
        print("Data being sent:", row.to_dict())

        # Convert the row to JSON and send it to Kafka
        data = {
            'Tweet ID': row['Tweet ID'],
            'Entity': row['Entity'],
            'TweetContent': row['TweetContent'].replace(',', ''),
            'Sentiment': row['Sentiment'],
            'columns': column_names  # Include column names in the data
        }
        producer.send(topic_name, value=json.dumps(data).encode('utf-8')).add_callback(on_send_success).add_errback(on_send_error)


if __name__ == '__main__':
    stream_csv_file('twitter_validation.csv')
