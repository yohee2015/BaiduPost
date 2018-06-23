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
from config import *


class SendBaiduMsg():
    def __init__(self):
        self.cookies = {
            'Cookie': 'BIDUPSID=0F70BC193583F0EBE9498A6AA734A30B; PSTM=1527341051; BDUSS=VJEaVd1eDVXdlNKT0Ywc3lEWkhBcXdDcno5VDV-eTJQV2VOUDRLZ2lQejE4REJiQVFBQUFBJCQAAAAAAAAAAAEAAAC1yiMMbG92ZXh1YW45OTk5AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPVjCVv1YwlbZ; STOKEN=06b5316c8108e6800496e85d066b49ec5486f0167b2cedee8ec296b62cfe24e3; TIEBA_USERTYPE=57f1b4eb083a0c6cd094a225; TIEBAUID=a320d01d8de7c7a6867d6f28; bdshare_firstime=1527347260437; BAIDUID=ACF14B89176BEA18B34CC7C4F7D4B397:FG=1; H_PS_PSSID=1441_21120_18559_22074; PSINO=2; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; cflag=15%3A3; Hm_lvt_98b9d8c2fd6608d564bf2ac2ae642948=1529487237,1529583430,1529732786,1529738794; 203672245_FRSVideoUploadTip=1; wise_device=0; LONGID=203672245; Hm_lpvt_98b9d8c2fd6608d564bf2ac2ae642948=1529738900'}
        self.url2 = 'http://tieba.baidu.com/f/commit/post/add'#贴吧回复地址
        self.tb_url = 'http://tieba.baidu.com/f?fr=wwwt&' #贴吧列表地址
        self.uploadPicUrl = 'http://upload.tieba.baidu.com/upload/pic?tbs=9cb9836df73fbf60015297541300125500_1&fid=2679889' #图片上传地址
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
            "Referer": "https://www.baidu.com/link?url=YGMen8KEGYwu1ZmGnlzH4CAMr8JvHM_bj-GLBWVdiWDIDZrki-J5zGgY3SUprhbDFwGwjK3bzhfx_n0E_OSUja&wd=&eqid=fb3a1b5b0002f91e000000025b2cc255",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
        }
        '''
            留言文字内容列表
        '''
        self.message = [
            r"#迪丽热巴# #迪丽热巴一千零一夜# #迪丽热巴凌凌七# 当世界从华丽到荒芜，请放心我还是你的粉丝@Dear-迪丽热巴 ",
            r"#迪丽热巴# #迪丽热巴一千零一夜# #迪丽热巴凌凌七# 就算荧光棒成了拐杖，你也依旧是我的信仰@Dear-迪丽热巴 ",
            r"#迪丽热巴# #迪丽热巴一千零一夜# #迪丽热巴凌凌七# 你在哪，心在哪。没想过如影随形，但想过永生不弃@Dear-迪丽热巴 ",
            r"#迪丽热巴# #迪丽热巴一千零一夜# #迪丽热巴凌凌七# 心疼你的心疼，感受你的感受，你的微笑是我快乐的通行号@Dear-迪丽热巴 ",
            r"#迪丽热巴# #迪丽热巴一千零一夜# #迪丽热巴凌凌七# 陪伴是最长情的告白，思念是最真心的等待@Dear-迪丽热巴 ",
            r"#迪丽热巴# #迪丽热巴一千零一夜# #迪丽热巴凌凌七# 明天太阳依旧升起，转角我们能否相遇?@Dear-迪丽热巴 ",
            r"#迪丽热巴# #迪丽热巴一千零一夜# #迪丽热巴凌凌七# 我承认我很花心，你的每个样子我都很喜欢@Dear-迪丽热巴 ",
            r"#迪丽热巴# #迪丽热巴一千零一夜# #迪丽热巴凌凌七# 你一定不知道自己的微笑，可以拯救我的全世界@Dear-迪丽热巴 ",
            r'#迪丽热巴# #迪丽热巴一千零一夜# #迪丽热巴凌凌七# 我喜欢春天的花夏天的树秋天的风冬天的雪和每天的你',
            r'#迪丽热巴# #迪丽热巴一千零一夜# #迪丽热巴凌凌七# 世界有万千种脸孔，偏偏却对你的笑容情有独钟。',
            r'#迪丽热巴# #迪丽热巴一千零一夜# #迪丽热巴凌凌七# 比起天黑和鬼,我更怕你心酸皱眉',
            r'#迪丽热巴# #迪丽热巴一千零一夜# #迪丽热巴凌凌七# 路有多长我就陪你走多远毫无怨忿绝不皱一下眉头',
            r'#迪丽热巴# #迪丽热巴一千零一夜# #迪丽热巴凌凌七# 我想你的存在就是为了证明我并不是三分钟热度',
            r'#迪丽热巴# #迪丽热巴一千零一夜# #迪丽热巴凌凌七# 我想把世界上最好的都给你,世界上最好的就是你',
            r'我喜欢一种朴实🌺叫李慧珍。[br]我喜欢一种痴情🌸叫白凤九。[br]我喜欢一种任性🌷叫高雯。[br]我喜欢一种强悍💐叫关小迪。[br]我喜欢一种勇敢🌹叫公孙丽🌷。[br]我喜欢一种绝世美，叫倾城。[br]我喜欢一种活泼🌺叫楼兰公主🌹；[br]喜欢一种真实😊叫迪丽热巴·迪力木拉提！！[br]热巴，我爱你！[br]6.25 一千零一夜'
            r"#迪丽热巴# #迪丽热巴一千零一夜# #迪丽热巴凌凌七# 爱上你们不是因为你们多好，只是因为某一天某一瞬间某一眼，命中注定我会爱上你@Dear-迪丽热巴",
            r'吾心向迪，永不分离。[br]❥#迪丽热巴#&nbsp;[br]❥#迪丽热巴烈火如歌#&nbsp;[br]❥#迪丽热巴一千零一夜#&nbsp;[br]❥#迪丽热巴三生三世枕上书#&nbsp;[br]❥#迪丽热巴凌凌七#&nbsp;[br]❥#迪丽热巴白凤九#&nbsp;[br]❥#迪丽热巴刘佳音#&nbsp;[br]❥#迪丽热巴的贴吧粉绝不认输#&nbsp;[br]2018继续陪伴！@Dear-迪丽热巴'
        ]
        '''
        图片目录 图片路径列表
        '''
        self.picPath=[]
        self.todayTarget=""
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
                if os.path.exists('./rebapic/{}.{}'.format(pic_id, 'gif')) == False:
                    with open('./rebapic/{}.{}'.format(pic_id, 'gif'), 'ab') as f:
                        ret = requests.get(purl)
                        f.write(ret.content)
                else:
                    print('该图片已存在')
    '''
        获取百度贴吧首页帖子列表序号
    '''
    def getList(self,kw):

        tb_ret = requests.get(self.tb_url+kw, headers=self.headers)
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
            time.sleep(random.randint(2, 6))

        self.sendMsg(pid, pic_url)

    '''
       回复百度信息
       pid 回复帖子的序号
       content 回复帖子的图片内容
     '''
    def sendMsg(self, pid,content=''):
        maxm = len(self.message) - 1
        msg = self.message[random.randint(0, maxm)]+'[br]'+content
        #msg=content
        self.data2 = {
            'ie': 'utf-8',
            'kw': '迪丽热巴',
            'fid': '2679889',
            'tid': pid,
            'floor_num': '1741',
            'rich_text': '1',
            'tbs': '869dc267115692f21529738896',
            'content': msg,
            'basilisk': '1',
            'mouse_pwd': '29,29,28,4,25,29,27,25,28,33,25,4,24,4,25,4,24,4,25,4,24,4,25,4,24,4,25,4,24,33,26,16,27,30,31,33,25,30,24,24,4,17,24,24,15296568600400',
            'mouse_pwd_t': '1529738901604',
            'mouse_pwd_isclick': '0',
            '__type__': 'reply',
            '_BSK': 'JVwAV2cLBE0kGUA6TW4TAUhdZWVqFEIHC3xWCmdCdXJrEDYOXzohUVdebHVeD0gIOkEzXQ07ZyYSCFEJIhMICTVGEWVBKhdcGQJpdTsWVw0eKwZKNlBqciUCclUTeHFPTAVoYVwVEkVrRmwWRHAKd29JUVZ0AAgJJEQRZUF9QABaS2c0awdPF0o/EkNpFydicwpwVwV5aF8GAH9tRFlYHCwEfUNMcgJlECstL2cdBll0Vwl9BzkYUx4OKjl6VxRZWiIKDmwVPXAKXjEbWj8hXRZcOTI5DVdLZQosBVxqGH5uTk1BIQAGEWc7ZhMtbloSBlVnbXpRB0JbYUVKdBd8citYfSx9a2hfHAJ/bURZWBwsBH1DT3ICZRArLS9nHQZbd1cJfTYlGANYRWl1LRFXDRw9CFUxeCMjIlE3Ch8rKAgHHzs4B1hZRSpEMEcbfF41PxMEEGlCQUcjWUQ2DygZR0YXJCU/SwEbUT0CSCBHaiQ+QHwDVicjCR0fPjsLXk8NZUQwVx8kUSgwUgUMJkRJTisBHzATJRFZBEsrNjdAWV9XPhNJN0xqPD5TMRtaJiofFEFxOgFDXwsoWnNEGyJLKDAfDQEkQwhYJgdcMw0uF0IZRWl1NBRXDR5/VxdyBXNhYBxyAQFrfl0BQSgySA9eWGsSfVILPlszNxEPQzFed183HF04SWVWS0o8KzYuTANSHi4IQiBoZi1zHHIaAmt+XzhcJz4IQUtGfAZvFFYHUSk6ERYQZX9wC3NbAmRBGx9eXFN+dyITQR4eDBdWKVARNTN7ORscfHdKWwBrd0xmYj0EZHMUEjlTIn45BAAuXg0LBh1BMAwpWQZYSXV5aRdFBRB0UwYWVCAxI1l/WgB+ak5DEXF1FBwIU2sNaHZbYgozPA1EUXcUF2pgRwE8USoSAl5TIW5iHRMEDHtTF3AHf2ZkBmlfAmx2T1AEGXVID1lbaxJ/BUhgCDo='
        }
        html = requests.post(self.url2, data=self.data2, cookies=self.cookies)
        print(html.status_code, pid, msg)


if __name__ == '__main__':
    sendBaiduMsg = SendBaiduMsg()
    kw = {'kw': '迪丽热巴'}
    key=parse.urlencode(kw)
    #sendBaiduMsg.getPic('%E8%BF%AA%E4%B8%BD%E7%83%AD%E5%B7%B4','4646103205')
    sendBaiduMsg.createPicPath()
    sendBaiduMsg.getList(key)
    #sendBaiduMsg.sendPic('5760383358')