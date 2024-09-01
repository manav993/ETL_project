from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col, to_timestamp, sum, count, round
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
import json
import websockets
import asyncio

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("KafkaSparkConsumer") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2") \
    .getOrCreate()

# Set log level to WARN to reduce output verbosity
spark.sparkContext.setLogLevel("WARN")

# Define schema for incoming data
schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("timestamp", StringType(), True),
    StructField("page", StringType(), True),
    StructField("session_duration", IntegerType(), True)
])

# Read from Kafka topic 'web_traffic'
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "web_traffic") \
    .load()

# Convert the value column to string
kafka_df = df.selectExpr("CAST(value AS STRING)")

# Parse CSV data by splitting the 'value' column and convert timestamp to timestamp type
web_traffic_df = kafka_df.select(
    split(col("value"), ",").getItem(0).alias("user_id"),
    to_timestamp(split(col("value"), ",").getItem(1), 'yyyy-MM-dd HH:mm:ss').alias("timestamp"),
    split(col("value"), ",").getItem(2).alias("page"),
    split(col("value"), ",").getItem(3).cast(IntegerType()).alias("session_duration")
)

# Group by user_id, page to calculate total time spent per user on each page
user_page_time_window = web_traffic_df.groupBy(
    "user_id", 
    "page"
).agg(
    count("*").alias("count"),  # Count of visits
    round(sum("session_duration") / 60, 1).alias("total_time_spent_minutes")  # Total time spent in minutes, rounded to 1 decimal place
)

async def send_to_websocket(data):
    uri = "ws://localhost:5678"  # WebSocket server URL
    try:
        print(f"Attempting to connect to WebSocket server at {uri}")
        async with websockets.connect(uri) as websocket:
            print("Successfully connected to WebSocket server.")  # Confirm connection
            await websocket.send(json.dumps(data))
            print("Data sent to WebSocket server.")  # Confirm data is sent
    except Exception as e:
        print(f"Error sending data to WebSocket: {e}")  # Log any errors

# Function to process each batch of data and send it to the WebSocket server
def process_batch(df, epoch_id):
    # Collect the DataFrame into a list of dictionaries
    data = [row.asDict() for row in df.collect()]
    
    # Print data to console
    print(f"Processing Batch {epoch_id}:")
    for row in data:
        print(row)
    
    # Send data asynchronously to WebSocket
    print(f"Sending data to WebSocket: {data}")  # Debug statement
    asyncio.run(send_to_websocket(data))

# Use foreachBatch to process each batch
query = user_page_time_window.writeStream \
    .foreachBatch(process_batch) \
    .outputMode("complete") \
    .start()

query.awaitTermination()
