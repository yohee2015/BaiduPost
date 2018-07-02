# -*- coding:utf-8 -*-
"""
@author:Levy
@file:baiduPost.py
@time:2018-06-2216:42
"""
import os
from urllib import parse

import requests
import random
import time

from PIL import Image
from lxml import etree
from requests.exceptions import ProxyError

from config import *


class SendBaiduMsg():
    def __init__(self):
        self.cookies = {
            'Cookie': 'TIEBA_USERTYPE=240918a96567254ebf3f8355; TIEBAUID=a320d01d8de7c7a6867d6f28; bdshare_firstime=1413631725940; IS_NEW_USER=902f5df63276f258243f4212; BIDUPSID=58C9AF2252A9A93794338CFD83E8AC5A; PSTM=1433404427; SEENKW=%E8%BF%AA%E4%B8%BD%E7%83%AD%E5%B7%B4; rpln_guide=1; FP_LASTTIME=1510625484114; BAIDUID=8DB1428C3092FCCB2792D6C61228EAD1:FG=1; BDUSS=VnNEpnR290NnVybER2VTBQOEFvbVF6UmhUSmZGd0JVNTNTbFV4QTZCNGV1Q0JiQVFBQUFBJCQAAAAAAAAAAAEAAAC1yiMMbG92ZXh1YW45OTk5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB4r-VoeK~laMF; STOKEN=8ed08d3421593def428f771f94ad46498a5770bd28c3a92fe13a9a5f7fb8425d; H_PS_PSSID=26525_1460_21116_26350_22160; wise_device=0; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1530352873,1530438873,1530439068,1530499055; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1530499266'
        }
        self.url2 = 'http://tieba.baidu.com/f/commit/post/add'#贴吧回复地址
        self.tb_url = 'http://tieba.baidu.com/f?fr=wwwt&' #贴吧列表地址
        self.uploadPicUrl = 'http://upload.tieba.baidu.com/upload/pic?tbs=9cb9836df73fbf60015297541300125500_1&fid=2679889' #图片上传地址
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            "Referer": "http://tieba.baidu.com/p/5777628252",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            'X-Requested-With':'XMLHttpRequest'
        }
        self.proxies=None
        '''
        图片目录 图片路径列表
        '''
        self.picPath=[]
        self.todayTarget=""
        self.key = parse.urlencode({'kw': TIEBA_NAME})#目标贴吧名
        self.createPicPath()#获取图片目录
    '''
        获取贴吧相册的所有图片
    '''
    def getPic(self,kw,tid):
        pic_url = "http://tieba.baidu.com/photo/g/bw/picture/list?kw={}&tid={}".format(kw,tid)
        pic_ret = requests.get(pic_url, headers=self.headers1)
        error = pic_ret.json()['error']
        if error == 'sucess!':
            for i in range(len(pic_ret.json()['data']['pic_list'])):
                pic_id = pic_ret.json()['data']['pic_list'][i]['pic_id']
                nurl = pic_ret.json()['data']['pic_list'][i]['murl']
                ext = nurl.split(".")[-1];
                purl='https://imgsa.baidu.com/forum/pic/item/'+pic_id+'.'+ext
                print('正在下载第'+str(i+1)+'张图片...')
                if os.path.exists('./rebapic/{}.{}'.format(pic_id, 'jpg')) == False:
                    with open('./rebapic/{}.{}'.format(pic_id, 'jpg'), 'ab') as f:
                        ret = requests.get(purl)
                        f.write(ret.content)
                else:
                    print('该图片已存在')
    '''
        获取百度贴吧首页帖子列表序号
    '''
    def getList(self):

        tb_ret = requests.get(self.tb_url+self.key, headers=self.headers)
        #获取的源代码里面 注释掉的内容
        result = str(tb_ret.content).replace('<!--', '')
        result = result.replace('-->', '')
        html = etree.HTML(result)
        #获取所有标题的链接地址
        html_content = html.xpath("//div[contains(@class,'j_th_tit')]/a/@href")
        html_title = html.xpath("//div[contains(@class,'j_th_tit')]/a/text")
        for html in html_content:
            html = str(html).split(r'/')#获取pid 帖子ID
            for i in range(HF_COUNT):
                time.sleep(random.randint(3, 9))
                if PIC_COUNT<1:
                    self.sendMsg(html[-1])
                else:
                    self.sendPic(html[-1])

    '''
    生产图片地址列表
    '''
    def createPicPath(self):
        print(PIC_PATH)
        for root, dirs,files in os.walk(PIC_PATH):
            for file in files:
                if os.path.splitext(file)[1] == '.jpg':
                    self.picPath.append(os.path.join(root, file))

    '''
       上传图片
    '''
    def sendPic(self,pid):

        payload={
            'Content - Disposition': 'form - data;name = "file";filename = "aa.jpg"',
            'Content - Type': 'image / jpeg'
        }
        headers = {
            'Accept-Encoding': 'gzip, deflate',
            # 'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryQknAWxKg78v72soV',
            'Host': 'upload.tieba.baidu.com',
            'Origin': 'http://tieba.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
        }
        pic_url=''
        height=100
        for p in range(PIC_COUNT):
            pic = random.sample(self.picPath, 1)
            picpath = str(pic[0])
            img = Image.open(picpath)
            pic_size = img.size
            height=int(560 / pic_size[0] * pic_size[1])
            with open(picpath, 'rb') as f:
                fr=f.read()

            files={
                'file':('aa.jpg',fr,'image/jpeg')
            }
            html = requests.post(url=self.uploadPicUrl, data=payload, cookies=self.cookies, headers=self.headers, files=files)
            err_no = html.json()['err_no']
            if err_no == 0:
                pic_id_encode = html.json()['info']['pic_id_encode']
                pic_url += '[img pic_type=0 width=560 height={}]http://imgsrc.baidu.com/forum/pic/item/'.format(height) + pic_id_encode + '.jpg[/img][br]'
                print('图片上传成功！')
            time.sleep(random.randint(60, 300))
        err_no=self.sendMsg(pid, pic_url)
        if err_no != 0:
            print("发帖失败！休息一下！")
            time.sleep(600)

    '''
       获取代理
     '''
    def getProxy(self):
        try:
            proxy = requests.get(PROXY_POOL_URL)
            if proxy:
                self.proxies={
                    'http':'http://'+proxy.text
                }
        except ConnectionError:
            return None

    '''
       回复百度信息
       pid 回复帖子的序号
       content 回复帖子的图片内容
     '''
    def sendMsg(self, pid,content=''):
        msg = random.choice(MESSAGE)+'[br]'+content
        self.data2 = {
            'ie': 'utf-8',
            'kw': TIEBA_NAME,
            'fid': '2679889',
            'tid': pid,
            'floor_num': '1741',
            'rich_text': '1',
            'tbs': '45df411cda368c981530499316',
            'content': msg,
            'basilisk': '1',
            'mouse_pwd': '51,62,50,43,54,48,55,48,48,14,54,43,55,43,54,43,55,43,54,43,55,43,54,43,55,43,54,43,55,14,54,63,55,50,55,14,54,49,55,55,43,62,55,55,15304992667070',
            'mouse_pwd_t': '1530499266707',
            'mouse_pwd_isclick': '0',
            '__type__': 'reply',
            '_BSK': 'JVwSUWcLBBpzRQNzQztCElBFNTgpUThSTT4GQSAZJDwkQnwJXCoxDllQMTgXSAYPO0kyUQ18SyIyGE0ULF9ARDJZQz4TKRhERgg1MjRABxtKIhcKKVAoNyVYfAxfJjcYER8xOAdMXgAmRnNQETNNKjsQFU8qQ01MLBsfMQAhExwCDjYjNVcMG1IiBEcxXCk+M1EiQ14sKggXUi97FEhYGiZGPlgcMUprLR0TDCldRko3BhFzQzhHElBFIyI0RgFeUSNHUipmMiI4XjdHGmk/XS5dPCMNW09JKkc7USNwRWVyXAJSZwsEXzcAVnNDIkQSUEcxJS9AWRVKf0UcZQRzY2EEaVYBcXBRV1JpdV4NTAglWzoYXDEJZWReUFV1AQgJIEQRZUF+RgFdV3BmawlXRw9vXQRgAgR1YwIkDUBsdk9QABxyVh8eXC1OawVPM1wmbUhZAHwJFR52RQdmWH9HBk9Vd3JtYVcbHD9WBH8XICU/UyQGXCdkDxRdOTgJBQNJMggEWh8kUTE7XgIMIVR5CzhXH30IfVQKShM3Ij8JV1MPb10EC2AKHHMccgMCa35fD1twFCoPBks+GX0OXB5tCxJcTUEpAwYRZQFBKgRgVF5bRX93aBVEAA54VhdpFzZicwpyOFond09XH38kVQ8QSXAYbxhcPgtlZF5TU3QGFB50RB99AH5UCkpfc2d2BxgGHHdFRCRGLzw4QzswUgUyTR9Uf3tGWhlLcwg5VRIjXWt8C1BBfxNpRD8cXzMAY0MeWkdtADNLEVhJPkdoERVwfmALcDhaJ3JJThMlYVAECig5WDNRKTVaDDcKTlZ2BgoYc1UbFCkYO3xGRyk+MUBVcFsuDElsFQU4I189Chx/dlNFHW5lVB8EUH0IDFUYMUoucUtSVGsCEglpV0BsQ3ZWRBgSIHt4UkcVBG8pcwl5ZHxzUWNNCWkiHBlAOHtGXRlLcwg5VRIjXTo='
        }

        print('代理服务器IP：',self.proxies)
        try:
            html = requests.post(self.url2, data=self.data2, cookies=self.cookies,proxies=self.proxies)
            if html.status_code==200:
                print(time.strftime('%Y-%m-%d %H:%M:%S'), pid, msg)
                err_no = html.json()['err_code']
                return err_no
            elif html.status_code==404:
                print('404 COOKIES已失效，请更换COOKIES')
                return html.status_code
            else:
                return None
        except ProxyError:
            self.getProxy()





if __name__ == '__main__':
    sendBaiduMsg = SendBaiduMsg()
    sendBaiduMsg.getProxy()#获取代理
    #sendBaiduMsg.getList()#遍历回复贴吧首页帖子
    for i in range(TODAY_TARGET_COUNT): #回复今日目标帖子
        time.sleep(random.randint(36, 100))
        err_no=sendBaiduMsg.sendMsg(TODAY_TARGET_PID)
        if err_no==404:
            os._exit()
        elif err_no != 0:
            print(time.strftime('%Y-%m-%d %H:%M:%S'),"发帖失败！休息10分钟再继续！")
            sendBaiduMsg.getProxy()
            time.sleep(100)
