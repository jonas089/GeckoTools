import requests
import json
import time
import pickle
from os import system, name
import os

list = 'https://api.coingecko.com/api/v3/coins/list'
tickers = 'https://api.coingecko.com/api/v3/coins/'

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

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
    for e in range(0, len(ids) - 1):
        et = cut(str(time.time() - st))
        print('[Searching for coins that were listed on Coingecko less than ' + str(yt) + ' days ago]')

        print('Runtime(s): ' + et)
        if e > 0:
            toi = float(et) / e
            tl = toi * (len(ids) - 1 - e)
            print('Est. Time left: ' + cut(str(tl)) + 's' + ' (= ' + cutx(str(tl/60/60), 3) + 'h' + ')')

        print('[' + str(e + 1) + '/' + str(len(ids) - 1) + ']')
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
                        print('Warning: ' + str(E))
                        print('[This is due to too many requests, this Warning is resolved automatically.]')
                        time.sleep(10)
            else:
                print('Error: ' + str(E))
                time.sleep(10)
        clear()
    os.remove('OLD_' + str(days) + '.dat')
    open('OLD_' + str(days) + '.dat', 'x')
    with open('OLD_' + str(days) + '.dat', 'wb') as database:
            pickle.dump(old_coins, database)
    return coins

def unkown_vol_out(data):
    coins = []
    Etimeout = 'Expecting value: line 1 column 1 (char 0)'
    uke = 0
    st = time.time()
    for i in range(0, len(data) - 1):
        et = cut(str(time.time() - st))
        print('[Removing coins with an unknown 24 hour volume]')
        print('Runtime(s): ' + et)
        print('[' + str(i + 1) + '/' + str(len(data) - 1) + ']')
        c = data[i]
        uvo = 'https://api.coingecko.com/api/v3/simple/price?ids=' + c + '&vs_currencies=usd&include_24hr_vol=true'
        try:
            r = requests.get(uvo)
            res = json.loads(r.text)
            try:
                d = float(res[c]['usd_24h_vol'])
                if res[c]['usd_24h_vol'] != '?':
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
                        if res[c]['usd_24h_vol'] != '?':
                            coins.append(len(coins))
                            coins[len(coins) - 1] = c
                    except Exception as NOFLOAT:
                        uke += 1
                        pass
                    clear()
                    break
                except Exception as E2:
                    if str(E2) == Etimeout:
                        print('[Warning: Known timeout Error, will be fixed automatically]')
                        time.sleep(10)
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
    r = requests.get(tickers + coin + '?localization=false&tickers=true&market_data=true')
    res = json.loads(r.text)
    if exchange in str(res['tickers']):
        return True
    else:
        return False

def ExchangeFilterV2(coins, exchange):
    result = []
    for i in range(0, len(coins) - 1):
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
            data = pickle.loads(database)
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
    for c in range(0, len(coins) - 1):
        i = coins[c]
        url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=' + i + '&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=24h'
        r = requests.get(url)
        res = json.loads(r.text)
        volume = float(res['total_volume'])
        if volume >= bottom and volume <= top:
            result.append(len(result))
            result[len(result) - 1] = i
    return result

ResetAndCheckAll(90, '09.03.2021')