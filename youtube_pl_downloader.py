import requests
from bs4 import BeautifulSoup

url_pl = 'https://www.youtube.com/playlist?list=PLObNowOPccbtYbBNOmIlz0zb8OeoQlNlU'

def get_videos_href(url_pl):
	page_pl = requests.get(url_pl)
	soup = BeautifulSoup(page_pl.text, 'html.parser')

	pl_videos = set()
	for a in soup.find_all('a'):#, {'id': 'thumbnail' }):
		if a.get('href').startswith('/watch'):
			pl_videos.add('https://youtube.com' + a.get('href').split('&')[0])

	#from pprint import pprint as pp
	#pp(pl_videos)

	return pl_videos

def download_video(video):
	video = video.replace(':', '%3A').replace('/', '%2F')\
	.replace('?', '%3F').replace('=', '%3D')

	savedeo = 'https://savedeo.site/download?url=' + video
	page = requests.get(savedeo)
	#print(page.content)

	soup = BeautifulSoup(page.text, 'html.parser')

	print(len(soup.find_all('a', {'class': 'download-button'})))
	

	for a in soup.find_all('a', {'class': 'download-button'}):
		print(a.get('href'))
		url = a.get('href')
		break

	import urllib.request
	print('DOWNLOADING FILE')
	file_name = 'answering-your-queries.mp4'
	urllib.request.urlretrieve(url, file_name)
	print('download done')

	# https://savedeo.site/download?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D2xrcas1YDkU
	# https://www.youtube.com/watch?v=2xrcas1YDkU&list=PLObNowOPccbtYbBNOmIlz0zb8OeoQlNlU

#download_video('https://www.youtube.com/watch?v=2xrcas1YDkU')


vid_list = get_videos_href(input('Enter playlist url: '))




