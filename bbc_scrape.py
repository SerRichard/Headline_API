import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

my_url = 'https://www.bbc.co.uk/news'

#Opens connection, downloads page, then closes connection
uReqBBC = uReq(my_url)
bbc_html = uReqBBC.read()
uReqBBC.close()

news_soup = soup(bbc_html, "html.parser")

containers = news_soup.findAll("div",{"class":"gs-c-promo nw-c-promo gs-o-faux-block-link gs-u-pb gs-u-pb+@m nw-p-default gs-c-promo--inline gs-c-promo--stacked@m gs-c-promo--flex"})

filename = "daily_articles.csv"
f = open(filename, "w")

headers = "title, summary, date\n"

f.write(headers)

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

	print("Article title: " + title)
	print("Summary: " + summary)
	print("Date published: " + date)
	
	f.write(title + ","  +  summary.replace(",", ";") + "," + date + "\n")

f.close()
