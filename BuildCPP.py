#! /usr/bin/env python
#coding=utf-8

from jinja2 import Template
import os

#c++代码模板文件路径
cppTemplatefile = './template.txt'
#表格文件路径
tablefilePath = './table'
#生成代码的文件路径
generalCppPath = './general'


def GetTable():
    # 读取txt文件夹中的所有txt文件
    table_files = [f for f in os.listdir(tablefilePath) if os.path.isfile(os.path.join(tablefilePath, f)) and f.endswith('.txt')]
    
    for ts in table_files:
        with open(os.path.join(tablefilePath, ts), 'r') as f:
            
            filename = os.path.basename(ts)
            tablename,suffix = os.path.splitext(filename)
            #生成的文件名
            tablename += '.h'
            #print(ts)

            buildCpp(tablename,ts)

def buildCpp(filename,filepath):
    generalfilePath = generalCppPath+'/'+filename
    class_file = open(generalfilePath, 'w')
    tablename,suffix = os.path.splitext(filename)

    type = []
    name = []

    with open(tablefilePath+'/'+filepath, "r") as file:
        for i, line in enumerate(file):
            if i == 0:   # 只处理前2行数据
                for value in line.strip().split():
                    name.extend(value.split("\t"))
            elif i==1:
                for value in line.strip().split():
                    type.extend(value.split("\t"))
            else:
                break 
    member = dict(zip(name,type)) 
    print(member)

    # 加载模板文件
    template_file = open(cppTemplatefile, 'r')
    tmpl = Template(template_file.read())

    # 模板替换
    mycode = tmpl.render(CLASSNAME = tablename.upper(),Class_Name = tablename,member=member)
    
    # 将代码写入文件
    class_file.writelines(mycode)
    class_file.close()

    print('ok')    

if __name__ == '__main__':
    GetTable()
