'''
Created on 2017-10-16

@author: xiangmingzhe
'''
from selenium import webdriver
from selenium.webdriver import ActionChains
import unittest, time, logging

from os.path import sys
sys.path.append(r'../../lib/')
from key_mouse_control_by_win32com import *

class Autorun(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Ie(r'../../lib/IEDriverServer.exe')
        self.driver.implicitly_wait(30)
        self.baseurl = self.readconfig()[0]
        self.verificationErrors = []
        self.accept_next_alert = True

        _FORMAT = r'%(asctime)s,%(message)s'
        _Datefmt = r'%Y-%m-%d %H:%M:%S'
        _TF1 = time.strftime('%Y-%m-%d_%H%M%S', time.localtime())
        _Filename = (r'..\..\reports\test_Template_Posting_Process\Template_Posting_Process%s.log' % _TF1)
        logging.basicConfig(filename=_Filename, level=logging.INFO, format=_FORMAT, datefmt=_Datefmt)

    def readconfig(self):
        conf = open('config.conf', 'r')
        lines = conf.readlines()
        param = []        
        #param = ['', '', '', '']
        for num in range(len(lines)):
            param.append(lines[num].split(':', 1)[1][:-1])
            #param[num] = lines[num].split(':', 1)[1][:-1]  # [:-1] is used to delete line break symbol
        return param
    
    def login(self):
        driver = self.driver
        driver.maximize_window()
        driver.get(self.baseurl)
        self.listen('Login')
        js_login = "$('#cmdConfirm').unbind('click').bind('click',function(){ return true;});$('#UserName').val('"+ self.readconfig()[1] +"');$('#Password').val('"+ self.readconfig()[2] +"');$('#cmdConfirm').click();"
        driver.execute_script(js_login)
        try:
            driver.execute_script("$('#layui-layer-iframe1').contents().find('#btnNo').click();")
            driver.execute_script(js_login)
        except:
            pass  
        time.sleep(2)
        try:
            driver.execute_script("$('#layui-layer-iframe1').contents().find('#btnNo').click();")
            driver.execute_script(js_login)
        except:
            pass                       
        time.sleep(1)
        try:
            driver.execute_script("$('#layui-layer-iframe1').contents().find('#btnYes').click();")
            time.sleep(3)            
        except:
            pass
        try:
            driver.execute_script("$('#layui-layer-iframe1').contents().find('#btnNo').click();")
            time.sleep(1)
            driver.execute_script(js_login)
        except:
            pass
        time.sleep(1)        
        
    def logout(self):
        driver = self.driver        
        driver.execute_script("$('#imgLogout').click();")
        time.sleep(1)
        try:
            driver.execute_script("$('#layui-layer-iframe1').contents().find('#btnYes').click();")
            time.sleep(2)
        except:
            pass
        time.sleep(1)

    def loadingpage(self):
        driver = self.driver                      
        current_url = driver.current_url
        while current_url.find("LoadingPage") != -1:
            current_url = driver.current_url
            time.sleep(0.5)
        time.sleep(1)
        driver.switch_to_window(driver.window_handles[-1])
    
    def listen(self, url_fileter):
        driver = self.driver
        value = ""
        flag = 0
        while value == "":
            try:
                url = driver.find_element_by_id("hd_my_current_page_state_url").get_attribute("value")
                if url.find(url_fileter) != -1:
                    value = "Found It!"
            except:
                pass
            time.sleep(1)
            flag += 2
            if flag == 300:
                break
        return value 
         
    def listenNoParam(self):
        driver = self.driver
        value =""
        flag = 0
        while value =="" :
            try:
                value = driver.find_element_by_id("hd_my_current_page_state_url").get_attribute("value")
            except :
                pass
            time.sleep(2)
            flag += 2
            if flag == 300:
                break
        return value       

    def enter_TPP(self):
        driver = self.driver
        menu = driver.find_element_by_link_text("Fund Reporting")
        ActionChains(driver).move_to_element(menu).perform()
        driver.find_element_by_link_text("Template Posting Process").click()   
        
    def listen_process(self):
        driver = self.driver
        value = "Not Null"
        while value == "Not Null" :
            try:                
                driver.find_element_by_id('lblprocess').text
            except :
                value = "Null"
            time.sleep(1)
        return value      
     
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([],self.verificationErrors)
        
    i = 0

    def test_Template_Posting_Process(self):
        driver = self.driver
        self.login()
        logging.info('login passed')
        driver.get('https://www.idssuper.com.au/Pages/Admin/FundApplyProcess/FundApply.aspx')
        logging.info('Enter page passed')
        self.listen('FundApply')
        fund_number = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtFundsHeld").get_attribute("value")
        logging.info('Funds need to be Posted: %s'%(fund_number))
        if int(fund_number) == 0:
            print('There is no Fund to Process !')
            logging.info('There is no Fund to Process !')
            self.logout()
        else:            
            try:            
                driver.execute_script("$('#ctl00_ContentPlaceHolder1_gvFunds').find('[type=checkbox]').prop('checked',true);")
                time.sleep(1)
                js = "var q=document.documentElement.scrollTop=10000;"      #Scroll to the bottom of the current screen
#                 js = "window.scrollTo(0,document.body.scrollHeight);"
#                 js = "$('body').scrollTop('10000');"
                driver.execute_script(js)
                time.sleep(1)
                driver.execute_script("$('#ctl00_ContentPlaceHolder1_btnProcess').click();")
                logging.info('process button clicked')
                self.listen_process()                   #waiting for Posting Process to finish, there is no 'time limit' of this method
                self.listen('FundApplyResult')    #waiting for new page loading completely
                driver.execute_script("$('#ctl00_ContentPlaceHolder1_btnDownloadHidden').click();")
                logging.info('download button clicked')            
                time.sleep(10)
                mouse_click(1280, 1020)             #click "Save" button of IE download control
                logging.info('mouse1 clicked')
                time.sleep(3)
                mouse_click(1425, 1019)             #close IE download control
                logging.info('mouse2 clicked')
                
                driver.find_element_by_xpath(".//*[@id='ctl00_ContentPlaceHolder1_ddlStatus']/option[5]").click()
                logging.info('option selected')            
                time.sleep(1)
                driver.execute_script("$('#ctl00_ContentPlaceHolder1_btnDisplay').click();")
                logging.info('display clicked')   
                time.sleep(2)
                fund_complete = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtNumber").get_attribute("value")
                logging.info('get complete fund number')  
                fund_unpost = int(fund_complete) - int(fund_number)
                logging.info('calculate unpost fund number')
                if fund_unpost < 0:
                    logging.info('Funds Finished: %s'%(fund_complete))
                    self.logout()
                    self.test_Template_Posting_Process()
                else:
                    logging.info('Funds Finished: %s'%(fund_complete))
                    print('Template Posting Process Successful !')
                    logging.info('Template Posting Process Successful !')
                    self.logout()
            except:
                logging.info('Error during running !')
                if self.i < 1:
                    self.i = self.i+1
                    self.logout()
                    self.test_Template_Posting_Process()
                else:
                    self.logout()
        
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(Autorun("test_Template_Posting_Process"))
    
    runner = unittest.TextTestRunner()
    runner.run(suite)
        