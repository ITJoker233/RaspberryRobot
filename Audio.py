import pyaudio
import time, wave,collections,os
from logging import getLogger
logger = getLogger(__name__)

def play_audio_file(fname):
    wav = wave.open(fname, 'rb')
    wav_data = wav.readframes(wav.getnframes())
    audio = pyaudio.PyAudio()
    stream_out = audio.open(
        format = audio.get_format_from_width(wav.getsampwidth()),
        channels = wav.getnchannels(),
        rate = wav.getframerate(),
        input=False, output=True
    )
    stream_out.start_stream()
    stream_out.write(wav_data)
    time.sleep(0.2)
    stream_out.stop_stream()
    stream_out.close()
    audio.terminate()

def save_wave_file(filename, data):
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(16000)
    wf.writeframes(b"".join(data))
    wf.close()

class Audio:
    def __init__(self,detectorNumChannels,detectorSampleRate,ding_filename,dong_filename):
        if not os.path.exists('temp/'): os.mkdir('temp/')
        if not os.path.exists('cmd-wav/'): os.mkdir('cmd-wav/')
        self.ding_filename = ding_filename
        self.dong_filename = dong_filename
        self.audio = pyaudio.PyAudio()
        self.stream_in = self.audio.open(
            format = self.audio.get_format_from_width(self.detector.BitsPerSample()/8),
            channels = detectorNumChannels,
            rate = detectorSampleRate,
            frames_per_buffer = 2048,
            stream_callback = self.audio_stream_callback,
            input = True, output = False
        )
        self.rec_count = 0
        self.sil_count = 0
        self.save_buffer = []
        self.save_data = None
        self.buffer = collections.deque(maxlen=(detectorNumChannels * detectorSampleRate*5))
        
    def audio_stream_callback(self, in_data, frame_count, time_info, status):
        self.buffer.extend(in_data)
        play_data = chr(0) * len(in_data)
        return play_data, pyaudio.paContinue
    
    def record(self,filename):
        if self.rec_count > 0:
            #if play.playing == 1: music.pause_play();
            self.save_buffer.append(self.save_data)
            self.sil_count += 1
            logger.info('等待指令：', self.sil_count)
            if (self.sil_count > 30):
                logger.info('接收指令超时！')
                self.rec_count = 0
                self.sil_count = 0
                self.save_buffer = []
        if self.sil_count > 2 and self.rec_count > 1 and self.data != None:
            self.play(self.dong_filename)
            self.save(filename,self.save_data)
            self.save_buffer = []
            self.sil_count = 0
            self.rec_count = 0
            self.save_data = None
    
    def save(self,filename,data):
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(16000)
        wf.writeframes(b"".join(data))
        wf.close()
    
    def play(self,filename):
        wav = wave.open(filename, 'rb')
        wav_data = wav.readframes(wav.getnframes())
        audio = pyaudio.PyAudio()
        stream_out = audio.open(
            format = audio.get_format_from_width(wav.getsampwidth()),
            channels = wav.getnchannels(),
            rate = wav.getframerate(),
            input=False, output=True
        )
        stream_out.start_stream()
        stream_out.write(wav_data)
        time.sleep(0.2)
        stream_out.stop_stream()
        stream_out.close()
        audio.terminate()
    
    def terminate(self):
        self.stream_in.stop_stream()
        self.stream_in.close()
        self.audio.terminate()