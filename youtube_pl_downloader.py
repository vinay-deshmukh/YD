import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
import sys
import time

start_time = 0
url_pl = 'https://www.youtube.com/playlist?list=PLObNowOPccbtYbBNOmIlz0zb8OeoQlNlU'

def get_title(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	h1 = soup.find_all('h1', {'class' : 'watch-title-container'})[0]
	yt_formatted_string = h1.find('span')
	return yt_formatted_string.text.rstrip()

def get_videos_href(url_pl):
	page_pl = requests.get(url_pl)
	soup = BeautifulSoup(page_pl.text, 'html.parser')

	pl_videos = set()
	for a in soup.find_all('a'):#, {'id': 'thumbnail' }):
		if a.get('href').startswith('/watch'):
			pl_videos.add('https://youtube.com' + a.get('href').split('&')[0])

	return pl_videos

def reporthook(count, block_size, total_size):
	global start_time
	if count == 0:
		start_time = time.time()
		return
		
	duration = time.time() - start_time

	progress_size = int(count * block_size)

	speed = int(progress_size / (1024 * duration))

	percent = min(int(count*block_size*100/total_size),100)

	sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
	                (percent, progress_size / (1024 * 1024), speed, duration))
	sys.stdout.flush()

def save(url, filename):
	resp = urlopen(Request(url, method='HEAD'))
	headers = resp.info()
	urllib.request.urlretrieve(url, filename, reporthook)


def download(video_list):
	
	for video in video_list:
		video = video.replace(':', '%3A').replace('/', '%2F').replace('?', '%3F').replace('=', '%3D')

	for i in range(len(video_list)):
		title = ''.join(list(get_title(video_list[i]))[5:])
		savedeo = 'https://savedeo.site/download?url=' + video_list[i]
		page = requests.get(savedeo)


		soup = BeautifulSoup(page.text, 'html.parser')	

		for a in soup.find_all('a', {'class': 'download-button'}):
			url = a.get('href')
			break


		print('Downloading {}'.format(title))
		file_name = title + '.mp4'
		save(url, file_name)
		print('\nDownload complete')
		print('-'*15)


def main():
	vid_list = list(get_videos_href(input('Enter playlist url: ')))
	download(vid_list)

if __name__ == '__main__':
	main()



