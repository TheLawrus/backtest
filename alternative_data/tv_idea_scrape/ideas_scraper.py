from bs4 import BeautifulSoup as bs
import requests
import csv
import numpy as np
from datetime import datetime
import time


#It may be beneficial to strip all html elements (<div>, <span>, <img>) and formating to just keep text


#getting the number of posts per page
def get_post_titles(_page, _src):
	url = _src.format(_page)
	page = requests.get(url)
	soup = bs(page.content, features="lxml")
	post_titles = soup.find_all(class_='tv-widget-idea__title')
	return post_titles

#Function to return raw content of TV Idea post
def get_post(_page, _post_title):
	post_url = "https://www.tradingview.com/chart" + str(_post_title['href'])
	post_page = requests.get(post_url)
	post_soup = bs(post_page.content, features="lxml")

	#Unprocessed TV Idea Post Data
	post_content = post_soup.find_all(class_='tv-chart-view__description')[0].get_text(strip=True, separator='   ').encode("ascii","ignore").decode("utf-8")
	post_unix = str.split(str(post_soup.find_all(class_='tv-chart-view__title-time')[-1]), 'data-timestamp="')[-1]
	post_unix = float(str.split(post_unix, '"')[0])
	post_time = datetime.utcfromtimestamp(post_unix).strftime('%Y-%m-%d %H:%M:%S') #UTC Time String

	return post_url, post_time, post_unix, post_content

#actually collecting data
def collect_data(_pages, _days_back, _src, _outfile):
	header_file = ['Time (UTC)', 'Post URL', 'Post Content']
	idea_files = []
	for i in range(_pages):
		post_titles = get_post_titles(i+1, _src)
		for j in range(len(post_titles)):
			print("Page: {} Post:{}".format(i+1, j))
			post_url, post_time, post_unix, post_content = get_post(i, post_titles[j])

			if (time.time() - post_unix) / 86400 <= _days_back:
				idea_files.append([post_time, post_url, post_content])
			else:
				print("rejected:", post_time)

	#Saving the scraped ideas, note that this overwrites previous data
	with open(_outfile, 'w', newline='') as myfile:
		wr = csv.writer(myfile)
		wr.writerow(header_file)

		for idea in idea_files:
			print(idea)
			wr.writerow(idea)

#Collecting data on first 10 pages of stock idea posts from last 14 days
collect_data(100, 14, "https://www.tradingview.com/markets/stocks-usa/ideas/page-{}/", 'scraped_stock_ideas_pg0-100.csv')
