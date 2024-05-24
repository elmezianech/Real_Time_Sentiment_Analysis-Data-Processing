# Real_Time_Sentiment_Analysis-Data-Processing

This repository contains the data processing components of a real-time sentiment analysis application for Twitter data. The application utilizes Apache Kafka, PySpark, and MongoDB.

![Screenshot 2024-05-24 193722](https://github.com/elmezianech/Real_Time_Sentiment_Analysis-Data-Processing/assets/120784838/627ee086-c82b-4752-a5c8-f6411b29e612)

## Introduction

This project aims to develop a real-time sentiment analysis application for tweets using Apache Kafka and Spark Streaming. The goal is to predict the sentiment (positive, negative, neutral, or irrelevant) of a given tweet.

## Architecture and Technologies Used

### Architecture

The architecture of the project consists of the following elements:
1. **Twitter Data Stream**: Tweets are collected from a CSV file `twitter_validation.csv`.
2. **Apache Kafka**: Kafka serves as the streaming platform to process incoming tweets.
3. **Apache Spark Streaming**: Spark Streaming processes the tweets from the Kafka topic. The processing involves:
   - **Preprocessing**: Cleaning and preprocessing tweets to extract relevant features.
   - **Model Training**: Training a supervised machine learning model (Logistic Regression) on a labeled dataset (`twitter_training.csv`).
   - **Prediction**: Using the trained model to predict the sentiment of new tweets.
   - **Result Storage**: Storing sentiment predictions in MongoDB.
4. **Integration with Web Application**: The results from the data processing are used by the `real-time-sentiment-analysis-web` repository for visualization.

### Tools and Technologies

The tools and technologies used in this project include:
- **Python**: For developing data processing scripts, training machine learning models, and interacting with various technologies.
- **Docker**: To containerize different parts of the application, ensuring easy portability and scalability.
- **Apache Kafka**: For real-time data streaming.
- **Apache Spark (PySpark)**: For data processing and machine learning model training.
- **MongoDB**: For storing sentiment prediction results.
- **NLTK**: For text data preprocessing (tokenization, stop words removal, lemmatization).
- **Matplotlib**: For data visualization and analysis results.
- **Frontend and Backend Integration**: The `Real_Time_Sentiment_Analysis-Frontend-and-Backend` repository is included for complete frontend and backend functionality.
  
## Implementation

### Spark and Model Training

1. **Data Loading**: Data is loaded from the `twitter_training.csv` file using PySpark.
2. **Data Preprocessing**: Data is cleaned and prepared for analysis, including tokenization, stop words removal, and lemmatization using NLTK.
3. **Model Selection and Training**: A supervised machine learning model (Logistic Regression) is trained on the preprocessed data.
4. **Model Evaluation and Saving**: The trained model is evaluated, and the best-performing model is saved for real-time prediction.

### Kafka

1. **Broker, Topic, and Partition Setup**: Kafka is configured with the necessary brokers, topics, and partitions for processing Twitter data.
2. **Kafka Streams**: Kafka Streams are used to read Twitter data from the `twitter_validation.csv` file.
3. **Real-Time Processing**: Incoming data is processed using the pre-trained machine learning model to predict sentiments.
4. **Result Storage**: Sentiment prediction results are saved in MongoDB.

### Integration with Web Application

1. **Frontend and Backend Integration**: The `real-time-sentiment-analysis-web` repository is included within this repository.
2. **Data Flow**: The data processed and predicted in this repository is used by the web application for visualization and user interaction.
