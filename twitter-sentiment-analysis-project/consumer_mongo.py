import findspark
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, udf, json_tuple
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, IntegerType
from pyspark.sql import DataFrameWriter
import re

def preprocess_text(text):
    if isinstance(text, str):  # Check if text is a string
        cleaned_text = re.sub(r'[^A-Za-z\n ]|(http\S+)|(www.\S+)', '', text)
        return cleaned_text.split()
    else:
        return []  # Return an empty list for non-string inputs

def write_mongo(df, epoch_id):
    df.write.format("mongo").mode("append").option("database","twitter").option("collection", "tweets_col").save()

if __name__ == "__main__":
    findspark.init()

    # Path to the pre-trained model
    path_to_model = r'C:\Users\Yasmine\Desktop\Projet_Big Data\pyspark-etl-twitter-main\pre_trained_model'

    # Config
    spark = SparkSession \
        .builder \
        .master("local[*]") \
        .appName("TwitterSentimentAnalysis") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1") \
        .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/twitter.tweets_col") \
        .config("spark.sql.execution.pythonUDF.arrow.enabled", "false") \
        .getOrCreate()

    # Spark Context
    sc = spark.sparkContext
    sc.setLogLevel('ERROR')

    # Read the data from kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "twitter") \
        .option("startingOffsets", "latest") \
        .load() \
        .selectExpr("CAST(value AS STRING) as json_str")

    # Convert the JSON string to JSON object and extract values
    df = df.select(json_tuple(df.json_str, "Tweet ID", "Entity", "TweetContent", "Sentiment").alias("Tweet ID", "Entity", "TweetContent", "Sentiment"))

    # Define UDF for preprocessing
    pre_process_udf = udf(preprocess_text, ArrayType(StringType()))

    # Apply the UDF to the DataFrame column and drop null values
    df = df.withColumn("cleaned_data", pre_process_udf(df['TweetContent'])).dropna()

    # Extract the cleaned text for prediction
    df = df.withColumn("Tweet content", df["cleaned_data"].cast(StringType()))

    # Load the pre-trained model
    pipeline_model = PipelineModel.load(path_to_model)

    # Define a UDF to convert the numeric predictions to strings
    def convert_prediction(prediction):
        sentiment_dict = {
            0: 'Negative',
            1: 'Positive',
            2: 'Neutral',
            3: 'Irrelevant'
        }
        return sentiment_dict.get(int(prediction), 'Unknown')

    convert_prediction_udf = udf(convert_prediction, StringType())

    # Make predictions using the extracted text
    prediction = pipeline_model.transform(df.select("Tweet content", "Tweet ID", "Entity", "Sentiment", "TweetContent"))

    # Convert the numeric predictions to sentiment labels
    prediction = prediction.withColumn("prediction", convert_prediction_udf(prediction["prediction"]))

    # Select the columns of interest
    prediction = prediction.select("Tweet ID", "Entity", "TweetContent", "Sentiment", "prediction")

    # Write prediction to MongoDB
    query = prediction.writeStream.outputMode("update").foreachBatch(write_mongo).start()
    query.awaitTermination()


