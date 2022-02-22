RaspberryRobot
======
RaspberryRobot是一个中文人工智能机器人。支持语音唤起、智能音箱、对话机器人项目

安装第三方工具
```
#树莓派安装：https://github.com/LiveXY/elearning/blob/master/raspberrypi4.txt
sudo apt install python-pyaudio python3-pyaudio sox swig libatlas-base-dev mplayer -y
#MAC安装
brew install swig portaudio sox mplayer
```

编译_snowboydetect.so文件
```
git clone https://github.com/Kitt-AI/snowboy
cd snowboy/swig/Python3
make
cp _snowboydetect.so RaspberryRobot/
```

免费申请百度语音识别等API
```
1. 百度语音识别申请：http://ai.baidu.com/
2. 申请成功后更改config.py文件中的BAIDUS变量
```

安装启动方法：
```
git clone https://github.com/ITJoker233/RaspberryRobot
cd RaspberryRobot/
pip3 install -r requirements.txt
python3 app.py
```

语音测试
```
说：“冰冰” 可语音唤起，叮一声后录音

```

更换唤醒词
```
1，登陆https://snowboy.kitt.ai/
2，进入https://snowboy.kitt.ai/dashboard
3，点击“ Create Hotword ”按钮，按提示生成自己的唤醒词并下载到项目的resources目录
4，更改config.py文件中的MODELS变量，如果支持多个唤醒词使用逗号分隔（同时要更改SENSITIVITY变量）
```

代码文件详解
```
AI.py  #机器人核心处理中间件
app.py #启动程序
Audio.py # wav音频文件处理库
config.py #配置文件
logging.py #日志处理库
Middleware.py #中间件
Player.py #mplayer播放器的操作类
Robot.py #snowboy唤起识别
snowboydetect.py #snowboy官方代码
Speech.py #语音识别
```
