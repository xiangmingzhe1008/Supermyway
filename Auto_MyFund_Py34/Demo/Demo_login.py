'''
Created on 2016-7-5

@author: Michael
'''
from selenium import webdriver
import time

driver = webdriver.Ie(r'../test_tool/IEDriverServer.exe')
driver.get("https://www.idssuper.com.au/Pages/Login.aspx")
driver.maximize_window()
driver.find_element_by_id("UserName").clear()
driver.find_element_by_id("UserName").send_keys("masterrobot")
driver.find_element_by_id("PasswordEmpty").send_keys("Auto0507")
driver.find_element_by_id("cmdConfirm").click()
time.sleep(3)
driver.quit()