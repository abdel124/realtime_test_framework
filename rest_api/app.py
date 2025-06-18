from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json
import uuid

app = Flask(__name__)
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda m: json.dumps(m).encode('utf-8')
)

@app.route("/messages", methods=["POST"])
def post_message():
    data = request.get_json()
    key = str(uuid.uuid4())
    producer.send("chat-topic", value=data, key=key.encode('utf-8'))
    producer.flush()
    return jsonify({"status": "sent", "data": data}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)