# -*- coding: utf-8 -*-
# @Time    : 4/12/2019 14:02
# @Author  : MARX·CBR
# @File    : __init__.py.py
import threading
import sys
from PyQt5 import QtWidgets
from updateServer.HotUpdate import myfunction
import redis
import random
import importlib
from updateServer.HotUpdate.HotFixSample import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.fun = importlib.import_module("myfunction")
        self.pushButton.clicked.connect(self.runFunction)
        self.pushButton_2.clicked.connect(self.hotfix)
        self.ip = "47.101.195.58"
        self.redisport = 2017
        self.redis_manager = redis.StrictRedis(self.ip, port=self.redisport)
        # self.textBrowser.append(str(sys.modules))
        print(sys.modules)
        self.tunnel = self.redis_manager.pubsub()
        self.tunnel.subscribe(["update"])
        self.threads = []
        self.t1 = threading.Thread(target=self.autoReload, )
        self.threads.append(self.t1)
        self.threads[0].setDaemon(True)
        self.threads[0].start()

    def autoReload(self):

        for k in self.tunnel.listen():
            if k.get('data') == b'reload':
                self.hotfix()

    def runFunction(self):
        version = self.fun.AllFunction().version
        self.textBrowser.append("功能运行，当前版本为：" + version)
        for i in range(4):
            x = random.randint(-454, 994)
            y = random.randint(-245, 437)
            self.textBrowser.append(str(x) + "\tfunction version {}\t".format(version) + str(y) + " = " + str(
                self.fun.AllFunction().second(x, y)))
        # self.textBrowser.append(self.fun.AllFunction().first())

    def hotfix(self):
        del sys.modules["myfunction"]
        self.fun = importlib.import_module('myfunction')
        self.textBrowser.append("热更新完毕")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
