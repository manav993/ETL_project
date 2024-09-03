
---

# ETL Project

## Overview

This project is designed to perform Extract, Transform, Load (ETL) operations to process data from various sources, transform it according to business rules, and load it into a target data warehouse for further analysis.

The ETL pipeline is implemented using Python3, Apache Kafka, Apache Spark, and a WebSocket server for real-time data visualization.

## Table of Contents

1. [Features](#features)
2. [Technologies Used](#technologies-used)
3. [Architecture](#architecture)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Configuration](#configuration)
7. [Contributing](#contributing)
8. [License](#license)

## Features

- **Data Extraction**: Extracts data from multiple sources like APIs, databases, and flat files.
- **Data Transformation**: Cleans and transforms the raw data into a structured format suitable for analysis.
- **Data Loading**: Loads the transformed data into a data warehouse or database.
- **Real-Time Data Visualization**: Uses WebSocket for real-time data streaming and visualization.
- **Error Handling**: Implements robust error handling and logging mechanisms.

## Technologies Used

- **Python3**: Main programming language used for ETL scripting.
- **Apache Kafka**: Used for real-time data streaming.
- **Apache Spark**: Used for distributed data processing.
- **WebSockets**: For real-time data visualization.
- **Git**: Version control for project collaboration.

## Architecture

1. **Data Extraction**: Data is fetched from various sources and published to Apache Kafka topics.
2. **Data Transformation**: Apache Spark consumes data from Kafka, performs transformations, and writes the results to a target data store.
3. **Data Loading**: Transformed data is loaded into the target data warehouse.
4. **Real-Time Visualization**: A WebSocket server streams the processed data to a front-end web application for real-time visualization.

## Installation

### Prerequisites

- [Python3 3.8+](https://www.Python3.org/downloads/)
- [Apache Kafka](https://kafka.apache.org/downloads)
- [Apache Spark](https://spark.apache.org/downloads.html)
- [Git](https://git-scm.com/)

### Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/manav993/ETL_project.git
   cd ETL_project
   ```

2. **Set Up Python3 Environment**:
   ```bash
   Python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Start Kafka and Zookeeper**:
   Follow the instructions in the `kafka/README.md` file to start Kafka and Zookeeper.

4. **Run Spark Jobs**:
   Submit the Spark job using the `spark-submit` command.

5. **Start WebSocket Server**:
   ```bash
   Python3 websocket_server.py
   ```

## Usage

1. **Generate Data**: Run the data generator script to start sending data to Kafka.
   ```bash
   Python3 generate_web_traffic.py
   ```

2. **Run ETL Pipeline**: Start the ETL process by running the Spark consumer script.
   ```bash
   spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 spark_consumer.py
   ```

3. **Visualize Data**: Open `index.html` in a web browser to visualize the streaming data in real-time.

## Configuration

- **Kafka Configuration**: Configure your Kafka brokers and topics in `kafka/config/server.properties`.
- **Spark Configuration**: Adjust Spark configurations in `spark_conf.conf`.
- **WebSocket Configuration**: Modify the WebSocket server configurations in `websocket_server.py`.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request for any enhancements, bug fixes, or documentation improvements.


