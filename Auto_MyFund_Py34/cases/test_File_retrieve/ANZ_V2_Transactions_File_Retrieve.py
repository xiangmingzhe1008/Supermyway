'''
Created on 2016-6-5
Updated on 2017-9-12

@author: Michael xiang
'''
from selenium import webdriver
from selenium.webdriver import ActionChains
import unittest,time,logging

class Autorun(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Ie(r'../../lib/IEDriverServer.exe')
        self.driver.implicitly_wait(30)
        self.baseurl = self.readconfig()[0]
        self.verificationErrors = []
        self.accept_next_alert = True
        
        #set some values for logging
        _FORMAT = r'%(asctime)s,%(message)s'
        _Datefmt= r'%Y-%m-%d %H:%M:%S'
        _TF1 = time.strftime('%Y-%m-%d_%H%M%S', time.localtime())
        _Filename = (r'..\..\reports\test_File_retrieve\file_retrieve_%s.log' %_TF1)
        logging.basicConfig(filename=_Filename,level=logging.INFO,format=_FORMAT,datefmt=_Datefmt)
        
    def readconfig(self):
        conf = open('config.conf','r')
        lines = conf.readlines()
        param = ['','','','']
        for num in range(len(lines)):
            param[num] = lines[num].split(':',1)[1][:-1]
        return param
    
    def login(self):
        driver = self.driver
        driver.get(self.baseurl)
        driver.maximize_window()
        driver.find_element_by_id("UserName").send_keys(self.readconfig()[1])
        driver.find_element_by_id("PasswordEmpty").send_keys(self.readconfig()[2])
        nowhandle = driver.current_window_handle
        driver.find_element_by_id("cmdConfirm").click()
        time.sleep(1)
        try:
            driver.switch_to_frame('layui-layer-iframe1')
            driver.find_element_by_id('btnYes').click()
            time.sleep(1)
            try:
                driver.switch_to_frame('layui-layer-iframe1')
                driver.find_element_by_id('btnNo').click()
                time.sleep(1)
                driver.switch_to_window(nowhandle)
                driver.find_element_by_id("UserName").send_keys(self.readconfig()[1])
                driver.find_element_by_id("PasswordEmpty").send_keys(self.readconfig()[2])
                driver.find_element_by_id("cmdConfirm").click()
            except:
                pass
        except:
            pass
        time.sleep(1)
        self.listen("MasterSelectfund")   
            
    def logout(self):
        driver = self.driver        
        nowhandle = driver.current_window_handle
        driver.find_element_by_id("imgLogout").click()
        time.sleep(1)
        handles = driver.window_handles
        for handel in handles:
            if handel != nowhandle:
                driver.switch_to_window(handel)
                time.sleep(1)
                driver.find_element_by_id("btnYes").click()
        time.sleep(1)
    
    def loadingpage(self):
        driver = self.driver                      
        current_url = driver.current_url
        while current_url.find("LoadingPage") != -1: 
            current_url = driver.current_url 
            time.sleep(0.5)
        time.sleep(1)
        driver.switch_to_window(driver.window_handles[-1])
         
    def listen(self,url_fileter):
        driver = self.driver
        value = ""
        flag = 0
        while value == "":
            try:
                url = driver.find_element_by_id("hd_my_current_page_state_url").get_attribute("value")
                if (url.find(url_fileter) != -1):
                    value = "true"
            except :
                pass
            time.sleep(2)
            flag += 1
            if flag == 300:
                break
        return value        
                    
    def enter_File_Reposiry(self):
        driver = self.driver
        Data_Uploads = driver.find_element_by_link_text("Data Uploads")
        ActionChains(driver).move_to_element(Data_Uploads).perform()
        driver.find_element_by_link_text("File Repository").click()
        self.loadingpage()
        time.sleep(0.5)
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_radAutomate").click()  #Automate select        
        
    def status_judgement(self):
        driver = self.driver
        self.listen("FileRepository")
        time.sleep(1)
        status = driver.find_element_by_xpath(".//*[@id='ctl00_ContentPlaceHolder1_gvFiles']/tbody/tr[2]/td[4]").text
        if status ==  "Uploaded" :
            print("Successful")
        else :
            print("Not Uploaded")
        return status
          
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([],self.verificationErrors)  
        
    i = 1 
    def test_ANZ_V2_Transactions_File(self):
        try:
            self.i = self.i+1
            driver = self.driver
            self.login()
            self.enter_File_Reposiry()
            driver.find_element_by_id("ctl00_ContentPlaceHolder1_chkWeekend").click()
            file_name = "ANZ V2 Transactions File" 
            print(file_name)    
            driver.find_element_by_id("ctl00_ContentPlaceHolder1_ddlFile").send_keys(file_name)
            time.sleep(0.5)
            driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnDisplay").click()
            time.sleep(0.5)
            driver.find_element_by_id("ctl00_ContentPlaceHolder1_gvFiles_ctl02_chkTick").click()
            time.sleep(0.5)
            driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnRetrieve").click()  #click"Retrieve" button
            self.listen("UploadFileDataNew")   
            driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnOpen").click()
            self.listen("UploadFileDataNew")   
            driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnUpload").click()
            self.listen("FileRepository")       
            statu = self.status_judgement()
            logging.info('File Name: ' + file_name + '    Status:'+statu)
            self.logout()
        except:
            logging.exception("console information:")
            if self.i <=2:
                self.test_ANZ_V2_Transactions_File()
            else:     
                pass
           
if __name__ == '__main__':
    suite = unittest.TestSuite()    
    suite.addTest(Autorun("test_ANZ_V2_Transactions_File"))

    runner = unittest.TextTestRunner()
    runner.run(suite)