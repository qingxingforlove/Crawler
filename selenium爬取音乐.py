#coding=utf-8 
import selenium
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
import time
import urllib

mname = ''
#JS重定向
def wait(driver):
    elem = driver.find_element_by_tag_name('html')
    count = 0
    while True:
        count += 1
        if count > 20:
            print('超时')
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name('html')
        except StaleElementReferenceException:
            return

def get_url():
    input_string = input('小情歌')
    url = 'https://www.kugou.com/'
    driver = webdriver.Firefox(executable_path='D:\Personal\Desktop\geckodriver')
    driver.get(url)
    s = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[1]/input')
    s.send_keys(input_string.decode('gbk'))
    driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[1]/div/i')
    result_url = driver.current_url
    driver.quit
    return result_url

def show_results(url):
    driver = webdriver.Firefox(executable_path='C:\Users\Administrator\Desktop\chromedriver.exe')
    driver.get(url)
    time.sleep(2)
    for i in range(1,10):
        try:
            print(driver.find_element_by_xpath('/html/body/div[5]/div[1]/div[2]/ul[2]/li[%d]/div[1]/a').get_attribute('title') % i)
        except NoSuchElementException as msg:
            break
    global mname
    mname = driver.find_elements_by_xpath('/html/body/div[5]/div[1]/div[2]/ul[2]/li[%d]/div[1]/a').get_attribute('title') % i
    a = driver.find_elements_by_xpath('/html/body/div[5]/div[1]/div[2]/ul[2]/li[%d]/div[1]/a').get_attribute('title') % i
    actions = ActionChains(driver)
    actions.move_to_element(a)
    actions.click(a)
    actions.perform()
    driver.switch_to_window(driver.window_handles[1])  #跳转到新打开的页面
    result = driver.find_element_by_xpath(".//*[@id='myAudio']").get_attribute('src') #获取播放元文件url
    driver.quit()
    return result
#下载回调
def cbk(a, b, c):
    per = 100.0 * a * b / c  
    if per > 100:
        per = 100
    print('%.2f%%' % per)

def main():
    print('欢迎使用GREY音乐下载器')
    time.sleep(1)
    while True:
        url = get_url()
        result = show_results(url)
        if result == 'quit':
            print('\n')
            continue
        else:
            local = 'd://%s.mp3'%mname
            print('download start')
            time.sleep(1)
            urllib.urlretrieve(result, local, cbk)
            print('finish downloading %s.mp3'%mname + '\n')

if __name__ == '__main__':
  main()  