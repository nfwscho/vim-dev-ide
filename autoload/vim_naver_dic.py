from __future__ import print_function
import requests
from bs4 import BeautifulSoup

def get_http_soup(str):
	request = requests.get("http://m.endic.naver.com/search.nhn?searchOption=all&query=" + (str.replace(' ','%20')))
	content = request.content
	soup = BeautifulSoup(content, "lxml")
	return soup

def get_naver_dic(engword = 'none'):
	bsStart = get_http_soup(engword)
	entry = bsStart.find_all('div' , attrs={'class' : 'entry_search_word top'})
	for eachEntry in entry:
		word = eachEntry.find('div',attrs={'class':"h_word"})
		print(word.text.strip())
		wordMean = eachEntry.find_all('li')
		for eachMean in wordMean:
			print(eachMean.text.strip())

	if eachEntry.find('p',attrs={'class':'example_mean'}):
		wordEx = eachEntry.find('p',attrs={'class':'example_stc'}).find_all('a')
		wordExMean = eachEntry.find('p',attrs={'class':'example_mean'})

		print()
		for eachwordEx in wordEx:
			if eachwordEx.find('em',attrs={'class':"u_hc"}):
				continue
			print(eachwordEx.text, end=' ')
			print()
			print(wordExMean.text.strip())
			print()
	print()

