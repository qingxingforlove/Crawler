import lxml
import requests
from lxml import etree

#etree.parse()          解析.html文件
#etree.HTML()           构造了一个XPath解析对象并对HTML文本进行自动修正
#etree.tostring()：     输出修正后的结果，类型是bytes
class Login(object):
    '''
    Login类可以模拟登陆
    '''
    def __init__(self):
        '''
        初始化登陆页面，个人信息页面，会话
        '''
        self.headers = {
            'Referer':'https://github.com/',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            'Host':'github.com'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/login/session'
        self.logined_url = 'https://github.com/settings/profile'
        self.session = requests.Session()

    def token(self):
        '''
        请求登陆页时候，获取token信息
        '''
        response = self.session.get(self.login_url, headers=self.headers)
        selector = etree.HTML(response.text)

        #打印selector内容
        print('selector:', selector)

        token = selector.xpath('//div//input[2]/@value')

        #打印token
        print(token)
        return token

    def login(self, email, password):
        '''
        请求登陆session页面
        '''
        post_data = {
            'commit': 'Sign in',
            'utf8':'✓',
            'authenticity_token': self.token(), #调用token方法
            'login': email,
            'password': password,
            'webauthn-support': 'supported'
        }
        #打印post_data信息
        print(post_data)

        response1 = self.session.post(self.post_url, data=post_data, headers=self.headers)
        
        if response1.status_code == 200:
            self.dynamics(response1.text)
        else:
            print('请求失败,失败状态码为%s' % response1.status_code)
        

        response2 = self.session.get(self.logined_url, headers=self.headers)
        if response2.status_code == 200:
            self.profile(response2.text)
        else:
            print('请求失败,失败状态码为%s' % response2.status_code)

    def dynamics(self, html):
        selector = etree.HTML(html)
        dynamics = selector.xpath('//div[contains(@class, "news")]//div[contains(@class, "alert")]')
        print(dynamics)
        for item in dynamics:
            dynamic = ' '.join(item.xpath('.//div[@class="title"]//text()')).strip()
            #print(dynamic)
            print('---2---')
    
    def profile(self, html):
        selector = etree.HTML(html)
        print(selector)
        name = selector.xpath('//input[@id="user_profile_name"]/@value')
        email = selector.xpath('//select[@id="user_profile_email"]/option[@value!=""]/text()')
        print('name:', name, 'email:', email)

if __name__ =="__main__":
    login = Login() #实例化对象
    login.login(email='1749346256@qq.com', password='whywhy123-') #发送请求
        



