import requests
import time
import os

from selenium import webdriver

def main():
    #实例化一个浏览器对象
    driver = webdriver.PhantomJS()
    url = 'https://mangapark.net/manga/lady-long-legs/i1859018/c5'

    #进入要爬取的页面
    driver.set_page_load_timeout(10)
    try:
        driver.get(url)
    except:
        print('！！！！！！time out after 10 seconds when loading page！！！！！！')
        driver.execute_script("window.stop()")

    #获取图片链接
    links = driver.find_elements_by_xpath('//a[@class="img-num"]')

    #关闭浏览器对象
    #driver.quit()

    #创建一个存储图片链接的空列表
    get_images = []

    #把图片链接存储进去
    for i in links:
        get_images.append(i.get_attribute('href'))

    #验证是否获取到图片链接
    print(get_images)
    print(get_images[0])

    #判断文件夹是否存在
    file_path = r'F:/xfmovie/comics/lady_long_legs/5/'
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    #根据链接，循环下载图片
    num = 1
    for img in get_images:
        #浏览器请求头
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        '''
        proxy = '112.85.131.238:9999'
        proxies = {
            'http':'http://' + proxy,
            'https':'https://' + proxy,
        }
        '''
        try:
            response = requests.get(url=img, headers=headers)
            print('---1---')
        except requests.exceptions.ConnectionRefusedError as e:
            print("---2---")
        else:
            res = response.content
            #print(type(res))
    
        with open(r'F:/xfmovie/comics/lady_long_legs/5/%s.jpg' % num, 'wb') as fb:
            fb.write(res)
            print("正在下载第%s张图片" % num)
            num += 1
    print("下载完成")

if __name__ =='__main__':
    main()

