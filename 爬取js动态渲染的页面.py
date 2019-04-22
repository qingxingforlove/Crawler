from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import quote


path = r'C:\Users\Administrator\Desktop\chromedriver.exe'
brower = webdriver.Chrome(executable_path=path)
wait = WebDriverWait(brower, 10)
KEYWORD = 'ipad'

def index_page(page):
    '''抓列表页'''
    print('正在爬取', page, '页')
    try:
        url = 'https://s.taobao.com/search?q=' + quote(KEYWORD)  #为了符合url编码，比如把KEYWORD里的&=编码
        brower.get(url)
        #如果页码大于1就跳页
        if page > 1:
            input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
            )  #只接受一个参数，所以传入一个元组,取selector
            submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
            )
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page))
        )
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.m-itemlist .items .item'))
        )
        get_products()
    except TimeoutError:
        index_page(page)

def get_products():
    '''提取商品数据'''
    html = brower.page_source
    #初始化一个pq对象
    doc = pq(html)
    #传入一个css选择器，选取内部m-itemlist，再取内部items，再取内部item。然后多节点遍历获取
    items = doc('.m-itemlist .items .item').items()
    for item in items:
        product{
            'image':item.find('.pic .img').attrs('data-src')
            'price':item.find('.price').text()
            'deal':item.find('.deal-cnt').text()
            'title':item.find('.title').text()
            'shop':item.find('.shop').text()
            'location':item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)
#保存到mongodb
MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_COLLECTION = 'products'
client = pymongo.MongoClient(MONGO_URL)
db = client(MONGO_DB)
def save_to_mongo(result):
    '''
    保存到mongodb
    :param result:结果
    '''
    try:
        if db[MONGO_COLLECTION].insert(result):
            print('存储到mongodb成功')
    except Exception:
        print('存储到mongodb失败')

#遍历代码
MAX_PAGE = 100
def main():
    '''
    遍历所有页面
    '''
    for i in range(1, MAX_PAGE + 1):
        index_page(i)


























    




























