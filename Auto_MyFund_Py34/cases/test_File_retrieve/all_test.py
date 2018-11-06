'''
Created on 2016-7-11

@author: Michael
'''
import os
#from pip._vendor.distlib.compat import raw_input

caselist = []
#Agility
caselist.append('Agility_CHESS_Holdings_File.py')
caselist.append('Agility_CHESS_Transactions_File.py')
caselist.append('Agility_Daily_Trades_File.py')
#ASX Daily Prices
caselist.append('ASX_Daily_Prices_File_Retrieve.py')
#ANZ_V2 added on 2017-9-12
caselist.append('ANZ_V2_Balances_File_Retrieve.py')
caselist.append('ANZ_V2_Transactions_File_Retrieve.py')
#Baillieu
caselist.append('Baillieu_Holst_Cash_Transactions_File_Retrieve.py')
caselist.append('Baillieu_Holst_CHESS_Holdings_File_Retrieve.py')
caselist.append('Baillieu_Holst_CHESS_Transaction_File_Retrieve.py')
caselist.append('Baillieu_Holst_Daily_Trades_File_Retrieve.py')
#CMC Markets  added on 2018-2-1
caselist.append('CMC_CHESS_Holdings_File_Retrieve.py')
caselist.append('CMC_CHESS_Transactions_File_Retrieve.py')
caselist.append('CMC_Daily_Trades_File_Retrieve.py')
#Desktop--added on 2017-03-20
caselist.append('Desktop_CHESS_Holdings_File.py')
caselist.append('Desktop_CHESS_Transactions_File.py')
caselist.append('Desktop_Daily_Trades_File.py')
#Macquarie
caselist.append("Macquarie_Balances_File_Retrieve.py")
caselist.append("Macquarie_Transactions_File_Retrieve.py")
#Macquarie--added on 2017-08-11
caselist.append('Macquarie_Online_Trading_CHESS_Holdings_File.py')
caselist.append('Macquarie_Online_Trading_CHESS_Transactions_File.py')
caselist.append('Macquarie_Online_Trading_Daily_Trades_File.py')
#Morgans--added on 2017-07-03
caselist.append('Morgans_CHESS_Holdings_File.py')
caselist.append('Morgans_CHESS_Transactions_File.py')
caselist.append('Morgans_Daily_Trades_File.py')
#Ozedi
caselist.append('Ozedi_PKF_Lawler_File.py')
caselist.append('Ozedi_SMSF_Lite_Plus_File.py')
caselist.append('Ozedi_Total_SMSF_File.py')
#Patersons
caselist.append('Patersons_CHESS_Holdings_File_Retrieve.py')
caselist.append('Patersons_CHESS_Transaction_File_Retrieve.py')
caselist.append('Patersons_Daily_Trades_File_Retrieve.py')
#Sentinel
caselist.append('Sentinel_CHESS_Holdings_File_Retrieve.py')
caselist.append('Sentinel_CHESS_Transactions_File_Retrieve.py')
caselist.append('Sentinel_Daily_Trades_File_Retrieve.py')
#SSIS Transaction
caselist.append('SISS_Transaction_File_Retrieve.py')
#Contract Notes
caselist.append('Contract_Notes_File_Retrieve.py')
#AMM Call Accunt--added on 2017-08-14
caselist.append('AMM_Call_Account_File_Retrieve.py')
#AMM Term Deposites
caselist.append('AMM_Term_Deposits_File_Retrieve.py')
#Template Post Processing--added on 2017-07-07
caselist.append('Auto_Template_Posting_Process.py')

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