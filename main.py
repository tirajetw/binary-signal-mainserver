import paho.mqtt.client as mqttClient
import time
import sys
import mechanicalsoup
import pubMqtt
import json
import operator

currency_pair = {
    'EURUSD',
    'USDJPY',
    'GBPUSD',
    'USDCHF',
    'EURJPY',
    'USDCAD',
    'AUDUSD'
}

browser = mechanicalsoup.StatefulBrowser(
    soup_config = {'features': 'lxml'},
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    )

def check_winrate(action):
    browser.open("https://binary-signal.com/en/chart/" + action)
    list_history = str(browser.get_current_page().find_all(class_="history")[0]).split('"')
    win_index = [i for i, n in enumerate(list_history) if n == "win"] # List comprehension
    list_history = str(browser.get_current_page().find_all(class_="history")[0]).split('"')
    loss_index = [i for i, n in enumerate(list_history) if n == "loss"] # List comprehension
    data = loss_index + win_index
    data = list(data)
    data.sort()
    result_data = []
    recommended_level = 0
    for x in data:
        try:
            if (   x == win_index[0] 
                or x == win_index[1] 
                or x == win_index[2] 
                or x == win_index[3] 
                or x == win_index[4] 
                or x == win_index[5] 
                or x == win_index[6] 
                or x == win_index[7]):
                result_data.append(1)
        except:
            if ( x == loss_index[0] 
                or x == loss_index[1] 
                or x == loss_index[2] 
                or x == loss_index[3] 
                or x == loss_index[4] 
                or x == loss_index[5] 
                or x == loss_index[6] 
                or x == loss_index[7]):
                result_data.append(0)
    #recommend part
    j = 7
    sum_weight = 0
    for i in result_data:
        sum_weight = i * j + sum_weight
        j = j-1
    recommended_level = sum_weight/0.28
    recommended_level = int(recommended_level)

    return result_data,recommended_level

def time_check():
    spinner = spinning_cursor()
    for _ in range(5):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')
    timeis = time.localtime()
    #print(timeis)
    cal = [0,15,30,45] # rev2 : change refresh time
    time.sleep(1)
    for x in range(4):
        if(int(timeis.tm_min) == cal[x]):
            print("check winrate.")
            return True
    return False

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += str(ele)   
    
    # return string   
    return str1  


## RUNNING PART ##
if(__name__=='__main__'):
    status = []
    last_status = []
    print('Running bot.')
    try:
        while True:
            if time_check():
                for action in currency_pair:
                    data,level = check_winrate(action)
                    print(action, data, level)
                    if level >= 2:
                        status.append(tuple((action,level)))
                    # else:
                    #     status.append(0)

                if status != last_status:
                    last_status = status
                    timeis = time.localtime()
                    status.sort(key = operator.itemgetter(1), reverse = True)
                    statusJson = json.dumps(status)
                    print(statusJson)
                    print('have updated.')
                    pubMqtt.pubMQTT(statusJson)
                    status.clear()
                    time.sleep(60)
                elif status == last_status:
                    print('No update.')
                    time.sleep(10)

    except:
        print("error")
