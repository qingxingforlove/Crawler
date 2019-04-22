
#!/usr/bin/env python
# coding=utf-8
# 爬取m3u8地址的所有ts文件并下载到"D:/video2/"，一般会有几千个文件耐心等待
 
# 下载阿丽塔
# https://sohu.zuida-163sina.com/20190223/TnSFbZPj/800kb/hls/jQQWmUN39911775.ts 其中一个ts文件地址
# 第一步通过查看源代码可看到Referer地址如下，其中下载地址:https://sohu.zuida-163sina.com/20190223/TnSFbZPj/index.m3u8
# https://newplayers.pe62.com/mdparse/m3u8.php?id=https://sohu.zuida-163sina.com/20190223/TnSFbZPj/index.m3u8
# 第二步以上下载的文件中有个地址：/ppvod/FA7CC7B31F271DBD6F1A181E8429770D.m3u8
# 组合成地址："https://sohu.zuida-163sina.com/ppvod/FA7CC7B31F271DBD6F1A181E8429770D.m3u8"就可以下载了
import requests
import os,re
import time
import urllib.request
 
# https://sohu.zuida-163sina.com/20190223/TnSFbZPj/800kb/hls/jQQWmUN39911775.ts 通过这个可以确定url开头部分
# 将来需要拼接的每一个ts视频文件地址的开头
begin_url = "https://sohu.zuida-163sina.com"
length = len(begin_url)
# m3u8地址,下载下来会看到很多个ts文件名字组成
url = "https://sohu.zuida-163sina.com/ppvod/FA7CC7B31F271DBD6F1A181E8429770D.m3u8"
 
response = requests.get(url)
all_content = response.text
# 按照结尾的换行符进行切片操作
file_line = all_content.split("\n")
# 存储将来拼接的所有ts链接地址
url_list = []
header = {
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0);'
}
for index, line in enumerate(file_line):
    if "EXTINF" in line:
        pd_url = begin_url + file_line[index + 1]  # 拼出ts片段的URL
        # print(pd_url)
        url_list.append(pd_url)
        # file_name = file_line[index+1][-10:-3]
 
url_length = len(url_list)
for i in range(url_length):
    add_url= url_list[i]
    # 正则取出数字文件名字
    patt = re.compile(r'\d+')
    file_name = add_url.split("/")[-1]
    request = urllib.request.Request(add_url,headers=header)
    response = urllib.request.urlopen(request)
    html = response.read()
    # result_file_name= url_list[i][length:][-10:-3]
    result_file_name= patt.findall(file_name)[0]
    print("正在处理%s"%result_file_name+".ts","共%s/%s项"%(i+1,url_length))
    time.sleep(1)
    path = "D:/video2/"
    if (not os.path.exists(path)):
        os.makedirs(path)
    with open(path+result_file_name+'.ts',"wb")as f:
        f.write(html)
--------------------- 
作者：執筆冩回憶 
来源：CSDN 
原文：https://blog.csdn.net/z564359805/article/details/81055321 
版权声明：本文为博主原创文章，转载请附上博文链接！
# -*- coding:utf-8 -*-  
import sys  
import os  
from glob import glob  
#获取需要转换的路径  
def get_user_path(argv_dir):
    if os.path.isdir(argv_dir):  
        return argv_dir  
    elif os.path.isabs(argv_dir):
        return argv_dir
    # else:
    #     # return False
    #     print("您输入的路径不正确，:-(")
#对转换的TS文件进行排序         
def get_sorted_ts(user_path):
    # 对ts文件名字进行重命名，防止出现001.ts的名字，系统自动改成1.ts
    dirlist = os.listdir(user_path)
    for name in dirlist:
        if name[-3:]==".ts":
            newname = str(int(name[:-3]))+".ts"
            os.rename(user_path+"/"+name,user_path+"/"+newname)
    ts_list = glob(os.path.join(user_path,'*.ts'))  
    # print(ts_list)
    boxer = []
    for ts in ts_list:
        if os.path.exists(ts):
            # print(os.path.splitext(os.path.basename(ts)))
            # file就是文件的名字，_是文件的扩展名.ts
            file,_ = os.path.splitext(os.path.basename(ts))
            # boxer.append(file)
            # file要转换为int类型才能保证排序正确，但是要求转换文件名字是1.ts不能是001.ts
            boxer.append(int(file))  
    boxer.sort()  
    # print(boxer)  
    return boxer  
#文件合并     
def convert_m3u8(boxer,o_file_name):  
    #cmd_arg = str(ts0)+"+"+str(ts1)+" "+o_file_name  
    tmp = []  
    for ts in boxer:
        tmp.append(str(ts)+'.ts')
    cmd_str = '+'.join(tmp)  
    exec_str = "copy /b "+cmd_str+' '+o_file_name  
    # print("copy /b "+cmd_str+' '+o_file_name)  
    os.system(exec_str)
          
if __name__=='__main__':  
    # print(sys.argv[1:])  
    argv_len = len(sys.argv)
    if argv_len == 3:  
        o_dir,o_file_name =sys.argv[1:]  
        # print(o_dir+":"+o_file_name)
        user_path = get_user_path(o_dir)
        # print(user_path)
        if not user_path:
            print("您输入的路径不正确，:-(")
        else:
            if os.path.exists(os.path.join(user_path,o_file_name)):
                print('目标文件已存在，程序停止运行。')
                exit(0)
            try:
                os.chdir(user_path)
            except:
                print("请核实文件路径地址，程序停止运行！")
                exit(0)
            #convert_m3u8('2.ts','4.ts',o_file_name)
            boxer = get_sorted_ts(user_path)
            convert_m3u8(boxer,o_file_name)
            #print(os.getcwd())
    else:  
        print("参数个数非法")
--------------------- 
作者：執筆冩回憶 
来源：CSDN 
原文：https://blog.csdn.net/z564359805/article/details/81055825 
版权声明：本文为博主原创文章，转载请附上博文链接！