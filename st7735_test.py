import time
from machine import Pin, SPI
spi = SPI(1, 20000000, sck=Pin(27), mosi=Pin(26), miso=Pin(34))
from st7735 import ST7735
#lcd = ILI9341(240, 320, spi,dc=Pin(25),cs=Pin(32),rst=Pin(33))#竖屏初始化
lcd = ST7735(160, 80, spi,dc=Pin(33),cs=Pin(32),rst=Pin(25),rot=1,bgr=0)#横屏初始化参数rot，交换红蓝位置用bgr=1
#lcd.font_load("GB2312-32.fon")
bl=Pin(4,Pin.OUT)
bl.value(1)
#加载的字库是中文，可以选12，16，24，32四种中文
for i in range(8):
    for j in range(32):
        lcd.fill_rect(j*5,i*10,5,10,lcd.rgb(j*8*((i>>0)&0x01),j*8*((i>>1)&0x01),j*8*((i>>2)&0x01)))
lcd.show()
lcd.save("colbar.bmp")
time.sleep(2)
lcd.show_bmp("lt.bmp")
time.sleep(2)
   
for count in range(20):
    lcd.fill(0)
    lcd.font_set(0x11,0,1,0)
    #字体(第一位1-4对应标准，方头，不等宽标准，不等宽方头，第二位1-4对应12，16，24，32高度)，旋转，放大倍数，反白显示
    lcd.text("Micropython中文甒甒%d"%count,0,0,0xf800)
    lcd.font_set(0x12,0,1,1)
    lcd.text("micro拷贝甓甓",0,16,0x07e0)
    lcd.font_set(0x13,0,1,0)
    lcd.text("甒字符串Mpy%3.3d"%count,0,32,lcd.rgb(255,255,255))
    #lcd.rgb()是方便设置显示颜色的小功能
    lcd.font_set(0x44,0,1,0)
    lcd.text("甓中文Mpy%3.3d"%count,0,50,0x001f)
    lcd.show()

for count in range(81):
    lcd.fill(0)
    lcd.show_bmp("logo-2.bmp",count*3-80,count*2-80)
    lcd.show()
lcd.font_free()
