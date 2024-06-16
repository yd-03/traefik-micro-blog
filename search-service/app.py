from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import time

app = Flask(__name__)


# Elasticsearch 接続試行のリトライロジック
def create_elasticsearch_client():
    es = None
    retries = 5
    while retries > 0:
        try:
            es = Elasticsearch(["http://elasticsearch:9200"])
            if es.ping():
                print("Connected to Elasticsearch")
                return es
        except Exception:
            print(
                f"Elasticsearch connection failed. Retrying in 5 seconds... ({retries} retries left)"
            )
            time.sleep(5)
            retries -= 1
    raise Exception("Could not connect to Elasticsearch")


es = create_elasticsearch_client()


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    result = es.search(
        index="posts",
        body={
            "query": {"multi_match": {"query": query, "fields": ["title", "content"]}}
        },
    )

    return jsonify(result["hits"]["hits"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
