
import requests
import os
import time
import re
import sys
from convert_video import *


if __name__ == '__main__':

    print("输入的参数个数:" + str(len(sys.argv)))
    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        path = "./"

    print("patch:" + path)

    convert_video_thread = convert_video(2, "convert_video_flv_to_mp4", path)
    convert_video_thread.start()

    while True:
        time.sleep(10)
