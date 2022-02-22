import time

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text
from luma.core.legacy.font import proportional,  tolerant, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

class LEDMATRIX:
    #def __init__(self):
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-90, width=8, height=32)

    def show(self):
        self.device.show()

    def hide(self):
        self.device.hide()

    def clear(self):  # 初始化设备内存
        self.device.clear()

    def cleanup(self): # 清除屏幕并关闭与底层串行接口相关的资源
        self.device.cleanup()

    def draw_image(self):
        pass

    def draw_rectangle(self):
        virtual = viewport(self.device, width=self.device.width, height=self.device.height)
        with canvas(virtual) as draw:
            draw.rectangle(self.device.bounding_box, outline="white", fill="black")
            
    def draw_text(self,txt,scroll=False,scroll_model=1,scroll_delay=0.05): # model {width:1,heigth:0}
        text_length=len(txt)
        virtual = viewport(self.device, width=text_length*8, height=text_length*8)
        with canvas(virtual) as draw:
            text(draw, (0, 0), str(txt), fill="white", font=proportional( tolerant(CP437_FONT) ))
        if scroll:
            if scroll_model:
                self.width_scrolling(virtual,scroll_delay)
            else:
                self.height_scrolling(virtual,scroll_delay)

    def height_scrolling(self,virtual,scroll_delay):
        for i in range(virtual.height - self.device.height):
            virtual.set_position((0, i))
            time.sleep(scroll_delay)

    def width_scrolling(self,virtual,scroll_delay):
        for i in range(virtual.width - self.device.width):
            virtual.set_position((i, 0))
            time.sleep(scroll_delay)

    def set_intensity(self,intensity):
        if intensity >= 0 and intensity <=100:
            self.device.contrast(int(intensity * 255))
        else:
            self.device.contrast(int(50.0 * 255))
    
    def breathe_intensity(self):
        for _ in range(2):
            for intensity in range(16):
                self.device.contrast(intensity * 16)
                time.sleep(0.1)