from bs4 import BeautifulSoup as bs
import requests
import csv
import numpy as np
from datetime import datetime


#It may be beneficial to strip all html elements (<div>, <span>, <img>) and formating to just keep text


#getting the number of posts per page
def get_post_titles(_page):
	url = "https://www.tradingview.com/ideas/page-{}/".format(_page)
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
	print(post_content)
	post_unix = str.split(str(post_soup.find_all(class_='tv-chart-view__title-time')[-1]), 'data-timestamp="')[-1]
	post_unix = float(str.split(post_unix, '"')[0])
	post_time = datetime.utcfromtimestamp(post_unix).strftime('%Y-%m-%d %H:%M:%S') #UTC Time String

	return post_url, post_time, post_content

#actually collecting data
def collect_data(_pages):
	header_file = ['Post URL, Time (UTC), Post Content']
	idea_files = []
	for i in range(_pages):
		post_titles = get_post_titles(i+1)
		for j in range(len(post_titles)):
			post_url, post_time, post_content = get_post(i, post_titles[j])
			idea_files.append([post_time, post_url, post_content])

	#Saving the scraped ideas, note that this overwrites previous data
	with open('scraped_ideas.csv', 'w', newline='') as myfile:
		wr = csv.writer(myfile)
		wr.writerow(header_file)

		for idea in idea_files:
			print(idea)
			#print(''.join(idea.encode('unicode_escape').decode('ascii')))
			#wr.writerow(''.join(idea.encode('unicode_escape').decode('ascii')))
			wr.writerow(idea)

     #np.savetxt("scraped_ideas.csv", idea_files, delimiter =", ", fmt ='% s')

#Collecting data on first 2 pages of idea posts
collect_data(2)
