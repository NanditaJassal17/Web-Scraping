import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from urllib.parse import urlparse
import pandas as pd
import csv
import requests
from requests.auth import HTTPBasicAuth

from bs4 import BeautifulSoup
import requests

l=[]
file = open('business.csv', 'w',newline='')
writer = csv.writer(file)

#write title business
writer.writerow(['Name', 'Contact', 'Address','Email','Category','Location'])

#SPIDER TO FETCH LINKS

class DomainCrawlerSpider(scrapy.Spider):
	name = 'business'
	allowed_domains = ['yellowpages.in']
	start_urls = ['http://yellowpages.in/hyderabad/air-conditioners/259853214']

	

	# This spider has one rule: extract all (unique and canonicalized) links, follow them and parse them using the parse_items method
	rules = [
		Rule(
			LinkExtractor(
				allow='catalogue/',
				))

		   ]
	# Method which starts the requests by visiting all URLs specified in start_urls
	#def start_requests(self):
	#	for url in self.start_urls:
	#		yield scrapy.Request(url, callback=self.parse, dont_filter=True)

	# Method for parsing items
	def parse(self, response):
		# The list of items that are found on the particular page
		#items = DomainItem()
		scraped_data =[]
		# Only extract canonicalized and unique links (with respect to the current page)
		links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
		unique_list = set(links)
		final_links = list(unique_list)
		print(len(links))
		print(len(final_links))
		# Now go through all the found links
		for link in final_links:
			url = link.url
			headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'}
			response= requests.get(url, headers=headers)
			
			soup= BeautifulSoup(response.content,'lxml')

			soup.prettify()

			items = soup.select('#MainContent_ulFList > li')

			for item in items:
				try:
				  business_name = item.find("div", class_= "popularTitleTextBlock").text
				except:
				  business_name = 'NA'

				try:
				  business_contact_number = item.find("div", class_='eachPopular').find(class_="eachPopularRight").find(class_='businessContact').text
				except:
				  business_contact_number = 'NA'
					
				try:
				  business_address = item.find("div", class_='eachPopular').find(class_="eachPopularRight").find(class_='businessArea').text
				except:
				  business_address = 'NA'

				try:
				  business_categories = item.find("div", class_='eachPopular').find(class_="eachPopularLeft").find(class_ = 'eachPopularTagsList').text
				except:
				  business_categories = 'NA'

				try:
				  	business_email_address = item.find("div", class_= "eachPopularLink").a.get('href')
				  	business_email_address = business_email_address[7:]
				except:
				  	business_email_address = 'NA'


				try:
				  	business_lat_lon = item.find("div", class_='eachPopular').find(class_="eachPopularRight").find(class_='directionsLocationsBlock').a.get('href')
				  	business_lat_lon = business_lat_lon[33:]
				except:
				  	business_lat_lon = 'NA'
				
				if business_lat_lon not in l:
					l.append(business_lat_lon)
					writer.writerow([business_name, business_contact_number, business_address, business_email_address,business_categories,business_lat_lon])
					print ("=========================")
					print (business_name)
					print (business_contact_number)
					print (business_email_address)
					print (business_address)
					print (business_categories)
					print (business_lat_lon)
				else:
					pass



		

				



				

				#business = [ business_name, business_contact_number, business_address, business_categories ,business_email_address]

				#businesses.append(business)