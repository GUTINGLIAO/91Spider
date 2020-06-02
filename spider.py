import hashlib
import re

import requests
from bs4 import BeautifulSoup


def save_image(url, name):
    r = requests.get(url)
    print('./img/' + name + '.jpg', 'wb')
    with open('./img/' + name + '.jpg', 'wb') as f:
        f.write(r.content)


def spider_main(page):
    url = 'http://f.wonderfulday25.live/forumdisplay.php'
    data = {
        'fid': 19,
        'page': page,
    }
    print('爬取第' + str(page) + '页')
    try:
        response = requests.get(url, params=data).content
        soup = BeautifulSoup(response, 'lxml')
        soup1 = soup.find_all('a', title='新窗口打开')
        for a in soup1:
            spider_each(a['href'])
    except Exception as e:
        print(e)


def spider_each(href):
    url = 'http://f.wonderfulday25.live/' + href
    print(url)
    head = {
        'Referer': 'http://f.wonderfulday25.live/forumdisplay.php?fid=19',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }
    response = requests.get(url, headers=head).content
    soup = BeautifulSoup(response, 'lxml')
    imgs = soup.find_all('img', file=re.compile('http://pic.workgreat*'))
    for img in imgs:
        print(img['file'])
        m2 = hashlib.md5()
        m2.update(str(img['file']).encode('utf-8'))
        save_image(img['file'], m2.hexdigest())


if __name__ == '__main__':
    for i in range(2, 500):
        spider_main(i)
