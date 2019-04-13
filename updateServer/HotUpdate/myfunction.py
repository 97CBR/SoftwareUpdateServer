# -*- coding: utf-8 -*-
# @Time    : 4/12/2019 14:08
# @Author  : MARX·CBR
# @File    : myfunction.py

class AllFunction:
    def __init__(self):
        print("热更新成功")
        self.version="0.2.1"
        # self.first()

    def first(self):
        print("加载 第一个 功能成功")
        return "加载 第一个 功能成功,修改部分内容"

    def second(self,x,y):
        print("加载 第二个 功能成功")
        return x*y
    def third(self):
        print("加载 第三个 功能成功")
