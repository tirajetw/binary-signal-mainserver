import os
from datetime import datetime

def signal_update(currency,signal):
    now             = datetime.now()
    current_time    = now.strftime("%Y%m%d,%H:%M:%S")
    payload         = 'python3 ./google/append2gsheet.py --data ' + current_time + ',' + signal + ' --sheetid 1uxG4YKI2v5tb-ZJkWvX58t8FdHmx93xAmhEnXeB9SRA --range "' + currency + '" --noauth_local_webserver'
    os.system(payload)

def result_update(currency,signal,result,cost,balance):
    now             = datetime.now()
    current_time    = now.strftime("%Y%m%d,%H:%M:%S")
    payload         = 'python3 ./google/append2gsheet.py --data ' + current_time + ',' + currency + ',' + signal + ',' + result + ',' + str(cost) + ',' + str(balance) + ' --sheetid 1uxG4YKI2v5tb-ZJkWvX58t8FdHmx93xAmhEnXeB9SRA --range "' + 'history' + '" --noauth_local_webserver'
    os.system(payload)
    
def balance_update(balance):
    now             = datetime.now()
    current_time    = now.strftime("%Y%m%d,%H:%M:%S")
    payload         = 'python3 ./google/append2gsheet.py --data ' + current_time + ',' + str(balance) + ' --sheetid 1uxG4YKI2v5tb-ZJkWvX58t8FdHmx93xAmhEnXeB9SRA --range "' + 'balance' + '" --noauth_local_webserver'
    os.system(payload)

balance_update(1000)
# result_update('TEST','call','win',1000,10000)
# signal_update('TEST','call')

