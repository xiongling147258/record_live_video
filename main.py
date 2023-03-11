import requests
import os
import time
import re
import sys
from record_video import *

from record_danmu import *
# from save_log import *

import asyncio
from threading import Thread, Lock



if __name__ == '__main__':
    print("输入的参数个数:" + str(len(sys.argv)))
    if len(sys.argv) == 4:
        room_id = sys.argv[1]
        room_name = sys.argv[2]
        record_path = sys.argv[3]
    else:
        room_id = 72821
        room_name = "test"
        record_path = "./"

    pathTmp = datetime.datetime.now()
    log_file_name = str(pathTmp.day) + "_" + str(pathTmp.hour).zfill(2) + "." + str(pathTmp.minute).zfill(2) + "." + str(pathTmp.second).zfill(2) + ".log"
        
    log_f = open("./log/" + room_name  + "_" + log_file_name, "w")
    sys.stdout = log_f
    sys.stderr = log_f

    
    record_video_thread = record_video(1, "record_video_thread", room_id, room_name, record_path)

    record_video_thread.start()

    while 1:
        log_f.flush()
        time.sleep(10)


    
