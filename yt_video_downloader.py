import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
import sys
import time

def get_title(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.text, 'html.parser')
	h1 = soup.find_all('h1', {'class' : 'watch-title-container'})[0]
	yt_formatted_string = h1.find('span')
	return yt_formatted_string.text.rstrip()

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

def download(url):
	# print(get_title(url))
	title = ''.join(list(get_title(url))[5:])
	print(title)
	url = url.replace(':', '%3A').replace('/', '%2F').replace('?', '%3F').replace('=', '%3D')
	savedeo = 'https://savedeo.site/download?url=' + url
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
	url = input('Enter Video Link: ')
	download(url)

if __name__ == '__main__':
	main()