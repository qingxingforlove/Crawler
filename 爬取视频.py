import requests
import re
from selenium import webdriver
import time
import os




#实例化一个浏览器对象
driver = webdriver.PhantomJS()
url = 'http://www.piaohua.in/webPlay/48669-1-1.html?48669-1-1'

#设置最大加载时间
driver.set_page_load_timeout(10)
try:
    driver.get(url)
except:
    print('！！！！！！time out after 10 seconds when loading page！！！！！！')
    driver.execute_script("window.stop()")

#获取视频的链接
link1 = driver.find_element_by_xpath('//*[@id="playleft"]/iframe[2]')
link1 = link1.get_attribute('src')

print('视频的链接:', link1)

#构造请求
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
response = requests.get(url=link1, headers=headers)
'''
#视频文件的链接
link = driver.find_element_by_xpath('//*[@id="chpobwgycalxmamtei"]')
link = link.get_attribute('src')
print(link)
'''
res = response.content

#保存视频
with open(r'D:/BaiduNetdiskDownload/韩国电影/韩国/酒店目的.swf', 'wb') as f:
    f.write(res)
    print('正在下载视频中...')
print('下载完成')

