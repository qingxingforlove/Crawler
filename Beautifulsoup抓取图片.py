import requests
from bs4 import BeautifulSoup
import os
import re

def main():
    url = 'https://mangapark.net/manga/lady-long-legs/i2107502/c44'
    html = requests.get(url).text
    soup = BeautifulSoup(html, "lxml")
    soup.prettify()
    
    #创建存储链接的空字典
    get_images = []

    #自定义一个匹配方法
    def has_class_no_id(tag):
        return tag == 'a' and tag.has_attr('class') and not tag.has_attr('id')


    #循环链接
    links1 = soup.find_all(script=re.compile("https:\/\/xy-21-w.mangapark.net\/4c\/9a\/5c9f6c5682606176becaa9c4"))
    print(links1)
    links2= soup.find_all('a', class_='img-num')
    print(links2)

    for link in links:
        print(link['href'])
        get_images.append(link['href'])

    print(get_images)
    for img in get_images:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        res = requests.get(url=img, headers=headers).content
        file_path = r'F:/xfmovie/comics/lady_long_legs/43/'
        num = 1
        if not os.path.exists(file_path):
            os.makedirs(file_path)
            
            with open(r'F:/xfmovie/comics/lady_long_legs/43/%s.jpg' % num, 'wb') as fb:
                fb.write(res)
                print("正在下载第%s张图片" % num)
                num += 1
        else:
            with open(r'F:/xfmovie/comics/lady_long_legs/44/%s.jpg' % num, 'wb') as fb:
                fb.write(res)
                print("正在下载第%s张图片" % num)
                num += 1
        print("下载完成")

if __name__ =='__main__':
    main()

