# -*- coding: utf-8 -*-
# @Time    : 4/1/2019 19:27
# @Author  : MARX·CBR
# @File    : __init__.py.py
import pickle

import flask
from flask import request, jsonify, send_from_directory, abort, Flask, make_response
import os
import hashlib
import json

app = Flask(__name__)
allfile = []
md5_list = []
updateList = {}
directory = os.getcwd()


# 下载文件服务
@app.route("/<path:filename>", methods=['GET'])
def download(filename):
    if request.method == "GET":
        # FD=directory+'/updateFiles/'+filename
        # print(FD)
        # response = make_response(flask.send_file(FD))
        # response.headers["Content-Disposition"] = "attachment; filename={};".format(filename)
        # return response

        # filename=filename.replace('\\','/')
        if os.path.isfile(os.path.join('updateFiles', filename)):
            return send_from_directory(directory+'/updateFiles/', filename, mimetype='application/octet-stream',as_attachment=True)
        abort(404)


# 计算文件MD5
def Getfile_md5(filename):
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


# 计算生成新的清单文件
@app.route("/generateNewConfig", methods=['GET'])
def generate():
    findFile(directory + '/updateFiles/')
    file_md5_list = json.dumps(updateList)
    print(file_md5_list)
    with open('./updateFiles/.listFile', 'wb') as f:
        pickle.dump(updateList, f)
    return_data = {
        'Statu': 'success',
    }
    return jsonify(return_data)
    # file_md5_list=json.load(updateList)

# 找到更新文件目录里面的文件以及文件夹、递归寻找
def findFile(path):
    fsinfo = os.listdir(path)
    for fn in fsinfo:
        temp_path = os.path.join(path, fn)
        if not os.path.isdir(temp_path):
            print('文件路径: {}'.format(temp_path))
            fm = Getfile_md5(temp_path)
            print(fn)
            fn = temp_path.replace(directory + "/updateFiles/", '')
            updateList[fn] = fm
        else:
            findFile(temp_path)

# 检查更新版本，该部分尚未够，完善。可以考虑为管理员远程上传文件的时候
# 将更新说明以json格式一同上传到服务器中，更新时直接读取即可
@app.route("/checkUpdate", methods=['GET'])
def check():
    if request.method == "GET":
        return_data = {
            'Version': '0.0.1',
            'Msg': '更新文件，修复初始化卡顿bug\n增加文件预下载功能',
        }
        return jsonify(return_data)

# 首页Hello
@app.route("/", methods=['GET'])
def hello():
    if request.method == "GET":
        return "Hello MARXCBR"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1213)  # 运行，指定监听地址为 127.0.0.1:8080
