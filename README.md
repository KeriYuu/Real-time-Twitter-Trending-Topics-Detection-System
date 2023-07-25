# Real-time-Twitter-Trending-Topics-Detection-System

This project uses various technologies to create a real-time Twitter trending topics detection system. The system fetches Twitter data, processes it, and stores it in a Hadoop filesystem. A backend service interacts with Hadoop to fetch the data, and a frontend React application displays the data.

## Architecture

1. Twitter API: Fetches real-time tweets.
2. Kafka: A messaging system that ingests the real-time tweets.
3. Hadoop: Stores the processed data.
4. Backend Service: A bridge between Hadoop and the frontend application, fetching the necessary data from Hadoop.
5. Frontend Application: A React application that fetches data from the backend service and displays it.

## Installation

This guide assumes you are using a CentOS 7 system.

### Docker

Refer to the [Docker installation guide](https://docs.docker.com/engine/install/).

### Kafka

Download Kafka from the [official website](https://kafka.apache.org/downloads). Then extract the downloaded file:

```bash
tar -xzf kafka_2.13-3.4.1.tgz
cd kafka_2.13-2.8.0
```

Start Kafka:

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
bin/kafka-topics.sh --create --topic twitter_topics --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

### Hadoop

Pull the necessary Docker images and run the containers:

```bash
docker pull bde2020/hadoop-namenode:2.0.0-hadoop2.7.4-java8
docker pull bde2020/hadoop-datanode:2.0.0-hadoop2.7.4-java8
docker pull bde2020/hadoop-historyserver:2.0.0-hadoop2.7.4-java8

docker network create hadoop

docker run -d --net=hadoop --name=namenode -p 50070:50070 -p 8088:8088 -e CLUSTER_NAME=test bde2020/hadoop-namenode:2.0.0-hadoop2.7.4-java8
docker run -d --net=hadoop --name=datanode -p 50075:50075 bde2020/hadoop-datanode:2.0.0-hadoop2.7.4-java8
docker run -d --net=hadoop --name=historyserver -p 8188:8188 bde2020/hadoop-historyserver:2.0.0-hadoop2.7.4-java8
```

### Backend Service

Install the necessary Python libraries:

```bash
cd backend
conda create -n twitter python=3.8
pip install -r requirements.txt
```

Then, start the backend service:

```bash
python server.py
```

### Frontend Application

First, install Node.js and npm. Then, create a new React application and install axios:

```bash
cd frontend
npm install axios
```

Start the React application:

```bash
npm start
```

## Usage

Once everything is set up and running, you can navigate to `http://localhost:3000` in your web browser to see the trending topics.