import requests
import urllib
import urllib.request
import re
from bs4 import BeautifulSoup
import json
import time

#url = 'https://mangapark.net/manga/lady-long-legs/i1859014/c1'
url = 'http://www.qizuang.com/gonglue/dengju/87151.html'

#模拟浏览器
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

#获取网页的全部信息
response  = requests.get(url = url, headers = headers)
#把正则字符串编译成正则表达式对象
pattern = re.compile(r'http://[^\s]*.jpg')
images = re.findall(pattern, repr(response.content))

#下载图片
count = 1
for img in images:
    print('----开始循环----')
    image = requests.get(url = img, headers = headers).content
    print('----3----')
    with open (r'F:/xfmovie/comics/lady_long_legs/1/%s.jpg' % count, "wb") as fp:
        print("DOWNLOADING %d picture ..." % count)
        fp.write(image)
        count += 1
print('下载完成')


#picture_sre = "https://xy-21-w.mangapark.net/18/ad/5c4998c43f19dc29fc51da81/001_14546_720_500.webp"
#picture_sre = 'https://xy-21-w.mangapark.net/18/ad/5c4998c43f19dc29fc51da81/006_44284_720_700.webp'
#picture_sre = 'https://xy-21-w.mangapark.net/18/ad/5c4998c43f19dc29fc51da81/121_39214_720_700.webp'
#soup = BeautifulSoup(r.text, 'html.parser')
