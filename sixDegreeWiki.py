import requests
from bs4 import BeautifulSoup
import re

def get_random_page_url():
	r = requests.get('https://en.wikipedia.org/wiki/Special:Random')
	return r.url

def internal_not_special(href):
	if href:
		if re.compile('ˆ/wiki/').search(href):
			if not re.compile('/\w+:').search(href):
				if not re.compile('#').search(href):
					return True
	return False

def main():
	# get starting url
	#start = get_random_page_url()
	start = ("https://en.wikipedia.org/wiki/George_Lucas")

	page = BeautifulSoup(requests.get(start).text, 'html.parser')
	#page = start
	#print(page.text)
	# seach through page links
	# check if link is valid
	# check if link is the like to find
	pageTitle = page.find('h1', id="firstHeading").string
	print(pageTitle)
	mainBody = page.find(id="bodyContent")
	#print(mainBody)
	
	#mainBody.find_all('a', href=internal_not_special)

if __name__ == "__main__":
	main()
