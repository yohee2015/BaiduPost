# -*- coding:utf-8 -*-
"""
@author:Levy
@file:createFilePath.py
@time:2018-07-02 13:25
"""
import os
import shutil
class BylwHandle():
    def __init__(self):
        pass
    def classifyFile(self,path,clsn):
        filepath=path+clsn
        try:
            list = os.listdir(filepath)
            print('正在处理班级' + clsn + '...')
            for i in range(len(list)):
                path = os.path.join(filepath, list[i])
                if os.path.isfile(path):
                    stuname = str(list[i]).split('-')[1]
                    isExists = os.path.exists(filepath + '/' + stuname)
                    if not isExists:
                        os.makedirs(filepath + '/' + stuname)
                        print(stuname + "文件夹创建成功")
                    shutil.move(filepath + '/' + list[i], filepath + '/' + stuname)
            shutil.make_archive(filepath, 'zip', filepath)
            print(clsn+'处理成功！')
        except:
            print(clsn, '该班级不存在！')
            return None
    #中文乱码
    def decompress(self,path):
        try:
            list = os.listdir(path)
            print(list)
            for i in range(len(list)):
                shutil.unpack_archive(path+list[i],path)
        except:
            return None

if __name__=='__main__':
    rootdir = r'F:/test/'
    clsname = ['CFA1402', '保险1401', '创新1403', '金工1401', '投资1401', '金融双专', '金融1401', '金融1402', '金融1403']
    bylw=BylwHandle()
    for clsn in clsname:
        bylw.classifyFile(rootdir,clsn)
