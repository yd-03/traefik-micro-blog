from elasticsearch import Elasticsearch, ElasticsearchException

es = Elasticsearch(["http://elasticsearch:9200"])

# インデックスの設定（必要に応じてカスタマイズしてください）
index_settings = {
    "settings": {"number_of_shards": 1, "number_of_replicas": 0},
    "mappings": {
        "properties": {
            "title": {"type": "text"},
            "content": {"type": "text"},
            "author_id": {"type": "integer"},
        }
    },
}

try:
    # インデックスの存在をチェックし、存在しない場合のみ作成
    if not es.indices.exists(index="posts"):
        es.indices.create(index="posts", body=index_settings)
except ElasticsearchException as e:
    print(f"Error creating index: {e}")

# サンプルデータのインデックス
posts = [
    {
        "title": "First Post",
        "content": "This is the content of the first post.",
        "author_id": 1,
    },
    {
        "title": "Second Post",
        "content": "This is the content of the second post.",
        "author_id": 2,
    },
    # 追加のサンプルデータをここに
]

for i, post in enumerate(posts):
    try:
        es.index(index="posts", id=i + 1, body=post)
    except ElasticsearchException as e:
        print(f"Error indexing post {i+1}: {e}")
