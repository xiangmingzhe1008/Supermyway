# -*- coding: UTF-8 -*-
'''
Created on 2017年9月29日

@author: xiangmingzhe
'''
from selenium import webdriver
import time

from os.path import sys
sys.path.append(r'../../lib/')
from key_mouse_control_by_win32com import *

mouse_click(1324, 10)
driver = webdriver.Edge(r'../../lib/MicrosoftWebDriver_for_Edge_15063.exe')
driver.maximize_window()
driver.get('https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/')
time.sleep(3)
driver.find_element_by_link_text('Release 15063').click()
#driver.execute_script("$('.driver-download .subtitle').click();")
time.sleep(3)
mouse_click(1160,1010)



