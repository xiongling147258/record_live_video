import asyncio
import danmaku
import sys
import time
import threading
import datetime
import os
import random
import shutil


class save_danmu (threading.Thread):   #继承父类threading.Thread

    def __init__(self, rid, room_name, file_directory, save_danmu_flag):
        threading.Thread.__init__(self)
        self.file_directory = file_directory
        self.room_name = room_name
        self.rid = rid
        self.room_addr = "https://www.huya.com/" + str(self.rid)
        self.save_danmu_flag = save_danmu_flag
        self.start_path = {}
        self.end_path = {}
        self.danmu_file = 0
        self.loop1 = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop1)
        self.loop = asyncio.get_event_loop()

    def run(self):   
        self.loop.run_until_complete(self.save_danmu(self.room_addr))

    def danmu_start_stop_api(self, save_danmu_flag, path):
        self.save_danmu_flag = save_danmu_flag
        
        if 0 == self.save_danmu_flag:
            self.start_path = path
            shutil.copyfile("header.ass", self.start_path)
            self.danmu_file = open(self.start_path, "a", encoding='utf-8')
        else:
            self.end_path = path
            print("self.end_path:" + self.end_path)

    async def printer(self,q,dmc):
        danmu_time = datetime.datetime.now()
        total_time = datetime.datetime(1970,1,1,0,0,3,0)
        
        while True:
            m = await q.get()
            if m['msg_type'] == 'danmaku':
                danmu_time_new = datetime.datetime.now()
                timeTmp = danmu_time_new - danmu_time
                danmu_time = danmu_time_new
                total_time = total_time + timeTmp
                total_time_10 = total_time + datetime.timedelta(seconds=10)
                random_num = random.randint(9,288)
                string = f'{m["content"]}'
                #组装弹幕
                string_danmu = "Dialogue: 0," + total_time.strftime("%H:%M:%S.") + total_time.strftime("%f")[0:2] + "," + \
                    total_time_10.strftime("%H:%M:%S.")  + total_time_10.strftime("%f")[0:2] + \
                    ",*Default,,0000,0000,0000,Banner;20;0;0,{\\move( 32, " + str(random_num) + ", 32, " + str(random_num) + \
                    ")}{\\fs10}" + string
                # print(string_danmu)
                if 0 == self.save_danmu_flag:
                    self.danmu_file.write(string_danmu + "\n")
            elif m['msg_type'] == 'exit' and  m['name'] == 'end':
                self.danmu_file.close()
                print("[%s @ %s]" % (__file__, sys._getframe().f_lineno))
                print("self.start_path=",self.start_path)
                print("self.end_path=",self.end_path)
                os.rename(self.start_path, self.end_path)
                # await dmc.stop()
                print("退出弹幕录制线程")
                sys.exit()
                # break

    async def put_data(self,q):
        msg = {'name': '', 'content': '', 'msg_type': ''}
        while True:
            if 1 == self.save_danmu_flag:
                msg['name'] = 'end'
                msg['msg_type'] = 'exit'
                await q.put(msg)
                break
            await asyncio.sleep(1)
            
    async def save_danmu(self, url):
        q = asyncio.Queue()
        dmc = danmaku.DanmakuClient(url, q)
        asyncio.create_task(self.printer(q,dmc))
        asyncio.create_task(self.put_data(q))
        try:
            await dmc.start()
        except:
            print("await dmc.start() error!!!")
            self.danmu_file.close()