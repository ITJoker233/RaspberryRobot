
RESOURCE_FILE = 'resources/common.res'
DETECT_DING = 'resources/ding.wav'
DETECT_DONG = 'resources/dong.wav'
MODELS = 'resources/hotword.pmdl'

SENSITIVITY = '0.5'

TEMP_PATH = 'temp/'

NLU_ENABLE = True
NLU_WORD_ENABLE = True
NLU_SENTIMENT_ENABLE = True

ROBOT_NAME = '冰冰'
MASTER_NAME = '主人'


#confog.json 的模板
'''

{
    "APP_ID": "",
    "API_KEY": "",
    "SECRET_KEY": ""
}

'''

with open('baidu.json','r') as f:
	import json 
	BAIDUS = [json.loads(f.read())]