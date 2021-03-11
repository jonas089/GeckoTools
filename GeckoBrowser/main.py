import requests
import json
import time
import pickle
from os import system, name
import os
from tqdm import tqdm, trange

list = 'https://api.coingecko.com/api/v3/coins/list'
tickers = 'https://api.coingecko.com/api/v3/coins/'

def clear():
    #if name == 'nt':
    #    _ = system('cls')
    #else:
    #    _ = system('clear')
    pass
def cutx(string, x):
    res = ''
    loc = 1000000
    for l in range(0, len(string) - 1):
        if string[l] != '.' and string[l] != ',' and l != loc + x:
            res += string[l]
        elif l == loc + x:
            return res
        else:
            res += string[l]
            loc = l
    return res

def cut(string):
    res = ''
    loc = 1000000
    for l in range(0, len(string) - 1):
        if string[l] != '.' and string[l] != ',' and l != loc + 1:
            res += string[l]
        elif l == loc + 1:
            return res
        else:
            loc = l
    return res

def get_ids():
    r = requests.get(list)
    res = json.loads(r.text)
    valid = []
    for e in range(0, len(res) - 1):
        if '0-5x' not in res[e]['id'] and 'long' not in res[e]['id'] and 'short' not in res[e]['id']:
            valid.append(len(valid))
            valid[len(valid) - 1] = res[e]['id']
    return valid

def FilterByAge(yt, ids):
    days = yt
    old_coins = []
    try:
        open('OLD_' + str(days) + '.dat', 'x')
    except Exception as exists:
        pass
    try:
        with open('OLD_' + str(days) + '.dat', 'rb') as backup:
            old_coins = pickle.loads(backup)
    except Exception as empty:
        pass

    idov = []
    for i in range(0, len(ids) - 1):
        if ids[i] not in old_coins:
            idov.append(len(idov))
            idov[len(idov) - 1] = ids[i]

    ids = idov
    Etimeout = 'Expecting value: line 1 column 1 (char 0)'
    st = time.time()
    coins = []
    print('[Searching for coins that were listed on Coingecko less than ' + str(yt) + ' days ago]')
    with tqdm(total=len(ids)) as pbar:
        for e in range(0, len(ids)):
            pbar.update(1)
            et = cut(str(time.time() - st))
            if e > 0:
                toi = float(et) / e
                tl = toi * (len(ids) - 1 - e)
            i = ids[e]
            try:
                r = requests.get(tickers + i + '/market_chart?vs_currency=usd&days=' + str(yt) + '&interval=daily')
                res = json.loads(r.text)
                if len(res['prices']) < yt:
                    coins.append(len(coins))
                    coins[len(coins) - 1] = i
                else:
                    old_coins.append(len(old_coins))
                    old_coins[len(old_coins) - 1] = i
            except Exception as E:
                if str(E) == Etimeout:
                    while True:
                        try:
                            r = requests.get(tickers + i + '/market_chart?vs_currency=usd&days=' + str(yt) + '&interval=daily')
                            res = json.loads(r.text)
                            if len(res['prices']) < yt:
                                coins.append(len(coins))
                                coins[len(coins) - 1] = i
                            else:
                                old_coins.append(len(old_coins))
                                old_coins[len(old_coins) - 1] = i
                            break
                        except Exception as E:
                            time.sleep(10)
                else:
                    time.sleep(10)
        clear()
    os.remove('OLD_' + str(days) + '.dat')
    open('OLD_' + str(days) + '.dat', 'x')
    with open('OLD_' + str(days) + '.dat', 'wb') as database:
            pickle.dump(old_coins, database)
    return coins

def XgapFix(Range, acceptance, data):
    coins = FilterByAge(Range, data)
    print('[Applying XgapFix to list of ' + str(len(data)) + ' coins]')
    with tqdm(total=len(coins)) as pbar:
        for i in range(0, len(data)):
            pbar.update(1)
            while True:
                try:
                    r = requests.get(tickers + data[i] + '/market_chart?vs_currency=usd&days=' + str(Range) + '&interval=daily')
                    res = json.loads(r.text)
                    if len(res['prices']) < acceptance:
                        coins.append(len(coins))
                        coins[len(coins) - 1] = data[i]
                    else:
                        old_coins.append(len(old_coins))
                        old_coins[len(old_coins) - 1] = data[i]
                        break
                except Exception as E:
                    time.sleep(10)
    os.remove('OLD_' + str(days) + '.dat')
    open('OLD_' + str(days) + '.dat', 'x')
    with open('OLD_' + str(days) + '.dat', 'wb') as database:
            pickle.dump(old_coins, database)

    return coins

