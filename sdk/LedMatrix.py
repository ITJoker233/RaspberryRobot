from ..drivers.LedMatrix import LEDMATRIX

class MATRIX:
    device = None
    Emoticons = {
        'happy':'(^v^)', # 开心
        'angry':'*=M=', # 生气
        'sad':'(T-T)', # 悲伤
        'speechless':'(- -|)', #无语
        'surprised':'(0o0)', #惊讶
        'hello':'(-O-)', #打招呼
        'think':'think...', #思考
        'listen':'-0-?',
        'default':' - ',
        'error':'(X_X)' #错误
    }
    def __init__(self):
        self.device = LEDMATRIX()
    def _draw_emoticon(self,emo,scroll,scroll_model,scroll_delay):
        self.device.draw_text(self.Emoticons.get(emo.lower(),self.Emoticons['error']),scroll=scroll,scroll_model=scroll_model,scroll_delay=scroll_delay)

    def _change_emoticon(self,emo,new_emo):
        self._draw_emoticon(emo,True,0,0.01)
        self._draw_emoticon(new_emo,False,0,0.5)
        self.device.breathe_intensity()

    def show_emoticon(self,emo):
        self._change_emoticon('error',emo)


LedMatrix = MATRIX()