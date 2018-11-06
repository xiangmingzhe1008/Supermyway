'''
Created on 2018-01-24

@author: Michael
'''
# 17315M-17316P-SUNDAY SCRIPT AUTOMATED FILE RETRIEVAL REQUIREMENTS - 14 JANUARY 2018.docx
import os
#from pip._vendor.distlib.compat import raw_input
caselist = []
#Weekly Upload File
caselist.append('Macquarie_Balances_File_Retrieve.py')
caselist.append('Macquarie_Transactions_File_Retrieve.py')
# caselist.append('ASX_Income_File.py')
#Modified on 2018-02-05
caselist.append('ASX_Income_File_get_current_monday.py')

for n in range(1):
    m=0
    for a in caselist:
        print(a + ' is prepare to upload ' + str(n+1) +' '+str(m+1))
        cmd = 'python '+(os.getcwd()+'\\%s' %a)
        os.system(cmd)
        print(a + ' is finished ' + str(n+1) +' '+str(m+1))
        m = m+1
    n = n+1
#raw_input()