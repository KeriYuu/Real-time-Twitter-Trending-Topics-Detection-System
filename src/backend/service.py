from flask import Flask, jsonify
from hdfs import InsecureClient

app = Flask(__name__)

@app.route('/trending-topics', methods=['GET'])
def get_trending_topics():
    client = InsecureClient('http://localhost:50070', user='hdfs')  # replace with your HDFS details

    # Read the data from Hadoop
    with client.read('/twitterData') as reader:
        data = reader.read()

    # Send the data to the frontend
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=3001)
