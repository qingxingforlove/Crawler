import requests
import urllib
import urllib.request
import re
from bs4 import BeautifulSoup
import json
import time

#定义下载页面函数
def load_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    response = requests.get(url = url, headers = headers)
    data = response.content
    return data

#定义保存图片的函数
def get_image(html):
    regx = r'http://[^\s]*.jpg'
    pattern = re.compile(regx)
    get_images = re.findall(pattern, repr(html))
    print(get_images)

    num = 1
    for img in get_images:
        print('---2---')
        image = load_page(img)
        print('---3---')
        with open(r'F:/xfmovie/comics/lady_long_legs/1/%s.jpg' % num, 'wb') as fb:
            
            fb.write(image)
            print("正在下载第%s张图片" % num)
            num += 1
    print("下载完成")

url = 'http://www.qizuang.com/gonglue/dengju/87151.html'
html = load_page(url)
get_image(html)




