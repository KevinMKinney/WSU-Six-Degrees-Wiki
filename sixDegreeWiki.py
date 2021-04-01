import requests
from bs4 import BeautifulSoup
import re
import sys

pathArray = []
#visitedLinks = []
re_wiki = re.compile('^/wiki/')
re_word1 = re.compile('/\w+:')
re_pound = re.compile('#')

def get_random_page_url():
	r = requests.get('https://en.wikipedia.org/wiki/Special:Random')
	return r.url

def internal_not_special(href):
	if href:
		# This works while line 14 does not (dont know why)
		#r = re.compile('^/wiki/')
		if re_wiki.search(href):
		#if re.compile('ˆ/wiki/').search(href):
			#if not re.compile('/\w+:').search(href):
			if not re_word1.search(href):
				#if not re.compile('#').search(href):
				if not re_pound.search(href):
					return True
	return False
	
def recursiveSearch(links, search):
	global pathArray
	#global visitedLinks
	print("Search:",search)
	if search <= 0:
		return False
	for i in links: 
		try:
			#print(str(i['title']))
			href = str(i['href'])
			#print(href)
			if internal_not_special(href):
				#print("visited", visitedLinks)
				#if href in visitedLinks:
					#print('1')
					#return recursiveSearch(findInternalLinks("https://en.wikipedia.org" + href), search-1)
					#pass
				#else:
					#print(href)
				if href == '/wiki/Star_Wars':
					print('FOUND')
				#if href == '/wiki/Maoism':
					pathArray.append(i)
					return True
				else:
					#print('looking at sublinks')
					if search-1 > 0:
						l = findInternalLinks("https://en.wikipedia.org" + href)
						if recursiveSearch(l, search-1):
							pathArray.append(i)
							return True
					#return recusiveSearch(l, search - 1)
					#visitedLinks.append(href)
		except KeyError:
			pass
		except:
			e = sys.exc_info()[0]
			print(e)
	
	return False

def findInternalLinks(url):
	page = BeautifulSoup(requests.get(url).text, 'html.parser')
	#print(page.text)
	#pageTitle = page.find('h1', id="firstHeading").string
	#print(pageTitle)
	mainBody = page.find(id="bodyContent")
	#print(mainBody)
	#links = mainBody.find_all('a', href=internal_not_special)
	return mainBody.find_all('a')

def main():
	global pathArray
	
	sys.setrecursionlimit(10000)
	# get starting url
	start = get_random_page_url()
	prefix = "https://en.wikipedia.org"
	#start = "https://en.wikipedia.org/wiki/George_Lucas"
	#start = "https://en.wikipedia.org/wiki/National_Association_of_Professional_Base_Ball_Players"
	depth = 6
	links = findInternalLinks(start)
	#global pathArray = []
	#visitedLinks = []
	
	s = recursiveSearch(links, depth)
	#page = BeautifulSoup(requests.get(start).text, 'html.parser')
	#print(page.text)
	#pageTitle = page.find('h1', id="firstHeading").string
	#first = {'title': pageTitle, 'href': start}
	first_page = BeautifulSoup(requests.get(start).text, 'html.parser')

	first = {'title': first_page.title.string, 'href': start.strip(prefix)}

	pathArray.append(first)
	#print(s)
	pathArray.reverse()
	for i in range(len(pathArray)):
		#print(' ', end='')
		print(str(pathArray[i]['title']) + " (" + prefix + str(pathArray[i]['href']) + ")")
	

if __name__ == "__main__":
	main()
