'''
Created on 2016-7-6

@author: Michael
'''

from selenium import webdriver
from selenium.webdriver import ActionChains
import unittest, time, logging

from os.path import sys
sys.path.append(r'../../lib/')
from Screenshot import window_capture

class Fund_Initiate(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Ie(r'../../lib/IEDriverServer.exe')
        self.driver.implicitly_wait(30)
        self.baseurl = self.readconfig()[0]
        self.fundname = self.readconfig()[3]
        self.verificationErrors = []
        self.accept_next_alert = True

        _FORMAT = r'%(asctime)s,%(message)s'
        _Datefmt = r'%Y-%m-%d %H:%M:%S'
        _TF1 = time.strftime('%Y-%m-%d_%H%M%S', time.localtime())
        _Filename = (r'..\..\reports\test_Pre_compile\Pre_compile_%s.log' % _TF1)
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
        driver.get(self.baseurl)
        driver.maximize_window()
        driver.find_element_by_id("UserName").send_keys(self.readconfig()[1])
        driver.find_element_by_id("PasswordEmpty").send_keys(self.readconfig()[2])
        nowhandle = driver.current_window_handle
        driver.find_element_by_id("cmdConfirm").click()
        time.sleep(1)
        handles = driver.window_handles
        for handel in handles:
            if handel != nowhandle:
                driver.switch_to_window(handel)
                time.sleep(1)
                driver.find_element_by_id("btnYes").click()
                driver.switch_to_window(nowhandle)
        time.sleep(1)
        self.listen("MasterSelectfund")

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
            time.sleep(2)
            flag += 1
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
            flag += 1
            if flag == 300:
                break
        return value       
        
        
    def loadfinished(self,category,entry_type,starttime):
        driver = self.driver
        time.sleep(2)
        self.listen("Entry")    
        pre_button = driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnPrevious")
        ActionChains(driver).click(pre_button).perform()
        self.listen("PostTransaction")
        stoptime = time.strftime('%H:%M:%S', time.localtime())
        logging.info('Category is : '+category+'    Entry type is : ' + entry_type + "    start at:" + starttime + "    stop at:" + stoptime)
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([],self.verificationErrors)
        
    i = 1
        
    def test_cr_cashtransfer(self):
        try:
            self.i += 1
            driver = self.driver
            self.login()
#             driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnViewFund").click()
            driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtCriteria").send_keys(self.fundname)
            driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnDisplay").click()
            self.loadingpage()
            driver.find_element_by_xpath(".//*[@id='ctl00_ContentPlaceHolder1_gvFunds_ctl02_lblFundName']").click()
            self.loadingpage()
            driver.find_element_by_id("ctl00_ContentPlaceHolder1_btnDisplay").click()
            self.loadingpage()
            time.sleep(1)
            driver.find_element_by_xpath(".//*[@id='ctl00_ContentPlaceHolder1_gvTransaction']/tbody/tr[2]/td[2]").click()
            self.loadingpage()
            time.sleep(1)
            file_path = r"..\..\data\test_Pre_compile\cr_cashtransfer.csv"
            data = open(file_path)
            dl = data.read().splitlines()
            counts = len(open(file_path,'r').readlines())
            data.close()
            for line in range(counts):
                value = dl[line].split(',')
                print(value[1])
                time.sleep(1)
                categorys = driver.find_element_by_id("ctl00_ContentPlaceHolder1_EntrySelectorControl1_ddlPostingCategory")
                categorys.find_element_by_xpath("//option[@value='33']").click()
                time.sleep(1)
                types = driver.find_element_by_id("ctl00_ContentPlaceHolder1_EntrySelectorControl1_ddlPostingSubCategory")
                xpath = "//option[@value='"+value[2]+"']"
                types.find_element_by_xpath(xpath).click()
                starttime = time.strftime('%H:%M:%S', time.localtime())
                self.loadfinished(value[0],value[1],starttime)
        except:
            logging.exception("console information:")
            current_time = time.strftime('%Y%m%d%H%M%S', time.localtime())
            pic_name = value[0] + '_' + value[1] + current_time + '.png'
            window_capture(pic_name)
            if self.i <=2:
                self.test_cr_cashtransfer()
            else:     
                pass
            
if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(Fund_Initiate("test_cr_cashtransfer"))
    runner = unittest.TextTestRunner()
    runner.run(suite)   
    
