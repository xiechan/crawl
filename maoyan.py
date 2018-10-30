# -*- coding: utf-8 -*-
# @File  : maoyan.py
# @Author: Vivian
# @Desc  :猫眼电影top100
import requests
import re
import json
from multiprocessing import Pool

from requests.exceptions import RequestException

def get_one_page(url):
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response
        return None
    except RequestException:
        return None


def analysis_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6]
        }

def write_res(txt):
    with open('maoyanTop100.text','a',encoding='utf-8') as f:
        f.write(json.dumps(txt,ensure_ascii=False)+'\n')
        f.close()

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in analysis_one_page(html):
        write_res(item)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i*10 for i in range(10)])
    pool.close()
    pool.join()