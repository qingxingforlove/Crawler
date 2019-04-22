import requests
import json
import re
import os
'''
有需要Python学习资料的小伙伴吗?小编整理一套Python资料和PDF，感兴趣者可以加学习群：548377875，反正闲着也是闲着呢，不如学点东西啦~~
'''
 
def get_song(x):
    url = "http://songsearch.kugou.com/song_search_v2?callback=jQuery112407470964083509348_1534929985284&keyword={}&" \
          "page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filte" \
          "r=0&_=1534929985286".format(x)           #格式化输出一个动态搜索结果页
    res = requests.get(url).text                    #不是标准的json格式，部分是数组类型             
    js = json.loads(res[res.index('(') + 1:-2])     #切片：从res的(索引加一，一直到-2
    data = js['data']['lists']                      #取data下list数据
    for i in range(10):                             
        print(str(i + 1) + ">>>" + str(data[i]['FileName']).replace('<em>', '').replace('</em>', '')) #循环十次，打印出歌曲名称
    number = int(input("\n请输入要下载的歌曲序号（输入-1退出程序）: "))                                   #输入要下载的歌曲序号
    if number == -1:
        exit()
    else:
        name = str(data[number - 1]['FileName']).replace('<em>', '').replace('</em>', '')   #歌曲对应索引i = number -1
        fhash = re.findall('"FileHash":"(.*?)"', res)[number - 1]                           #匹配歌曲对应的filehash
        hash_url = "http://www.kugou.com/yy/index.php?r=play/getdata&hash=" + fhash         #对应歌曲的链接
        hash_content = requests.get(hash_url)                                               #链接的页面数据
        play_url = ''.join(re.findall('"play_url":"(.*?)"', hash_content.text))             #正则匹配播放链接
        real_download_url = play_url.replace("\\", "")                                      #取出下载链接

        with open(r'D:/CloudMusic/%s.mp3' % name, "wb")as fp:
            fp.write(requests.get(real_download_url).content)
        print("歌曲已下载完成！")                                                            #打开新文件，保存下载链接的内容
 
 
if __name__ == '__main__':
    x = input("请输入歌名：")                                                               #输入歌曲名称
    get_song(x)                                                                            #执行函数
    