# Sky News daily web scraper
# Author Sean Hoyal, 2020
#
# Get the headlines in time for coffee!
#
# Imports
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from datetime import datetime
import schedule
import time

# Function to scrape
def scrape():
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
	filename = "sky_daily_articles.csv"
	f = open(filename, "a")
	headers = "title, date, trending\n"
	f.write(headers)

	# Loop for non-trending articles: Sky
	for container in containers:
		try:
			article_titles = container.findAll("span",{"class":"sdc-site-tile__headline-text"})
			title = article_titles[0].text
		except IndexError:
			title = "N/A"
		
		date = datetime.today().strftime('%Y-%m-%d')
		trending = 'No'

		print("Article title: " + title)
		print("Date published: " + date)
		print("Trending: " + trending)

	# Write findings to csv
		f.write(title.replace(",", "|") + ","  +  date + "," + trending + "\n")

	# Loop for the trending articles: Sky
	for trend in trendings:
		trending_titles = trend.findAll("a",{"class":"sdc-site-trending__link"})
		title = trending_titles[0].text

		date = datetime.today().strftime('%Y-%m-%d')
		trending = 'Yes'

		print("Article title: " +  title)
		print("Date published: " + date)
		print("Trending: " + trending)

	# Write findings to csv
		f.write(title.replace(",", "|") + ","  +  date + "," + trending + "\n")

	f.close()

# Schedule scrape to occur daily @ 7am
schedule.every().day.at("07:00").do(scrape)

while True:
	schedule.run_pending()
	time.sleep(0.5)

# Scrape!
if __name__ == '__main__':
	scrape()
