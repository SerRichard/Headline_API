# Sky News daily web scraper
# Author Sean Hoyal, 2020
# Ver 2.0
# This version carries out the same scrape
# Additional methods:
# addBinary() to add binary indicators for articles about Brexit or Covid
# reset() to reset all files in directory
#
# Imports
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from datetime import datetime
from csv import DictReader, DictWriter, reader, writer
from itertools import islice
import pandas as pd
import subprocess
import uuid
import csv

class Scraper:
	@classmethod
	def scrape(self):
		my_url = 'https://news.sky.com/'

		#Opens connection, downloads page, then closes connection
		uReqSky = uReq(my_url)
		sky_html = uReqSky.read()
		uReqSky.close()

		# Parse into beautiful soup, place all of a particular class into containers
		news_soup = soup(sky_html, "html.parser")

		containers = news_soup.findAll("div",{"class":"sdc-site-tile__body"})
		trendings = news_soup.findAll("li",{"class":"sdc-site-trending__item"})

		# Prepare csv to record data
		filename = "scraped_articles.csv"
		f = open(filename, "a+")

		# Loop for non-trending articles: Sky
		for container in containers:
			uid = uuid.uuid4().hex
			try:
				article_titles = container.findAll("span",{"class":"sdc-site-tile__headline-text"})
				title = article_titles[0].text
			except IndexError:
				title = "N/A"
			
			date = datetime.today().strftime('%Y-%m-%d')
			trending = 'No'

			# Write findings to csv
			f.write("\n" + uid + "," + title.replace(",", "|") + ","  +  date + "," + trending)

		# Loop for the trending articles: Sky
		for trend in trendings:
			uid = uuid.uuid4().hex
			trending_titles = trend.findAll("a",{"class":"sdc-site-trending__link"})
			title = trending_titles[0].text

			date = datetime.today().strftime('%Y-%m-%d')
			trending = 'Yes'

			# Write findings to csv
			f.write("\n" + uid + "," + title.replace(",", "|") + ","  +  date + "," + trending)

		print("Scrape complete")
		f.close()

	@classmethod
	def addBinary(self):
		
		# Find all titles referring to Brexit
		input_file = "scraped_articles.csv"
		temp = "temp.csv"
		output_file = "modified_articles.csv"

		with open(input_file, "r") as f, \
			open(temp, 'w', newline='') as g:

			headers = ['uuid','title','date','trending','brexit']

			d_read = DictReader(f)
			d_write = DictWriter(g, fieldnames=headers)
		
			d_write.writeheader()

			brex = ("brexit", "BREXIT", "Brexit")

			for row in d_read:
				if any(x in row["title"] for x in brex):
					row["brexit"] = 1
					d_write.writerow(row)
				else:
					row["brexit"] = 0
					d_write.writerow(row)
			
		f.close()
		g.close()

		with open(temp, "r") as f, \
			open(output_file, 'w', newline='') as g:

			cov = ("coronavirus", "Coronavirus", "CORONAVIRUS", "COVID", "Covid", "covid")

			headers = ['uuid','title','date','trending','brexit','covid']

			d_read = DictReader(f)
			d_write = DictWriter(g, fieldnames=headers)
		
			d_write.writeheader()

			for row in d_read:
				if any(x in row["title"] for x in cov):
					row["covid"] = 1
					d_write.writerow(row)
				else:
					row["covid"] = 0
					d_write.writerow(row)

		print("Modification complete")
		f.close()
		g.close()

	@classmethod
	def reset(self):
		# Open csv and truncate
		filename = "temp.csv"
		f = open(filename, "w+")
		f.close()

		# Open csv and truncate
		filename = "scraped_articles.csv"
		f = open(filename, "w+")
		f.close()

		# Open csv and prepare headers
		filename = "scraped_articles.csv"
		f = open(filename, "a+")
		f.write('uuid,title,date,trending')
		f.close()

		# Open csv and truncate
		filename = "modified_articles.csv"
		f = open(filename, "w+")
		f.close()

		# Open csv and prepare headers
		filename = "modified_articles.csv"
		f = open(filename, "a+")
		f.write('uuid,title,date,trending,brexit,covid')
		f.close()

		print("Files reset")

	@classmethod
	def migrateCass(self):
		comm1 = "sudo docker cp modified_articles.csv news-dock:/home/modified_articles.csv"

		normal = subprocess.run(comm1,
			stdout = subprocess.PIPE, stderr = subprocess.PIPE,
			check = True,
			text = True,
			shell = True)
		print(normal.stdout)
		print("Complete!")