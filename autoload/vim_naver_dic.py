## sudo pip install python-vlc wget
from __future__ import print_function
import json
import requests
import wget
from bs4 import BeautifulSoup
import vlc

DIC_URL = "https://endic.naver.com/search.nhn?sLn=kr&searchOption=all&query="
PAPAGO_URL = "https://openapi.naver.com/v1/papago/n2mt"

class AngaeNaverDic:
	def __init__(self):
		''' Constructor for this class. '''
		self.dic_url = DIC_URL
		self.papago_url = PAPAGO_URL
		self.search_sentence = ''
		self.search_word = ''
		self.soup = None
		self.search_result = ''
		self.papago_result = ''

	def get_http_soup(self, word):
		if word:
			self.search_word = word

		if self.search_word:
			res = requests.get(self.dic_url + self.search_word)
			self.soup = BeautifulSoup(res.text, 'html.parser')
		else:
			self.search_result = 'No search word exists'

	def search_papago(self, to, sentence):
		self.search_sentence = sentence
		headers = {"X-Naver-Client-Id": "zAPmLQev4f8FVxVowF7O", "X-Naver-Client-Secret": "wrXgfiqNXw"}
		if to == 'ko':
			params = {"source": "en", "target": "ko", "text": self.search_sentence}
		else:
			params = {"source": "ko", "target": "en", "text": self.search_sentence}
		response = requests.post(self.papago_url, headers=headers, data=params)
		# convert json to python dict
		self.papago_result = response.json()
		# self.papago_result = json.loads(response.json())
		return self.papago_result['message']['result']['translatedText']

	def search_naver_dic(self, word):
		self.get_http_soup(word)

		try:
			word_box = self.soup.select('.word_num .list_e2')[0]
		except IndexError:
			self.search_result = '"{}"에 대한 검색결과가 없습니다.'.format(word)
			return self.search_result

		info = word_box.find('dd').find('p')

		if info.find('span')['class'][0] == 'fnt_k05':
			# 한영
			word_class = None
		else:
			# 영한
			word_class = word_box.select('dd p .fnt_k09')[0].text

		## get phonetic alphabet
		phonetic_alpha = word_box.select('.fnt_e25')
		phonetic_count = len(phonetic_alpha)
		phonetic_alpha_us = phonetic_alpha_uk = phonetic_alpha[0].text
		if phonetic_count == 2:
			phonetic_alpha_uk = word_box.select('.fnt_e25')[1].text

		## get audio file
		audio_url = word_box.select('.btn_side_play')[0].attrs['playlist']
		local_audio_filename = wget.download(audio_url, '/tmp/surpass.mp3')
		p = vlc.MediaPlayer("file://" + local_audio_filename)
		p.play()

		meaning = word_box.select('dd p .fnt_k05')[0].text

		try:
			example = word_box.select('dd p .fnt_e07._ttsText')[0].text
		except IndexError:
			example = None

		self.search_result += '"{}"에 대한 검색결과\n'.format(word)
		# self.search_result += '='*80

		if phonetic_alpha_us:
			self.search_result += ' {} \n'.format(phonetic_alpha_us)

		if phonetic_alpha_uk:
			self.search_result += ' {} \n'.format(phonetic_alpha_uk)

		if word_class:
			self.search_result += '품사: {}\n'.format(word_class)
		self.search_result += '의미: {}\n'.format(meaning)

		if example:
			self.search_result += '예문: {}\n'.format(example)

		return self.search_result

def get_naver_dic(word='none'):
	dicstring = AngaeNaverDic().search_naver_dic(word)
	return dicstring

def get_naver_papago(to='ko', text='none'):
	papagostring = AngaeNaverDic().search_papago(to, text)
	return papagostring


