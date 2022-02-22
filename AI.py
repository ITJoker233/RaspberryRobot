import requests
import json
from Player import Player
from Speech import Speech
from config import ROBOT_NAME,MASTER_NAME
from logging import getLogger
logger = getLogger(__name__)

class AiMiddleware(object):
    
    def handle(self, context):
        logger.info('AI:', context)
        if (len(context) >= 2):
            self.answer(context)
        return False
    
    def answer(self, context):
        url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg='+context
        response = requests.get(url)
        data = json.loads(response.text)
        text = '抱歉, 我的大脑短路了,请稍后再试试.'
        if data['result'] == 0:
            text = data.get('content').replace('菲菲',ROBOT_NAME).replace('主人',MASTER_NAME)
        tts_filepath = Speech.tts(text)
        logger.info('AI:', text,tts_filepath)
        Player.play(tts_filepath)
        
AI = AiMiddleware()

if __name__ == '__main__':
    AI.handle('你好')

