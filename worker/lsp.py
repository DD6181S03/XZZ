from zzcore import StdAns, mysakuya
import requests

from config import LOLIKEY

class Ans(StdAns):
    AllowGroup = [ 805197917,343700338,125733077,1084566280,920863253,798595664,655057127,196268763, 204097403, 247022495, 474907856]
    def GETMSG(self):
        url = 'https://api.lolicon.app/setu/'
        params = {
            'apikey': LOLIKEY,
        }

        if len(self.parms) < 2:        
            try:
                resp = requests.get(url=url,params=params).json()
                quota = str(resp['quota'])
                seconds = resp['quota_min_ttl']
                m, s = divmod(seconds, 60)
                h, m = divmod(m, 60)
                quota_min_ttl = f'{h}时{m}分{s}秒'
                picurl = resp['data'][0]['url']
                msg =  f"[CQ:reply,id={self.raw_msg['message_id']}][CQ:image,file={picurl}]\n剩余次数 {quota}\n距离回复元气 {quota_min_ttl}"
            except Exception as e:
                print(e)
                msg = '什么东西坏掉了,大概是Pixiv吧...不可能是咱!'
            return msg

        else:
            keyword = self.parms[1]
            if mysakuya(self, keyword) == False:
                return "不许你们看咲夜的涩图！！"
            
            params['keyword'] = keyword
            try:
                resp = requests.get(url=url,params=params).json()
                picurl = resp['data'][0]['url']
                msg =  '[CQ:reply,id=' + str(self.raw_msg['message_id']) + ']' + '咱帮你🔍 ' + keyword + ' 找到了这个\n' + picurl

                if len(self.parms) > 2 and self.parms[2] == 'p' :
                    msg = '[CQ:image,file=' + picurl + ']'
                # .replace('https://i.pixiv.cat', 'https://pximg.sihuan.workers.dev')
                # msg =  picurl.replace('https://i.pixiv.cat', 'https://original.img.cheerfun.dev')
            except Exception as e:
                print(e)
                msg = '[CQ:reply,id=' + str(self.raw_msg['message_id']) + ']咱没查到 ' + keyword + ' 也有可能是Pixiv坏掉了'
            return msg
