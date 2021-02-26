from time import sleep_ms
from ustruct import pack
from machine import SPI,Pin
from micropython import const
import framebuf

#   ST7735V registers definitions

NOP     = const(0x00) # No Operation
SWRESET = const(0x01) # Software reset

SLPIN   = const(0x10) # Sleep in & booster off
SLPOUT  = const(0x11) # Sleep out & booster on
PTLON   = const(0x12) # Partial mode on
NORON   = const(0x13) # Partial off (Normal)

INVOFF  = const(0x20) # Display inversion off
INVON   = const(0x21) # Display inversion on
DISPOFF = const(0x28) # Display off
DISPON  = const(0x29) # Display on
CASET   = const(0x2A) # Column address set
RASET   = const(0x2B) # Row address set
RAMWR   = const(0x2C) # Memory write
RGBSET  = const(0x2D) # Display LUT set

PTLAR   = const(0x30) # Partial start/end address set
COLMOD  = const(0x3A) # Interface pixel format
MADCTL  = const(0x36) # Memory data access control

# panel function commands
FRMCTR1 = const(0xB1) # In normal mode (Full colors)
FRMCTR2 = const(0xB2) # In Idle mode (8-colors)
FRMCTR3 = const(0xB3) # In partial mode + Full colors
INVCTR  = const(0xB4) # Display inversion control

PWCTR1  = const(0xC0) # Power control settings
PWCTR2  = const(0xC1) # Power control settings
PWCTR3  = const(0xC2) # In normal mode (Full colors)
PWCTR4  = const(0xC3) # In Idle mode (8-colors)
PWCTR5  = const(0xC4) # In partial mode + Full colors
VMCTR1  = const(0xC5) # VCOM control

GMCTRP1 = const(0xE0)
GMCTRN1 = const(0xE1)



class ST7735(framebuf.FrameBuffer):
    def __init__(self, width, height, spi, dc, rst, cs, rot=0, bgr=0, external_vcc=False):
        if dc is None:
            raise RuntimeError('TFT must be initialized with a dc pin number')
        dc.init(dc.OUT, value=0)
        if cs is None:
            raise RuntimeError('TFT must be initialized with a cs pin number')
        cs.init(cs.OUT, value=1)
        if rst is not None:
            rst.init(rst.OUT, value=1)
        else:
            self.rst =None
        self.spi = spi
        self.rot = rot
        self.dc = dc
        self.rst = rst
        self.cs = cs
        self.height = height
        self.width = width
        self.external_vcc = external_vcc
        self.buffer = bytearray(self.height * self.width*2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565SW, self.width)
        if (self.rot ==0):
            madctl=0x00
        elif (self.rot ==1):
            madctl=0xa0
        elif (self.rot ==2):
            madctl=0xc0
        else :
            madctl=0x60
        if bgr==0:
            madctl|=0x08
        self.madctl = pack('>B', madctl)
        self.reset()

        self._write(SLPOUT)
        sleep_ms(120)
        for command, data in (
            (COLMOD,  b"\x05"),
            (MADCTL,  pack('>B', madctl)),
            (INVON,   None),

            #(GMCTRP1, b"\0x03\0x1d\0x07\0x06\0x2e\0x2c\0x29\0x2d\0x2e\0x2e\0x37\0x3f\0x00\0x00\0x02\0x10"),
            #(GMCTRN1, None),
            ):
            self._write(command, data)
        buf=bytearray(128)
        for i in range(32):
            buf[i]=i*2
            buf[i+96]=i*2
        for i in range(64):
            buf[i+32]=i
        self._write(RGBSET, buf)
        #self._write(NORON)
        #sleep_ms(10)
        self.show()
        self._write(DISPON)
        #sleep_ms(100)
    def reset(self):
        if self.rst is None:
            self._write(SWRESET)
            sleep_ms(50)
            return
        self.rst.off()
        sleep_ms(50)
        self.rst.on()
        sleep_ms(50)
    def _write(self, command, data = None):
        self.cs.off()
        self.dc.off()
        self.spi.write(bytearray([command]))
        self.cs.on()
        if data is not None:
            self.cs.off()
            self.dc.on()
            self.spi.write(data)
            self.cs.on()
    def show(self):
        if self.rot==0 or self.rot==2:
            self._write(CASET,pack(">HH", 26, self.width+26-1))
            self._write(RASET,pack(">HH", 1, self.height+1-1))
        else:
            self._write(CASET,pack(">HH", 1, self.width+1-1))
            self._write(RASET,pack(">HH", 26, self.height+26-1))
        self._write(RAMWR,self.buffer)
    def rgb(self,r,g,b):
        return ((r&0xf8)<<8)|((g&0xfc)<<3)|((b&0xf8)>>3)


        

        
