from lxml import etree
import os
import requests

url = "https://mangapark.net/manga/lady-long-legs/i1859043/c23"

html = etree.parse(requests.get(url).text, etree.HTMLParser())
results = html.xpath('//a[@class="img-num"/href]')

get_images = []

for result in results:
    get_images.append(result)
    print(length(get_images))
#print(get_images)

file_path = r'F:/xfmovie/comics/lady_long_legs/100/'
if not os.path.exists(file_path):
    os.makedirs(file_path)

for img in get_images:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    response = requests.get(url=img, headers=headers).content
    with open(r'F:/xfmovie/comics/lady_long_legs/100/%s.jpg' % num, 'wb') as fb:
        fb.write(res)
        print("正在下载第%s张图片" % num)
        num += 1
print("下载完成")

