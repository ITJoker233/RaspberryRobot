import time,subprocess
import snowboydetect
from Audio import Audio
from Speech import Speech
from Player import Player
from sdk.LedMatrix import LedMatrix
from sdk.NLU import nlu
from Middleware import middleware
from config import TEMP_PATH,NLU_ENABLE
from logging import getLogger
logger = getLogger(__name__)

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

class Brian(object):
    def __init__(self, model_str, resource_filename, sensitivity, audio_gain,ding_filename, dong_filename):
        self.speech = Speech
        self.player = Player
        self.middleware = middleware
        
        self.detector = snowboydetect.SnowboyDetect(
            resource_filename = resource_filename.encode(),
            model_str = model_str.encode()
        )
        self.detector.SetSensitivity(sensitivity.encode())
        self.detector.SetAudioGain(audio_gain)

        self.audio = Audio(self.detector.NumChannels(),self.detector.SampleRate(), ding_filename, dong_filename)
        
        '''
        logger.info('量化位数：%d'%self.audio.get_format_from_width(self.detector.BitsPerSample()/8))
        logger.info('声道数：%d'%self.detector.NumChannels())
        logger.info('频率：%d'%self.detector.SampleRate())
        logger.info('关键词：%d'%self.detector.NumHotwords())
        logger.info('等待语音激活...')
        '''


    def listen(self,sleep_time):
        global interrupted
        if interrupted: return
        while True:
            if interrupted: break

            self.audio.save_data = bytes(bytearray(self.audio.save_buffer))
            self.audio.save_buffer.clear()

            if len(self.audio.save_data) == 0:
                time.sleep(sleep_time)
                continue
            LedMatrix.show_emoticon('default')
            ans = self.detector.RunDetection(self.audio.save_data)
            if ans is 1:
                LedMatrix.show_emoticon('hello')
                logger.info('语音唤醒成功！')
                self.audio.play(self.audio.ding_filename)
                self.audio.save_buffer = []
                self.audio.rec_count = 1
                self.audio.save_data = bytes(bytearray(self.audio.save_buffer))
                self.audio.save_buffer.clear()
            elif ans is 0:
                if self.audio.rec_count > 0:
                    LedMatrix.show_emoticon('listen')
                    logger.info('正在接收指令：', self.audio.rec_count)
                    self.audio.save_buffer.append(self.audio.save_data)
                    self.audio.rec_count += 1
                    self.audio.sil_count = 0
                    if (self.audio.rec_count > 60):
                        ans = -2
                        self.audio.sil_count = 3
            elif ans is -2:
                #if music.playing == 1: music.pause_play();
                filename = TEMP_PATH+'rec.wav'
                self.audio.record(filename)
                context = self.speech.asr(filename)
                self.think(context)
                logger.info('等待语音唤醒...')

    def speak(self, context):        
        tts_path = self.speech.tts(context,TEMP_PATH)
        if self.player.playing == 1 and context: self.player.pause_play();
        time.sleep(0.5)
        subprocess.run(["mplayer", tts_path])
        time.sleep(0.5)
        if self.player.playing == 2 and context: self.player.continue_play();
        return False

    def think(self, context):
        LedMatrix.show_emoticon('think')
        logger.info('接收到指令：%s'%context)
        if NLU_ENABLE:
            nlu_word_resp = self.nlu('words',context)['data']
            nlu_word_resp_len = len(nlu_word_resp)
            if 1 == nlu_word_resp_len%2:
                nlu_word_resp.popitem()
            nlu_res = ''.join([nlu_word_resp[x] for x in nlu_word_resp])
            logger.info('识别的指令：%s'%nlu_res)
            context = nlu_res
        self.middleware.handle(context)

    def nlu(self, func_name,context):
        result = None
        if func_name == 'sentiment':
            result = nlu.sentiment(context)
        elif func_name == 'words':
            result = nlu.wordsAnalysis(context)
        return result
    
    def run(self,sleep_time = 0.03):
        self.listen(sleep_time)
