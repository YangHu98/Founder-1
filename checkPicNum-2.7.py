# -*- coding: utf-8 -*-
"""
检查IM字段中的图片的url是否和TX中的图片的url数量相同
在服务器上运行
Created on Wed Aug 7 11:19:28 2019
@author: LiYuexiang
"""

import os
import re


# 获取当前目录下所有TXT格式的文件
def eachFile():
    files = []
    pathFiles = os.listdir('./Main/')

    for eachfile in pathFiles:
        # 把TXT格式的文件加入到列表里
        if eachfile[-4:] == '.txt':
            eachfile = 'Main/' + eachfile
            files.append(os.path.join(os.getcwd(), eachfile))

    return files


def chechNum(files):
    for file in files:
        with open(file, 'r') as read_file:
            MI = ''
            while 1:
                line = read_file.readline()

                if not line:
                    break

                if line[:3] == 'MI:':
                    MI = line[3:-1]

                if line[:3] == 'IM:' and len(line) > 5:

                    # 去掉前面的 "IM:" 和结尾的“\n”
                    line = line.strip()[3:]
                    urls_IM = re.split(r';', line)
                    num_IM = count_Num(urls_IM)

                    # 找到TX字段里的图片链接
                    while 1:
                        line = read_file.readline()

                        # 遇到 "TX:" 开始查找
                        if line[:3] == 'TX:':
                            line = line.strip()
                            # text中存放正文内容
                            text = line
                            while 1:
                                line = read_file.readline()

                                # 遇到 "IO:"退出查找
                                if line[:3] == 'IO:':
                                    break

                                line = line.strip()
                                text += line

                            # 从正文从提取链接, 'src'前有空格才行，不然会匹配到oldsrc等
                            exp = re.compile('\ssrc="https?://[\d\w\:\/\.\?=&_\-,%]*"')
                            url_src = exp.findall(text)
                            # 从src=XXX中提取链接
                            urls_TX = [re.findall(r'https?://[\d\w\:\/\.\?=&_\-,%]*', url)[0] for url in url_src]
                            num_TX = count_Num(urls_TX)

                            if num_IM != num_TX:
                                print("The picture number is not equal: ")
                                print(MI + ": IM-" + str(num_IM) + " TX-" + str(num_TX))

                                if num_IM-num_TX == 1:
                                    print("Maybe is the cover.")
                                else:
                                    print("IM urls: " + str(urls_IM))
                                    print("TX urls: " + str(urls_TX))

                                print("---------------------------------")

                            # 到下一个字段退出
                            # if line[:3] == 'IO:':
                            break


def count_Num(urls):
    return len(urls)


if __name__ == '__main__':
    files = eachFile()
    chechNum(files)
