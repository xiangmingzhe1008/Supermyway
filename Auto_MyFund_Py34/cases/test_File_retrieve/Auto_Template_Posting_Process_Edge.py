# -*- coding: UTF-8 -*-
'''
Created on 10Jul.,2017

@author: xiangmingzhe
'''
from selenium import webdriver
from selenium.webdriver import ActionChains
import unittest, time, logging

class Autorun(unittest.TestCase):
    def setUp(self):
        #self.driver = webdriver.Ie(r'../../lib/IEDriverServer.exe')
        self.driver = webdriver.Edge(r'../../lib/MicrosoftWebDriver.exe')
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
        param = ['', '', '', '']
        for num in range(len(lines)):
            param[num] = lines[num].split(':', 1)[1][:-1]  # [:-1] is used to delete line break symbol
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
        nowhandle = driver.current_window_handle
        time.sleep(1)
        try:
            driver.execute_script("$('#layui-layer-iframe1').contents().find('#btnYes').click();")
            time.sleep(1)
            try:
                driver.execute_script("$('#layui-layer-iframe1').contents().find('#btnNo').click();")
                time.sleep(1)
                driver.switch_to_window(nowhandle)
                driver.execute_script(js_login)
            except:
                pass
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

    def test_Template_Posting_Process(self):
        driver = self.driver
        self.login()
        driver.get('https://www.idssuper.com.au/Pages/Admin/FundApplyProcess/FundApply.aspx')
        self.listen('FundApply')
        fund_number = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtFundsHeld").get_attribute("value")
        logging.info('Funds need to be Posted: %s'%(fund_number))
        try:            
            driver.execute_script("$('#ctl00_ContentPlaceHolder1_gvFunds').find('[type=checkbox]').prop('checked',true);")
            time.sleep(1)
            driver.execute_script("$('body').scrollTop('10000');")
            time.sleep(1)
            driver.execute_script("$('#ctl00_ContentPlaceHolder1_btnProcess').click();")
            self.listen_process()                   #waiting for Posting Process to finish, there is no 'time limit' of this method
            self.listen('FundApplyResult')    #waiting for new page loading completely
            now_handle = driver.current_window_handle
            driver.execute_script("$('#ctl00_ContentPlaceHolder1_chkDetail').click();")
            time.sleep(1)
            driver.execute_script("$('#ctl00_ContentPlaceHolder1_btnDownload').click();")
            time.sleep(1)
            try:
                driver.execute_script("$('#layui-layer-iframe1').contents().find('#btnNo').click();")
            except:
                pass
            time.sleep(10)
            driver.switch_to_window(now_handle)
            
            driver.find_element_by_xpath(".//*[@id='ctl00_ContentPlaceHolder1_ddlStatus']/option[5]").click()            
            time.sleep(1)
            driver.execute_script("$('#ctl00_ContentPlaceHolder1_btnDisplay').click();")   
            time.sleep(2)
            fund_complete = driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtNumber").get_attribute("value")
            fund_unpost = int(fund_complete) - int(fund_number)
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
            print('There is no Fund to Process !')
            logging.info('There is no Fund to Process !')
            self.logout()
            pass
        
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(Autorun("test_Template_Posting_Process"))
    
    runner = unittest.TextTestRunner()
    runner.run(suite)
