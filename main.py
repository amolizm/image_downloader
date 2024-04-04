from bs4 import BeautifulSoup
import requests
import os
from urllib.parse import urljoin, urlparse
import concurrent.futures
import time

default_path = 'image_downloader'
if not os.path.exists(default_path):
    os.mkdir(default_path)

start = time.time()
start_pn = 1
page_count = 5

def download_images(url):
    folder = default_path + '/' + url.split("://")[1].replace(':', '-').replace('?', '-').replace('=', '-').replace('/', '-')
    if not os.path.exists(folder):
        os.mkdir(folder)

    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36', 'Referer': 'https://www.google.com/', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-User': '?1', 'Sec-Fetch-Dest': 'document', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'}
    cont=requests.get(url, headers=headers).content

    soup=BeautifulSoup(cont,'html.parser')
    imgall=soup.find_all('img')
    
    local_todo = []
    for img in imgall:
        try:
            imgsrc=img['data-srcset']
        except:
            try:
                imgsrc=img['data-src']
            except:
                try:
                    imgsrc=img['data-fallback-src']
                except:
                    try:
                        imgsrc=img['src']
                    except:
                        pass
        full_url = urljoin(url, imgsrc)
        base_name = os.path.basename(urlparse(full_url).path)
        local_todo.append([folder + '/' + base_name, full_url])
    print(f'images from {url} fetched')
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_todo, local_todo)
    print(f'completed downloading from {url}')

def download_todo(pair):
    path = pair[0]
    url = pair[1]
    r=requests.get(url).content
    with open(path,'wb+') as f:
        f.write(r)

def get_url():
    urls = []
    for i in range(start_pn, page_count+1):
        urls.append(f"https://www.zerochan.net/?p={i}")
    return urls

if __name__ == '__main__':
    start_pn = int(input("Start from page: "))
    page_count = int(input("Pages to scan: "))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_images, get_url())

print(f'completed in {int(time.time() - start)} seconds')
