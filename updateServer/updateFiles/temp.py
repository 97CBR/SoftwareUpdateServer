# -*- coding: utf-8 -*-
# @Time    : 4/1/2019 20:11
# @Author  : MARX·CBR
# @File    : temp.py
import hashlib
import os
import json
updateList={}
def Getfile_md5( filename):
    if not os.path.isfile(filename):
        return
    myHash = hashlib.md5()
    f = open(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myHash.update(b)
    f.close()
    return myHash.hexdigest()

def findFile(path):
    fsinfo = os.listdir(path)
    for fn in fsinfo:
        temp_path = os.path.join(path, fn)
        if not os.path.isdir(temp_path):
            print('文件路径: {}' .format(temp_path))
            fm=Getfile_md5(temp_path)
            print(fn)
            updateList[fn]=fm
        else:
            findFile(temp_path)

# def generate():
directory = os.getcwd()
findFile(directory)
file_md5_list=json.dumps(updateList)
print(file_md5_list)

d = {}

import pickle
with open("listFile", "rb") as f:
    d = pickle.load(f)
print(d)