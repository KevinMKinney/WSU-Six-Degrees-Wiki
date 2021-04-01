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
	
def recusiveSearch(links, maxSearch):
	if maxSearch <= 0:
		return False
	for i in links: 
		try:
			href = str(i['href'])
			if internal_not_special(href):
				if href == '/wiki/Star_Wars':
					printLink(i)
					return True
				#recursive call here
				#return recusiveSearch(i, maxSearch-1)
		except:
			pass
	return False
	
def printLink(link):
	title = str(link['title'])
	url = "https://en.wikipedia.org" + str(link['href'])
	print(title + " (" + url + ")")

def main():
	# get starting url
	#start = get_random_page_url()
	start = ("https://en.wikipedia.org/wiki/George_Lucas")

	page = BeautifulSoup(requests.get(start).text, 'html.parser')
	#page = start
	#print(page.text)
	pageTitle = page.find('h1', id="firstHeading").string
	#print(pageTitle)
	mainBody = page.find(id="bodyContent")
	#print(mainBody)	
	#links = mainBody.find_all('a', href=internal_not_special)
	links = mainBody.find_all('a')
	#for link in links:
	#	print(internal_not_special(link.href))
	s = recusiveSearch(links, 6)
	print(s)

if __name__ == "__main__":
	main()
