# -*- coding: utf-8 -*-
# @Time    : 4/1/2019 19:36
# @Author  : MARX·CBR
# @File    : updateClient.py
import json
import hashlib
import sys
import pickle
from PyQt5 import QtWidgets
from urllib3 import request
from urllib import request
import os

from updateServer.UClient.sample import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.showUpdate)
        self.pushButton_2.clicked.connect(self.updateNow)
        self.updateList = []
        self.updateServer = UpdateFiles()

    def showUpdate(self):
        self.textBrowser.clear()
        self.updateList = self.updateServer.check_update()
        for j in self.updateList:
            print(j)
            self.textBrowser.append(j)

    def updateNow(self):
        all_file_number = 0
        for j in self.updateList:
            self.updateServer.downloadFiles(j)
            all_file_number += 1
            vau = int((all_file_number * 100) / len(self.updateList))
            self.progressBar.setValue(vau)
            self.repaint()


class UpdateFiles():
    def __init__(self):
        self.server = 'xx.xx.xx.xx'
        self.port = '1213'
        self.directory = os.getcwd()

    def downloadFiles(self, key):
        checkurl = 'http://' + self.server + ':' + self.port
        file_dir = self.directory + '\\' + key
        file_dir = file_dir.replace('/', '\\')
        if os.path.exists(file_dir):
            os.remove(file_dir)
            request.urlretrieve(checkurl + '/' + key, file_dir)
        else:
            newpath = '\\'.join(file_dir.split('\\')[:-1:])
            print(newpath)
            try:
                os.mkdir(newpath)
                request.urlretrieve(checkurl + '/' + key, file_dir)
            except:
                request.urlretrieve(checkurl + '/' + key, file_dir)

    def Getfile_md5(self, filename):
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

    def check_update(self):
        data = {}
        updateList = []
        checkurl = 'http://' + self.server + ':' + self.port
        request.urlretrieve(checkurl + '/.listFile', ".listFile")

        with open(".listFile", "rb") as f:
            data = pickle.load(f)
        print(data)
        for key in data:
            new_md5 = data[key]
            file_dir = self.directory + '\\' + key
            if os.path.exists(file_dir):
                oldmd5 = self.Getfile_md5(file_dir)
                if oldmd5 != new_md5:
                    print(new_md5, "准备下载")
                    updateList.append(key)
                # print(new_md5)
            else:
                updateList.append(key)
                print('准备下载', file_dir)
        return updateList


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
