#!/bin/sh

echo "Waiting for Elasticsearch to start..."
while ! nc -z elasticsearch 9200; do
    sleep 1
done

echo "Elasticsearch started"
python index_data.py
python app.py
