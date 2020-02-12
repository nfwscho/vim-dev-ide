## sudo pip install python-vlc wget
from __future__ import print_function
import requests
import wget
from bs4 import BeautifulSoup
import vlc


def get_http_soup(str):
	DIC_URL = "https://endic.naver.com/search.nhn?sLn=kr&searchOption=all&query={}".format(str)
	res = requests.get(DIC_URL)
	soup = BeautifulSoup(res.text, 'html.parser')
	return soup


def get_naver_dic(word='none'):
	dicstring = ''
	soup = get_http_soup(word)

	try:
		word_box = soup.select('.word_num .list_e2')[0]
	except IndexError:
		result = '"{}"에 대한 검색결과가 없습니다.'.format(word)
		return result

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

	dicstring += '"{}"에 대한 검색결과'.format(word)
	# dicstring += '='*80

	if phonetic_alpha_us:
		dicstring += ' {} '.format(phonetic_alpha_us)

	if phonetic_alpha_uk:
		dicstring += ' {} '.format(phonetic_alpha_uk)

	if word_class:
		dicstring += '품사: {}'.format(word_class)
	dicstring += '의미: {}'.format(meaning)

	if example:
		dicstring += '예문: {}'.format(example)

	return dicstring

