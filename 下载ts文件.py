import requests
import os,re
import sys
from glob import glob
import time
import urllib.request
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from requests.adapters import HTTPAdapter

#   20180516/BP1Dfyu2/800kb/hls/oJT0cmM4892003.ts 其中一个ts文件地址
# 第一步:通过f12可看到Referer地址如下，其中下载地址:https://www.ixxplayer.com/video.php?url=https://605ziyuan.com/20180516/BP1Dfyu2/index.m3u8
# 第二步:以上下载的文件中有个地址：https://605ziyuan.com/ppvod/2fvnvSeC.m3u8
# 组合成地址：https://605ziyuan.com/ppvod/Q7W3G6T7.m3u8"就可以下载了



#每个ts文件都会有的链接
begin_url = 'https://605ziyuan.com'
length = len(begin_url)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#m3u8地址
url = 'https://605ziyuan.com/ppvod/5PNzE7pL.m3u8'

#获取请求数据
response = requests.get(url)
all_content = response.text
print(all_content)

#按照结尾换行符切片
file_line =  all_content.split("\n")

#干掉前5个数据,以及最后一个数据,每隔一个取出数据
file_line = file_line[5:-2:2]
print(file_line)

#存储所有来拼接ts的链接地址
url_list = []
headers =  {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

#对可遍历数据，取出索引和对应的数据
for index, line in enumerate(file_line):
    pd_url = begin_url + file_line[index]  # 拼出ts片段的URL
    # print(pd_url)
    url_list.append(pd_url)
    # file_name = file_line[index+1][-10:-3] 

#计算url_list的长度,并且打印出来
url_length = len(url_list)
print(url_length)

for i in range(url_length):
    add_url= url_list[i]
    # 正则取出数字文件名字
    patt = re.compile(r'\d+')
    file_name = add_url.split("/")[-1]
    print('file_name:', file_name)

    #设置最大重试次数
    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))

    #请求页面数据
    try:
        response = s.get(add_url, headers=headers, verify=False, timeout=(3.05, 7))
        html = response.content
    except requests.exceptions.RequestException as e:
        print(e)
    
    # result_file_name= url_list[i][length:][-10:-3]
    result_file_name = patt.findall(file_name)[1][-4:]
    print('result_file_name:', result_file_name)
    print("正在处理%s"%result_file_name+".ts","共%s/%s项"%(i+1,url_length))
    time.sleep(1)
    path = "D:/video2/"
    if (not os.path.exists(path)):
        os.makedirs(path)
    with open(path+result_file_name+'.ts',"wb")as f:
        f.write(html)


path1 = 'D:/video2/'
#切换目录
os.chdir(path1)
#合并的命令
cmd = "copy /b * new.tmp"
os.system(cmd)
os.rename("new.tmp", "new.mp4")


print('合并完成')