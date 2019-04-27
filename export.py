import re
import time

import requests

class QQMusicList():
    def __init__(self, id):
        self.id = id
        self.headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Mobile Safari/537.36",
            "referer": f"https://y.qq.com/w/taoge.html?ADTAG=profile_h5&id={self.id}"

        }
        self.session = requests.Session()

    def total_song_num(self):
        url = f"https://y.qq.com/n/m/detail/taoge/index.html"
        params = {
            "ADTAG": "profile_h5",
            "id": self.id
        }
        method = "GET"
        resp = self.session.request(method, url, params=params, headers=self.headers, timeout=10)
        if resp.status_code != 200:
            print("get song num error.")
            return 0
        total_song_num = re.search(r"共(\d+)首", resp.text).group(1)
        if not isinstance(total_song_num, int):
            total_song_num = int(total_song_num)
        return total_song_num

    def get_list(self):
        song_list = []
        url = "https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg"
        params = {
            "_": int(time.time() * 1000)
        }
        method = "POST"
        postdata = {
            "format": "json",
            "inCharset": "utf-8",
            "outCharset": "utf-8",
            "notice": "0",
            "platform": "h5",
            "needNewCode": "1",
            "new_format": "1",
            "pic": "500",
            "disstid": self.id,
            "type": "1",
            "json": "1",
            "utf8": "1",
            "onlysong": "0",
            "nosign": "1",
            "song_begin": 0,
            "song_num": "15",
        }
        total_song_num = self.total_song_num()
        for song_begin in range(0, total_song_num, 15):
            postdata["song_begin"] = str(song_begin)
            params["_"] = int(time.time() * 1000)
            resp = self.session.request(method, url, headers=self.headers, params=params, data=postdata)
            if resp.status_code != 200:
                print(f"{song_begin} 页数获取失败.")
                continue
            data = resp.json()
            cdlist = data.get("cdlist")[0]
            songlist = cdlist.get("songlist")
            for song in songlist:
                name = song.get("name")
                singer = song.get("singer")[0].get("name")
                sony_name = f"{name} - {singer}"
                print(sony_name)
                song_list.append(sony_name)

        return song_list

    def start(self):
        datas = self.get_list()
        to_file_data = "\n".join(datas)
        file_name = f"{self.id} QQ音乐歌单.txt"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(to_file_data)
        print(f"文件成功保存到:{file_name},"
              f"歌曲数量:{len(datas)}")


if __name__ == '__main__':
    wang_qq_list = QQMusicList("3332861007")
    wang_qq_list.start()
