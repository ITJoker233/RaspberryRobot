import signal,os
from Robot import signal_handler
from config import RESOURCE_FILE, DETECT_DING, DETECT_DONG, MODELS, SENSITIVITY,TEMP_PATH
from AI import AI
from Robot import Brian

if not os.path.exists(TEMP_PATH): os.mkdir(TEMP_PATH)

signal.signal(signal.SIGINT, signal_handler)

brian = Brian(
    model_str = MODELS,
    resource_filename = RESOURCE_FILE,
    sensitivity = SENSITIVITY,
    audio_gain = 1,
    ding_filename = DETECT_DING,
    dong_filename = DETECT_DONG
)

brian.middleware.add(AI);
    
brian.start()
brian.terminate()
