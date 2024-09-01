from kafka import KafkaProducer
import random
import time
from datetime import datetime

# Set up Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# List of pages to simulate user visits
pages = ['home', 'about', 'products', 'contact', 'blog']

# Generate a fixed list of user IDs (user_1 to user_50)
users = [f"user_{i}" for i in range(1, 51)]

def generate_web_traffic():
    # Randomly select a user from the predefined list of users
    user_id = random.choice(users)
    
    # Get the current timestamp in the format 'yyyy-MM-dd HH:mm:ss'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Randomly choose a page from the list
    page = random.choice(pages)
    
    # Random session duration between 1 and 300 seconds
    session_duration = random.randint(1, 300)
    
    # Generate a line of synthetic data in the format 'user_id,timestamp,page,session_duration'
    log_line = f"{user_id},{timestamp},{page},{session_duration}"
    
    return log_line

# Simulate continuous data generation
while True:
    # Generate synthetic data
    for _ in range(5):  # Simulate multiple visits in a single batch
        message = generate_web_traffic()
        
        # Send data to Kafka topic 'web_traffic'
        producer.send('web_traffic', value=message.encode('utf-8'))
        print(f"Sent: {message}")
        
    # Wait for 1 second before sending the next batch
    time.sleep(1)
