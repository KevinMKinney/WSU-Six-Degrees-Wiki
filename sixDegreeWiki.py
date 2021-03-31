import requests
from bs4 import BeautifulSoup
import re

def get_random_page_url():
	r = requests.get('https://en.wikipedia.org/wiki/Special:Random')
	return r.url

def internal_not_special(href):
	if href:
		# This works while line 14 does not (dont know why)
		r = re.compile('^/wiki/')
		if r.search(href):
		#if re.compile('ˆ/wiki/').search(href):
			if not re.compile('/\w+:').search(href):
				if not re.compile('#').search(href):
					return True
	return False
	
def recusiveSearch(mainBody, maxSearch):
	if maxSearch <= 0:
		return False
	for link in mainBody:
		print(link)
		if link == 'https://en.wikipedia.org/wiki/Star_Wars':
			print("Found it")
			return True
		return recusiveSearch(link, maxSearch-1)
	return False

def main():
	# get starting url
	#start = get_random_page_url()
	start = ("https://en.wikipedia.org/wiki/George_Lucas")

	page = BeautifulSoup(requests.get(start).text, 'html.parser')
	#page = start
	#print(page.text)
	pageTitle = page.find('h1', id="firstHeading").string
	print(pageTitle)
	mainBody = page.find(id="bodyContent")
	#print(mainBody)	
	#links = mainBody.find_all('a', href=internal_not_special)
	links = mainBody.find_all('a')
	#for link in links:
	#	print(internal_not_special(link.href))
	#print(links)
	for i in links: 
		try:
			href = str(i['href'])
			#print(href)
			if internal_not_special(href):
				print(href)
		except:
			pass	
	#s = recusiveSearch(links, 6)
	#print(s)

if __name__ == "__main__":
	main()
