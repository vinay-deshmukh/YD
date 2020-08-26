import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
import sys
import time
import re
import os
import sys


start_time = 0
url_pl = 'https://www.youtube.com/playlist?list=PLObNowOPccbtYbBNOmIlz0zb8OeoQlNlU'


def get_video_url_from_video_id(video_id):
    return "https://www.youtube.com/watch?v={}".format(video_id)


def get_videos_href(url_pl):
    page_pl = requests.get(url_pl)
    soup = BeautifulSoup(page_pl.text, 'html.parser')
    pl_videos = set()
    for string in set(re.findall('"videoId":".+?(?<=")', str(soup))):
        try:
            pl_videos.add(get_video_url_from_video_id(re.search(r'"videoId":"(.+)"', string).group(1)))
        except:
            continue
    return pl_videos


def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
        
    duration = time.time() - start_time

    progress_size = int(count * block_size)

    #speed = int(progress_size / (1024 * duration))

    percent = min(int(count*block_size*100/total_size),100)

    sys.stdout.write("\r...%d%%, %d MB, %d seconds passed" %
                    (percent, progress_size / (1024 * 1024), duration))
    sys.stdout.flush()


def save(url, filename):
    resp = urlopen(Request(url, method='HEAD'))
    headers = resp.info()
    urllib.request.urlretrieve(url, filename, reporthook)


def get_available_title(n):
    while True:
        fname = '{}.mp4'.format(n)
        if not os.path.isfile(get_abs_filepath(fname)):
            return fname
        n += 1


def get_abs_filepath(fname):
    dir_path = './'
    if len(sys.argv) > 1:
        dir_path = sys.argv[1]
    return os.path.join(dir_path, fname)


def download(video_list):
    n = len(video_list)
    print("There are total {} videos".format(n))
    for i in range(1, n + 1):
        savedeo = 'https://savedeo.site/download?url=' + video_list[i - 1]
        page = requests.get(savedeo)

        soup = BeautifulSoup(page.text, 'html.parser')    

        for a in soup.find_all('a', {'class': 'download-button'}):
            url = a.get('href')
            break

        print('Downloading video {}/{}'.format(i, n))
        fpath = get_available_title(i) # use memoization.
        print(fpath)
        save(url, fpath)
        print('\nDownload complete')
        print('-'*15)


def main():
    vid_list = list(get_videos_href(input('Enter playlist url: ')))
    download(vid_list)


if __name__ == '__main__':
    main()

