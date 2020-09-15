# Daily news API
# Author Sean Hoyal, 2020
# Ver 1.0
#
# Implements jobs from sky_scraping Ver 2.0
#
# Imports
import os
from flask import Flask, request, jsonify, abort, url_for
from apscheduler.schedulers.background import BackgroundScheduler
from cassandra.cluster import Cluster
from sky_scraping import Scraper
from datetime import date
import requests
import schedule
import json
import time

# Initialize cluster connection
cluster = Cluster(contact_points=['192.168.99.107'],port=30036)
session = cluster.connect(wait_for_all_pools=True)

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Local Job
def cassCopy():
    session.execute("""COPY news.daily (uid, title, date, trending, brexit, covid) FROM '/home/modified_articles.csv' WITH DELIMITER=',' AND HEADER=TRUE;
""")
    return("New files moved into news.daily")

# Instantiate Scraper & Schedule jobs
scrap1 = Scraper

sched = BackgroundScheduler(daemon=True)
sched.add_job(scrap1.reset,'interval',hours=23,minutes=59)
sched.add_job(scrap1.scrape,'interval',hours=23,minutes=59,seconds=5)
sched.add_job(scrap1.addBinary,'interval',hours=23,minutes=59,seconds=10)
sched.add_job(scrap1.migrateCass,'interval',hours=23,minutes=59,seconds=15)
sched.add_job(cassCopy(), interval,hours=23,minutes=59,seconds=20)
sched.start()

# API Routes
@app.route('/')
def hello():
    return('<h1> Hello! Welcome to my scrapes web API, currently scaping from Sky! Visit /articles for daily current articles<h1>')

@app.route('/articles', methods=['GET'])
def all():
    tuples = session.execute("""Select * From news.daily""")
    results = []
    for x in tuples:
        results.append({"title":x.title,"date":x.date})
    return jsonify(results), 200

@app.route('/today', methods=['GET'])
def current():
    tuples = session.execute("""Select * From news.daily WHERE date='{}' ALLOW FILTERING""".format(str(date.today())))
    results = []
    for x in tuples:
        results.append({"title":x.title,"date":x.date})
    return jsonify(results), 200

@app.route('/brexit', methods=['GET'])
def brexit():
    tuples = session.execute("""Select * From news.daily WHERE brexit=1 ALLOW FILTERING""")
    results = []
    for x in tuples:
        results.append({"title":x.title,"date":x.date})
    return jsonify(results), 200

@app.route('/covid', methods=['GET'])
def covid():
    tuples = session.execute("""Select * From news.daily WHERE covid=1 ALLOW FILTERING""")
    results = []
    for x in tuples:
        results.append({"title":x.title,"date":x.date})
    return jsonify(results), 200

# App run
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
