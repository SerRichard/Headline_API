import os
import json
import requests
from flask import Flask, request, jsonify, abort, url_for
from cassandra.cluster import Cluster

# Initialize cluster connection
cluster = Cluster(contact_points=['0.0.0.0'],port=9042)
session = cluster.connect()

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Extensions
# ...

@app.route('/')
def hello():
    return('<h1> Hello! Welcome to my scrapes web API, currently scaping from Sky! Visit /articles for all current articles<h1>')

@app.route('/articles', methods=['GET'])
def articles():
    tuples = session.execute("""Select * From c02.stats""")
    results = []
    for x in tuples:
        results.append({})
    return jsonify(results), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)