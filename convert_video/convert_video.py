import threading
import time
import os
from unittest.mock import patch

class convert_video (threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, thread_name, file_directory):
        threading.Thread.__init__(self)
        self.file_directory = file_directory
        self.flv_file_name = ""
        self.mp4_file_name = ""
        self.m4a_file_name = ""

    def run(self):        
        while True:
            # self.convent_video_print(self.file_directory)
            if os.path.exists(self.file_directory):
                self.flv_file_name  = self.get_flv_path(self.file_directory)
                print(self.flv_file_name)
                if "" != self.flv_file_name :
                    self.mp4_file_name = self.flv_file_name.replace(".flv", ".mp4")
                    self.mp4_file_name = self.mp4_file_name.replace("_need_convert", "")
                    cmd = "ffmpeg -i " + self.flv_file_name + " -vcodec copy -acodec copy " + self.mp4_file_name + " 2>> log.txt"
                    print("cmd = ", cmd)
                    os.system(cmd)

                    self.m4a_file_name = self.mp4_file_name.replace(".mp4", ".m4a")

                    cmd = "ffmpeg -i " + self.mp4_file_name  + " -vn -codec copy " + self.m4a_file_name + " 2>> log.txt"
                    print("cmd = ", cmd)
                    os.system(cmd)

                    os.remove(self.flv_file_name)
                    #重命名弹幕文件
                    tmp_danmu_end_path = self.flv_file_name.replace(".flv", ".ass").replace("_need_convert", "")
                    tmp_danmu_start_path = self.flv_file_name.replace(".flv", ".ass")
                    
                    try:
                        os.rename(tmp_danmu_start_path, tmp_danmu_end_path)
                    except:
                        print("重命名弹幕文件失败！！！")
                        pass

                    print("tmp_danmu_end_path: "+ tmp_danmu_end_path)
            time.sleep(10)
    
    def get_flv_path(self,path):
        flv_path = ""
        files= os.listdir(path) # 得到文件夹下的所有文件名称
        # print(files)
        for file in files: # 遍历该文件夹
            if os.path.isdir(path+"/"+file): # 是子文件夹
                flv_path = self.get_flv_path(path+"/"+file)
                # print(flv_path)
                if "_need_convert" in flv_path and ".flv" in flv_path:
                    # flv_path = path + "/" + file
                    print(flv_path)
                    return flv_path
                
            else: # 是文件
                # print(path+"/"+file)
                if "_need_convert" in file and ".flv" in file:
                    flv_path = path + "/" + file
                    # print(path+"/"+file)
                    return flv_path

        return flv_path

    def convent_video_print(self,str):
        print("convent video print: ", str)