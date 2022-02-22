import random,os,hashlib
from aip import AipSpeech
from config import BAIDUS
class BaiduSpeech():
    def __init__(self, lan='zh', per=0, vol=5, spd=7):
        self.aip = {}
        self.lan = lan
        self.per = per                # per 发音人选择 0：女生；1：男生；3：度逍遥；4：度丫丫
        self.vol = vol
        self.spd = spd
        self.voices = None
        i = random.randint(0, len(BAIDUS) - 1)
        self.key_index = 'n%s' % i
        if not self.key_index in self.aip:
            obj = BAIDUS[i]
            self.aip[self.key_index] = AipSpeech(obj['APP_ID'], obj['API_KEY'], obj['SECRET_KEY'])

    def __read_file_content__(file_path):
        with open(file_path, 'rb') as fp:
            return fp.read()

    def __write_file_content__(file_path, data):
        with open(file_path, 'wb') as fp:
            fp.write(data)

    def asr(self, voices):
        if os.path.exists(voices):
            result = self.aip[self.key_index].asr(self.__read_file_content__(voices), 'wav', 16000, {'lan': self.lan})
            if 'result' in result.keys():
                return result['result'][0]
        return ''

    def tts(self, context,file_path):
        file_path = file_path+'tts_'+str(hashlib.md5(context.encode()).hexdigest())+'.wav'
        if not os.path.exists(file_path): 
            result = self.aip[self.key_index].synthesis(context, self.lan, 1, {'vol': self.vol, 'per': self.per, 'spd': self.spd})
            if not isinstance(result, dict):
                self.__write_file_content__(file_path, result)
        return file_path
            
Speech = BaiduSpeech()
