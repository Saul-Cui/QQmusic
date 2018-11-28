
import requests
import os,re,json,time

class Request():
    
    def __init__(self,max=5):
        self.max = max
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 (KHTML, like Gecko) Raspbian Chromium/65.0.3325.181 Chrome/65.0.3325.181 Safari/537.36'
        }

    def get(self, url, headers = None, timeout = 5):
        if not headers:
            headers = self.headers
        key = 0
        while True:
            try:
                html = requests.get(url,headers = headers,timeout = timeout)
                break
            except:
                key += 1
                if key > self.max:
                    print ('无法获取：%s'%url)
                    html = None
                    break
                else:
                    print ('再次尝试：%s'%url)
        return html

#数据处理加输出类 继承 maxking.Request
class Out(Request):
    
    def __init__(self,name):
        Request.__init__(self,5)
        
        self.datas = self.get_datas(name)
        
        

    
    def xiazai(self,down_url,geshi,Name1,geshou):
        
        start = time.time()
        size = 0
        resopnse = requests.get(down_url,stream = True)
        chunk_size = 1024
        content_size = int(resopnse.headers["content-length"])
        
        if resopnse.status_code == 200:
            print("[文件大小]：%0.2f MB,默认下载路径E:\\music"%(content_size / chunk_size / 1024))
            with open("E:/music/%s-%s.%s"%(Name1,geshou,geshi),"wb") as file:
                for i in resopnse.iter_content(chunk_size=chunk_size):
                    file.write(i)
                    size += len(i)
                    print("\r"+"[下载进度]:%s%.2f%%"%(">"*int(size*50/ content_size),float(size / content_size *100)),end = "")
            end = time.time()
            print("\n"+"《%s-%s》下载完成!用时%.2f秒。\n"%(Name1,geshou,end-start))
        else:
            print("下载失败，请尝试其他资源！")
    #获取key
    
    
    
        


    
    #输出 编号 ＋ name
    def look_datas(self):
        key = 0
        
        for i in self.datas:
            Name1 = i['name']
            geshou = i['singer'][0]['title']
            print (str(key)+':'+Name1+'-'+geshou)
            key += 1

    #获取数据
    def get_datas(self,name):
        search_api = "http://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.center&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=100&w=%s" \
            "&&jsonpCallback=searchCallbacksong2020&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"
        list_music = self.get(search_api%name)
        if list_music:
            list_music = list_music.json()
            datas = list_music['data']['song']['list']
        else:
            datas = None
        return datas          



#输入类
class Ing():
    def __init__(self):
        self.path = 'E:/music/'
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        
        self.key = self.get_key()
        self.url1 = 'http://streamoc.music.tc.qq.com/'
        self.url2 = '%s?vkey=%s&guid=1234567890&uin=1008611&fromtag=8'
        
    #获取key
    def get_key(self):
        url0 = 'http://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=0&loginUin=1008611&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&uin=1008611&songmid=003a1tne1nSz1Y&filename=C400003a1tne1nSz1Y.m4a&guid=1234567890'
        key = requests.get(url0).json()
        key = key['data']['items'][0]['vkey']
        return key
    

    #输入歌名
    def ing_name(self):
        while True:
            name = input('请输入想要下载的歌曲或歌手名字：').strip()
            if name:
                break
        return name

    #更具输出的 编号 ＋ name 获取输入编号
    def ing_key1(self,out):
        while True:
            out.look_datas()
            key = input('序号 : ').strip()
            try:
                key = int(key)
            except:
                os.system('clear')
                print('NG')
            else:
                if 0 <= key < len(out.datas):
                    break
        return key

    #输入文件类型编号
    def ing_key2(self,out,key):
        _id = out.datas[key]['file']['media_mid']
        Name1 = out.datas[key]['name']
        geshou = out.datas[key]['singer'][0]['title'] 
        while True:
            show_geshi = ["1:mp3"]
            size_ape = out.datas[key]['file']['size_ape']
            size_flac = out.datas[key]['file']['size_flac']
            mv_vid = out.datas[key]['mv']['vid']
            if size_ape != 0:
                show_geshi.append("2:ape")
            if size_flac != 0:
                show_geshi.append("3:flac")
            if mv_vid != "":
                show_geshi.append("4:mv")
            print(show_geshi)
            bak = input('请选择下载音质的编号：').strip()
            if bak == '1':
                geshi = 'mp3'
                down_url = self.url1+"M800"+_id+self.url2%(".mp3",self.key)
                out.xiazai(down_url,geshi,Name1,geshou)
                break
            elif bak == '2':
                if size_ape != 0:
                    geshi = 'ape' 
                    down_url = self.url1+"A000"+_id+self.url2%(".ape",self.key)
                    out.xiazai(down_url,geshi,Name1,geshou)
                else:
                    print("输入有误,请返回重试！")
                break
            elif bak == '3':
                if size_flac != 0:
                    geshi = 'flac' 
                    down_url = self.url1+"F000"+_id+self.url2%(".flac",self.key)
                    out.xiazai(down_url,geshi,Name1,geshou)
                else:
                    print("输入有误,请返回重试！")
                break
            elif bak == '4':
                
                if mv_vid:
                    geshi = 'mp4'
                    getmv_url = "https://u.y.qq.com/cgi-bin/musicu.fcg?data=%7B%22getMvUrl%22:%7B%22module%22:%22gosrf.Stream.MvUrlProxy%22,%22method%22:%22GetMvUrls%22,%22param%22:%7B%22vids%22:" \
                                "%5B%22{}%22%5D,%22request_typet%22:10001%7D%7D%7D&g_tk=5381".format(mv_vid)
                    html = requests.get(getmv_url).json()
                    down_url = html["getMvUrl"]["data"][mv_vid]["mp4"][3]["freeflow_url"][0]
                    out.xiazai(down_url,geshi,Name1,geshou)
                else:
                    print("该资源没有mv格式，请尝试其他资源")
                break
            else:
                print("输入有误,请返回重试！")
                break
        return bak


def main():
    ing = Ing()
    while True:
        name = ing.ing_name()
        out = Out(name)
        key = ing.ing_key1(out)
        ing.ing_key2(out,key)

if __name__ == '__main__':
    __version__ = '2.0'
    NAME = 'QQ音乐资源下载'
    msg = """
            +------------------------------------------------------------+
            |                                                            |
            |              欢迎使用{} V_{}                  |
            |              特别感谢@Max King, 大力支持！                 |
            |                                                            |
            |                     Copyright (c) 2018 Max King，lyjxhxn   |
            +------------------------------------------------------------+
            """.format(NAME, __version__)
    print(msg)  
    main()
    
