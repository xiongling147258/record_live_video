import requests

def get_live_url(room_id, header):
    video_url = ""
    room_url = 'https://mp.huya.com/cache.php?m=Live&do=profileRoom&roomid=' + str(room_id)
    
    try:
        data = requests.get(url=room_url, headers=header).json()
    except:
        print("get_live_url:get data error!!!")
        pass

    try:
        if 'stream' in data['data']:
            multiLine=data['data']['stream']['flv']['multiLine']
            obj=multiLine[0]
            al_flv = obj['url']
            video_url = al_flv + "&ratio=4000"
        else:
            print(str(room_id) + ":" + "不在线")
    except:
        print("get anchor status error!!!!")
        print("error room id:" + str(room_id))
        pass

    return video_url