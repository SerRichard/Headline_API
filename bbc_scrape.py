# BBC News daily web scraper
# Author Sean Hoyal, 2020
#
# Get the headlines in time for coffee!
#
# Imports
import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import schedule
import time

def scrape():
	my_url = 'https://www.bbc.co.uk/news'

#Opens connection, downloads page, then closes connection
	uReqBBC = uReq(my_url)
	bbc_html = uReqBBC.read()
	uReqBBC.close()

# Parse into beautiful soup, place all of a particular class into containers
	news_soup = soup(bbc_html, "html.parser")

	containers = news_soup.findAll("div",{"class":"gs-c-promo nw-c-promo gs-o-faux-block-link gs-u-pb gs-u-pb+@m nw-p-default gs-c-promo--inline gs-c-promo--stacked@m gs-c-promo--flex"})

# Prepare csv to record data
	filename = "daily_articles.csv"
	f = open(filename, "a")

	headers = "title, summary, date\n"

	f.write(headers)

# Loop through containers, extracting titles, summaries and times
	for container in containers:
		title_container = container.findAll("h3", {"class":"gs-c-promo-heading__title gel-pica-bold nw-o-link-split__text"})
		title = title_container[0].text

		try:	
			summary_container = container.findAll("p", {"class":"gs-c-promo-summary gel-long-primer gs-u-mt nw-c-promo-summary"})
			summary = summary_container[0].text
		except IndexError:	
			summary = "N/A"
		
		try:
			date = container.time["datetime"]
		except TypeError:
			date = "N/A"
# Print findings
		print("Article title: " + title)
		print("Summary: " + summary)
		print("Date published: " + date)

# Write findings to csv and close connection to file
		f.write(title.replace(",", "|") + ","  +  summary.replace(",", "|") + "," + date + "\n")

	f.close()

# Schedule scrape to occur daily @ 7am
schedule.every().day.at("07:00").do(scrape)

while True:
	schedule.run_pending()
	time.sleep(0.5)

if __name__ == '__main__':
	scrape()
