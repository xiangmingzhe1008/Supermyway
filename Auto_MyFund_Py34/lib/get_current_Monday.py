# -*- coding: UTF-8 -*-
'''
Created on 5Feb.,2018

@author: xiangmingzhe
'''
import datetime

oneday = datetime.timedelta(days=1)
twoday = datetime.timedelta(days=2) 
threeday = datetime.timedelta(days=3) 
fourday = datetime.timedelta(days=4) 
fiveday = datetime.timedelta(days=5) 
sixday = datetime.timedelta(days=6)  
current_date = datetime.date.today()
# print(current_date)
current_weekday = (current_date).weekday()
# print(current_weekday)
def get_current_monday():
    Date = []
    if current_weekday == 0: 
        From_Date = current_date.strftime('%d/%m/%y')
    elif current_weekday == 1:
        From_Date = (current_date - oneday).strftime('%d/%m/%y')
    elif current_weekday == 2:
        From_Date = (current_date - twoday).strftime('%d/%m/%y')
    elif current_weekday == 3:
        From_Date = (current_date - threeday).strftime('%d/%m/%y')
    elif current_weekday == 4:
        From_Date = (current_date - fourday).strftime('%d/%m/%y')
    elif current_weekday == 5:
        From_Date = (current_date - fiveday).strftime('%d/%m/%y')
    elif current_weekday == 6:
        From_Date = (current_date - sixday).strftime('%d/%m/%y')
#     print('From_Date = '+str(From_Date))
    Date.append(str(From_Date))
    Date.append(str(current_date.strftime('%d/%m/%y')))
    print(Date)
    return(Date)
if __name__ == '__main__':
    get_current_monday()
     
