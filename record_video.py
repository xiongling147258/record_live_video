
import threading
import time
import requests
import datetime
import os
from get_live_url import *
import asyncio
from record_danmu import *

header = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/75.0.3770.100 Mobile Safari/537.36 '
    }


class record_video (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, thread_name, room_id, room_name, file_directory):
        threading.Thread.__init__(self)
        self.room_id = room_id
        self.room_name = room_name
        self.root_file_directory = file_directory + self.room_name + "/"
        self.file_suffix = ".flv"
        print("room_id: " + str(room_id))
        print("room_name: " + str(room_name))
        print("file_directory: " + file_directory)
        
        self.file_directory = ""
        self.start_time = ""
        self.start_file_name = ""
        self.startPath = ""
        self.downloaded = 0
        self.fileSize = 1024*1024*1000

        self.end_time = ""
        self.end_file_name = ""
        self.endPath = ""

        self.save_danmu_flag = 0

    def run(self):  
        while True: 
            self.record_video()

    def record_video(self):

        room_id = self.room_id
        video_live = get_live_url(room_id, header)

        if "" == video_live:
            print("主播不在线")
            time.sleep(120)
        else:
            file = self.new_record_file()
            try:
                response = requests.get(video_live, stream=True, headers=header, timeout=120)
            except:
                print("response  get error")
                pass

            try:
                for data in response.iter_content(chunk_size=1024*1024*10):
                    if data:
                        if self.downloaded >= self.fileSize:
                            self.downloaded = 0
                            file.write(data)
                            self.close_record_file(file)
                            break
                        else:
                            self.downloaded += len(data)
                            file.write(data)
                    else:
                        break
            except:
                print("data response  get error")
            
            #主播直播结束或者获取数据异常
            if 0 < self.downloaded:
                self.downloaded = 0
                # file.write(data)
                self.close_record_file(file)
                print("直播结束")
            else:
                print("0 > self.downloaded 直播结束")

    def get_start_path(self):
        pathTmp = datetime.datetime.now()
        self.start_time = str(pathTmp.day) + "_" + str(pathTmp.hour).zfill(2) + "." + str(pathTmp.minute).zfill(2) + "." + str(pathTmp.second).zfill(2)
        self.start_file_name = self.start_time + self.file_suffix
        self.startPath = self.file_directory + self.start_file_name
        print(self.room_name + ":" + self.startPath)

    def get_end_path(self):
        pathTmp = datetime.datetime.now()
        self.end_time = str(pathTmp.hour).zfill(2) + "." + str(pathTmp.minute).zfill(2) + "." + str(pathTmp.second).zfill(2)
        self.end_file_name = self.start_time  + "-" + self.end_time + "_need_convert" + self.file_suffix
        self.endPath = self.file_directory + self.end_file_name
        print(self.room_name + ":" + self.endPath)

        self.save_danmu_flag = 1
        self.danmu_end_path = self.endPath.replace(".flv", ".ass")
        print("self.danmu_end_path: " + self.danmu_end_path)
        self.save_danmu_thread.danmu_start_stop_api(self.save_danmu_flag, self.danmu_end_path)


    def new_record_file(self):
        #如果目录不存在，则创建一个
        #获取年月日
        tmpTime = datetime.datetime.now()
        YMD = str(tmpTime.year) + "_" +  str(tmpTime.month).zfill(2) + "_" + str(tmpTime.day).zfill(2) + "/"
        self.file_directory = self.root_file_directory + YMD
        if 0 == os.path.isdir(self.file_directory):
            os.makedirs(self.file_directory) 
        
        self.get_start_path()
        print("self.startPath: " + self.file_directory)
        file = open(self.startPath,"wb")

        #开始录制弹幕
        self.danmu_start_path = self.startPath.replace(".flv", ".ass")
        self.save_danmu_flag = 0
        #创建一个线程
        self.save_danmu_thread = save_danmu (self.room_id, self.room_name, self.file_directory, self.save_danmu_flag)
        self.save_danmu_thread.danmu_start_stop_api(self.save_danmu_flag, self.danmu_start_path)
        self.save_danmu_thread.start()

        return file

    def close_record_file(self,file):
        file.close()
        self.get_end_path()
        os.rename(self.startPath, self.endPath)
        print("重命名----------->")
        print("开始文件名：" + self.startPath)
        print("结束文件名：" + self.endPath)
    