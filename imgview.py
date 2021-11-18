import ctypes,os,sys,numpy as np
from PIL import Image
LF_FACESIZE = 32
STD_OUTPUT_HANDLE = -11

class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

class CONSOLE_FONT_INFOEX(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_ulong),
                ("nFont", ctypes.c_ulong),
                ("dwFontSize", COORD),
                ("FontFamily", ctypes.c_uint),
                ("FontWeight", ctypes.c_uint),
                ("FaceName", ctypes.c_wchar * LF_FACESIZE)]
def set_font():
    font = CONSOLE_FONT_INFOEX()
    font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
    font.nFont = 12
    font.dwFontSize.X = 1
    font.dwFontSize.Y = 1
    font.FontFamily = 54
    font.FontWeight = 0
    font.FaceName = "Consolas"

    handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    ctypes.windll.kernel32.SetCurrentConsoleFontEx(
            handle, ctypes.c_long(False), ctypes.pointer(font))

class _CursorInfo(ctypes.Structure):
    _fields_ = [("size", ctypes.c_int),("visible", ctypes.c_byte)]

def hide_cursor():
    ci = _CursorInfo()
    handle = ctypes.windll.kernel32.GetStdHandle(-11)
    ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))
    ci.visible = False
    ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))

def get_ansi(r, g, b):
    if r == g and g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231
        return round(((r - 8) / 247) * 24) + 232
    return 16 + (36 * round(r / 255 * 5)) + (6 * round(g / 255 * 5)) + round(b / 255 * 5)

def get_color(r, g, b):
    return "\x1b[0m\x1b[48;5;{}m ".format(int(get_ansi(r,g,b)))

def loadPicture(cha, resize=300, al=Image.ANTIALIAS,fast=True):
    ascimg=[]
    try:
        img = Image.open(cha)
    except:
        exit('File not found')
    if img.size[0] > img.size[1]:
        img = img.resize((resize*3, int(resize * img.size[1] / img.size[0])), al)
    else:
        img = img.resize((int(resize * img.size[0] * 3 / img.size[1]), resize), al)
    img_arr=np.asarray(img)
    h,w,c=img_arr.shape
    for x in range(h):
        tim=[]
        for y in range(w):
            pix=img_arr[x][y]
            try:
                alh=pix[3]
            except:
                alh=255
            if alh != 0:
                tim.append(str(get_color(pix[0],pix[1],pix[2])))
            else:
                tim.append(' ')
        ascimg.append(tim)
    if fast:
        for alist in ascimg:
            for i in range(len(alist) - 1, 0, -1):
                if alist[i] == alist[i-1]:
                    alist[i] = ' '
            for i in ascimg:
                i[-1] = i[-1]+'\x1b[0m'
    return '\n'.join([''.join(i) for i in ascimg]),h,w

def init_con(cols,lines):
    os.system(f'mode con cols={cols} lines={lines}')

def main():
    hide_cursor()
    os.system(f' title {os.path.basename(sys.argv[1]).split(".")[0]}')
    os.system('cls')
    set_font()
    image,h,w=loadPicture(sys.argv[1],fast=True)
    init_con(w,h)
    print(image)
    init_con(w,h)
    sys.stdout.write(image)
    input()
    
if __name__ == '__main__':
    main()
    