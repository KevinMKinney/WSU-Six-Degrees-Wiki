# Description of project:
# This python script web scraps wikipedia, starting from a random wiki page (given from 'https://en.wikipedia.org/wiki/Special:Random') to the wiki page of Star Wars. It does this by using recursive depth first search (depth of 6) to find a path.

import requests
from bs4 import BeautifulSoup
import re
import sys

# pathArray is global array that stores the path of links
pathArray = []
# these are for internal_not_special function (prob faster)
re_wiki = re.compile('^/wiki/')
re_word1 = re.compile('/\w+:')
re_pound = re.compile('#')

# function that returns the url from a random Wikipedia page
def get_random_page_url():
	r = requests.get('https://en.wikipedia.org/wiki/Special:Random')
	return r.url

# function that checks for valid internal links (i.e. links to other wiki pages)
def internal_not_special(href):
	if href:
		# is it a Wikipedia link
		if re_wiki.search(href):
			# ignore category type links
			if not re_word1.search(href):
				if not re_pound.search(href):
					return True
	return False
	
# function that used DFS recusively to find a path to Star Wars 
def recursiveSearch(links, search):
	# init global variable(s)
	global pathArray
	# iterate through internal links
	for i in links: 
		try:
			# get href of link
			href = str(i['href'])
			# check if link is valid
			if internal_not_special(href):
				# check if link is Star Wars
				if href == '/wiki/Star_Wars':
					# add to path
					pathArray.append(i)
					return True
				else:
					# base case / is the next recusive call valid
					if search-1 > 0:
						# find internal links...
						l = findInternalLinks("https://en.wikipedia.org" + href)
						# ...and search through them
						if recursiveSearch(l, search-1):
							# add link to path and stop searching only if it found Star Wars
							pathArray.append(i)
							return True
		except KeyError:
			# occasionally looks at non-valid links and causes a keyError
			pass
		except:
			# for testing purposes (its a bad thing if its in here)
			e = sys.exc_info()[0]
			#print(e)
	# only return false if it could not find a path to Star Wars
	return False

# function converts url to list of internal links in that url
def findInternalLinks(url):
	# get contents of url
	page = BeautifulSoup(requests.get(url).text, 'html.parser')
	# find contents only in the main body of page
	mainBody = page.find(id="bodyContent")
	# return links in main body
	return mainBody.find_all('a')

def main():
	# init global variable(s)
	global pathArray
	# increase recusion limit 
	sys.setrecursionlimit(10000)
	# get starting url
	start = get_random_page_url()
	# manual starting url
	#start = "https://en.wikipedia.org/wiki/George_Lucas"
	
	# set depth of DFS
	depth = 6
	# find internal links in starting url
	links = findInternalLinks(start)
	# start searching for Star Wars	
	s = recursiveSearch(links, depth)

	# add starting page to the path array
	first_page = BeautifulSoup(requests.get(start).text, 'html.parser')
	first = {'title': first_page.title.string.strip("- Wikipedia"), 'href': re.sub("https://en.wikipedia.org", "", start)}
	pathArray.append(first)
	# reverse path array for printing
	pathArray.reverse()
	# print the contents of path array
	# syntaxt is "page title" (
	for i in range(len(pathArray)):
		print(str(pathArray[i]['title']) + " (https://en.wikipedia.org" + str(pathArray[i]['href']) + ")")
	

if __name__ == "__main__":
	main()
