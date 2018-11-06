'''
Created on 2017-9-6

@author: Michael
'''
import os

caselist = []
#Cash_CR
caselist.append('Cash_CR_CashTransfer.py')
caselist.append('Cash_CR_FundIncome.py')
caselist.append('Cash_CR_CorporateActions.py')
caselist.append('Cash_CR_FinancialAssetSale.py')
caselist.append('Cash_CR_NonFinancialAssetSale.py')
caselist.append('Cash_CR_DerivativesExercise.py')
caselist.append('Cash_CR_OtherContributions.py')
caselist.append('Cash_CR_TransactionAdjustments.py')
#Cash_DR
caselist.append('Cash_DR_CashTransfer.py')
caselist.append('Cash_DR_FundExpenses.py')
caselist.append('Cash_DR_CorporateActions.py')
caselist.append('Cash_DR_FinancialAssetPurchase.py')
caselist.append('Cash_DR_NonFinancialAssetPurchase.py')
caselist.append('Cash_DR_DerivativesExercise.py')
caselist.append('Cash_DR_WithdrawalOfMemberBenefits.py')
caselist.append('Cash_DR_MemberAccountRollover.py')
caselist.append('Cash_DR_TransactionAdjustments.py')
#NoCash
caselist.append('NonCash_CorporateActions.py')
caselist.append('NonCash_InSpecieContributions.py')
caselist.append('NonCash_InSpecieMemberPayments.py')
caselist.append('NonCash_AccrualAmounts.py')
caselist.append('NonCash_AdjustmentsWriteoffs.py')

for n in range(1):
    m=0
    for a in caselist:
        print(a + ' is in compile ' + str(n+1) +' '+str(m+1)) 
        exec(open(os.getcwd()+'\\%s' %a).read())          
        #cmd = 'python '+(os.getcwd()+'\\%s' %a)
        #os.system(cmd)
        print(a + ' is finished ' + str(n+1) +' '+str(m+1))
        m = m+1
    n = n+1
