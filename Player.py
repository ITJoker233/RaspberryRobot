import subprocess, threading, time

class MPlayer(object):
    def __init__(self):
        self.music_list = []
        self.player_handler = None
        self.playing = 0;
        self.current_list = []
        self.current_index = 0
        self.shuffle = False
        self.loop = False
        self.exit = False
  
    def pause_play(self):
        if self.playing:
            self.playing = 2
            self.player_handler.stdin.write(b'p')
            self.player_handler.stdin.flush()
        return False

    def continue_play(self):
        if self.playing:
            self.playing = 1
            self.player_handler.stdin.write(b'c')
            self.player_handler.stdin.flush()
        return False

    def inc_volume(self):
        if self.playing:
            self.player_handler.stdin.write(b'*')
            self.player_handler.stdin.flush()
        return False

    def dec_volume(self):
        if self.playing:
            self.player_handler.stdin.write(b'/')
            self.player_handler.stdin.flush()
        return False

    def backward(self):
        if self.playing:
            self.player_handler.stdin.write(b'<-')
            self.player_handler.stdin.flush()
        return False

    def forward(self):
        if self.playing:
            self.player_handler.stdin.write(b'->')
            self.player_handler.stdin.flush()
        return False

    def play_next(self):
        thread = threading.Thread(target=self.mplayer, name="mplayer")
        thread.setDaemon(True)
        thread.start()

    def quit_play(self):
        if self.playing:
            self.player_handler.stdin.write(b'q')
            self.player_handler.stdin.flush()
        return False

    def close_music(self):
        self.exit = True
        self.playing = 0
        self.current_list.clear()
        self.current_index = 0
        self.player_handler.stdin.write(b'q')
        self.player_handler.stdin.flush()
        time.sleep(0.5)
        self.player_handler.kill()
        time.sleep(0.5)
        subprocess.run("killall mplayer", shell=True)
        return False
    
    def play(self,file):
        self.player_handler = subprocess.Popen(["mplayer", file], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.playing = 1
        while True:
            if self.exit: break
            strout = self.player_handler.stdout.readline()
            if strout == b'Exiting... (End of file)\n' or strout == b'Exiting... (Quit)\n':
                self.playing = 0
                break
            
Player = MPlayer()