def unkown_vol_out(data):
    coins = []
    Etimeout = 'Expecting value: line 1 column 1 (char 0)'
    Enovolume = 'Expecting value: line 1 column 1 (char 0)'
    uke = 0
    st = time.time()
    print('[Applying Unkown-Volume-Filter to list of ' + str(len(data)) + ' coins]')
    with tqdm(total=len(data)) as pbar:
        for i in range(0, len(data)):
            pbar.update(1)
            et = cut(str(time.time() - st))
            #print('[' + str(i + 1) + '/' + str(len(data)) + ']')
            c = data[i]
            uvo = 'https://api.coingecko.com/api/v3/simple/price?ids=' + c + '&vs_currencies=usd&include_24hr_vol=true'
            try:
                r = requests.get(uvo)
                res = json.loads(r.text)
                try:
                    d = float(res[c]['usd_24h_vol'])
                    if d > 1:
                        coins.append(len(coins))
                        coins[len(coins) - 1] = c

                except Exception as NOFLOAT:
                    uke += 1
                    pass
                clear()
            except Exception as E:
                while True:
                    try:
                        uvo = 'https://api.coingecko.com/api/v3/simple/price?ids=' + c + '&vs_currencies=usd&include_24hr_vol=true'
                        r = requests.get(uvo)
                        res = json.loads(r.text)
                        try:
                            d = float(res[c]['usd_24h_vol'])
                            if d > 1:
                                coins.append(len(coins))
                                coins[len(coins) - 1] = c
                        except Exception as NOFLOAT:
                            uke += 1
                            pass
                        clear()
                        break
                    except Exception as E2:
                        if str(E2) == Etimeout:
                            time.sleep(10)
                        elif Enovolume in str(E2):
                            uke += 1
                            clear()
                            break
                        else:
                            uke += 1
                            time.sleep(10)
                            clear()
                            break
    print('Unkown Errors [ignored]: ' + str(uke))
    time.sleep(10)
    return coins

def ExchangeFilterV1(coin, exchange):
    # exchange = 'binance'
    try:
        r = requests.get(tickers + coin + '?localization=false&tickers=true&market_data=true')
        res = json.loads(r.text)
        if exchange in str(res['tickers']):
            return True
        else:
            return False
    except Exception as E:
        return False

def ExchangeFilterV2(coins, exchange):
    result = []
    print('[Applying Exchange-Filter to list of ' + str(len(coins)) + ' coins]')
    with tqdm(total=len(coins)) as pbar:
        for i in range(0, len(coins)):
            pbar.update(1)
            #print('[' + str(i) + '/' + str(len(coins) - 1) + ']')
            c = coins[i]
            if ExchangeFilterV1(c, exchange) == True:
                result.append(len(result))
                result[len(result) - 1] = c
    return result

def NewOnGecko(days):
    return unkown_vol_out(FilterByAge(days, get_ids()))

def ReturnFileData(days, date):
    data = []
    try:
        with open('db_d' + str(days) + '_' + date + '.dat', 'rb') as database:
            data = pickle.load(database)
    except Exception as empty:
        pass
    return data

def ResetAndCheckAll(days, date):
    data = NewOnGecko(days)
    try:
        open('db_d' + str(days) + '_' + date + '.dat', 'x')
    except Exception as exists:
        pass
    try:
        os.remove('db_d' + str(days) + '_' + date + '.dat')
    except Exception as nan:
        pass
    with open('db_d' + str(days) + '_' + date + '.dat', 'wb') as database:
        pickle.dump(data, database)

def FilterByVolumeRange(bottom, top, coins):
    result = []
    print('[Applying Volume-Filter to list of ' + str(len(coins)) + ' coins]')
    with tqdm(total=len(coins)) as pbar:
        for c in range(0, len(coins)):
            pbar.update(1)
            i = coins[c]
            url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=' + i + '&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=24h'
            r = requests.get(url)
            res = json.loads(r.text)
            volume = float(res['total_volume'])
            if volume >= bottom and volume <= top:
                result.append(len(result))
                result[len(result) - 1] = i
    return result

def OnExchangeMinVol(data, exchange, minvol, maxvol):
    return(FilterByVolumeRange(minvol, maxvol, ExchangeFilterV2(data, exchange)))


#ResetAndCheckAll(30, '10.03.2021')
coins = ReturnFileData(90, '09.03.2021')
print(OnExchangeMinVol(XgapFix(180, 90 , coins), 'binance', 1*10^6, 1*10^11))
# note to myself: feature "hypedate", showing all coins, which social media attention did a y-x over the course of z - time
