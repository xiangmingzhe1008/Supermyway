# -*- coding: UTF-8 -*-
#import time
import  win32gui, win32ui, win32con, win32api, os

def window_capture(filename, srcbmp=[0, 0, None, None]):
    hwnd = 0
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC=win32ui.CreateDCFromHandle(hwndDC)
    saveDC=mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    MoniterDev=win32api.EnumDisplayMonitors(None,None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    if srcbmp[2]==None or (srcbmp[0]+srcbmp[2]>w):
        srcbmp[2] = w
    if srcbmp[3]==None or (srcbmp[1]+srcbmp[3]>w):
        srcbmp[3] = h
    saveBitMap.CreateCompatibleBitmap(mfcDC, srcbmp[2], srcbmp[3])
    saveDC.SelectObject(saveBitMap)
    ddss = (srcbmp[2], srcbmp[3])
    saveDC.BitBlt((0,0), ddss , mfcDC, (srcbmp[0], srcbmp[1]), win32con.SRCCOPY)
    #cc=time.gmtime()
    #print(os.path.abspath('..\..\\reports\\screenshot\\'))
    bmpname = os.path.abspath('..\\reports\\screenshot\\') +'\\' + filename
    print(bmpname)
    saveBitMap.SaveBitmapFile(saveDC, bmpname)    
if __name__ == '__main__':
    window_capture('test.png')   