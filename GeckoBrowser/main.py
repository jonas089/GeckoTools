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
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
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
    coins = []
    print('[Searching for coins that were listed on Coingecko less than ' + str(yt) + ' days ago]')
    with tqdm(total=len(ids)) as pbar:
        for e in range(0, len(ids)):
            pbar.update(1)
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
                        except Exception as E2:
                            if Etimeout == str(E2):
                                time.sleep(10)
                            else:
                                print(str(E2))
                                time.sleep(1)
                                break
                else:
                    pass
    try:
        os.remove('OLD_' + str(days) + '.dat')
    except Exception as Nofile:
        pass
    open('OLD_' + str(days) + '.dat', 'x')
    with open('OLD_' + str(days) + '.dat', 'wb') as database:
            pickle.dump(old_coins, database)
    return coins

def XgapFix(Range, acceptance, data):
    #coins = FilterByAge(Range, data)
    Etimeout = 'Expecting value: line 1 column 1 (char 0)'
    coins = []
    old_coins = []
    print('[Applying XgapFix to list of ' + str(len(data)) + ' coins]')
    with tqdm(total=len(data)) as pbar:
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
                    if str(E) == Etimeout:
                        time.sleep(10)
                    else:
                        break
    try:
        os.remove('OLD_' + str(Range) + '.dat')
    except Exception as Nofile:
        pass
    open('OLD_' + str(Range) + '.dat', 'x')
    with open('OLD_' + str(Range) + '.dat', 'wb') as database:
            pickle.dump(old_coins, database)
    print(coins)
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

                        break
                    except Exception as E2:
                        if str(E2) == Etimeout:
                            time.sleep(10)
                        elif Enovolume in str(E2):
                            uke += 1

                            break
                        else:
                            uke += 1
                            time.sleep(10)

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

def FilterInactive(coins, reddit_post_min, reddit_comment_min, alexa_rank_min, pull_requests_merged_min):
    result = []
    Etimeout = 'Expecting value: line 1 column 1 (char 0)'
    print('[Applying Activity-Filter to list of ' + str(len(coins)) + ' coins]')
    with tqdm(total=len(coins)) as pbar:
        for e in range(0, len(coins)):
            pbar.update(1)
            while True:
                try:
                    c = coins[e]
                    url = 'https://api.coingecko.com/api/v3/coins/' + c + '/history?date=12-03-2021&localization=false'
                    r = requests.get(url)
                    res = json.loads(r.text)
                    reddit_average_posts_48h = 0
                    reddit_average_comments_48h = 0
                    alexa_rank = 0
                    pull_requests_merged = 0
                    try:
                        reddit_average_posts_48h = float(res['community_data']['reddit_average_posts_48h'])
                    except Exception as E:
                        pass
                    try:
                        reddit_average_comments_48h = float(res['community_data']['reddit_average_comments_48h'])
                    except Exception as E:
                        pass
                    try:
                        alexa_rank = float(res['public_interest_stats']['alexa_rank'])
                    except Exception as E:
                        pass
                    try:
                        pull_requests_merged = float(res['developer_data']['pull_requests_merged'])
                    except Exception as E:
                        pass

                    if (reddit_average_posts_48h >= reddit_post_minand and reddit_average_comments_48h >= reddit_comment_min and alexa_rank >= alexa_rank_minand and pull_requests_merged >= pull_requests_merged_min):
                        result.append(len(result))
                        result[len(result) - 1] = c
                    else:
                        pass
                    break
                except Exception as E:
                    if str(E) == Etimeout:
                        time.sleep(10)
                    else:
                        break
    return result
def FilterByVolumeRange(bottom, top, coins):
    result = []
    Etimeout = 'Expecting value: line 1 column 1 (char 0)'
    print('[Applying Volume-Filter to list of ' + str(len(coins)) + ' coins]')
    with tqdm(total=len(coins)) as pbar:
        for c in range(0, len(coins)):
            pbar.update(1)
            i = coins[c]
            while True:
                url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=' + i + '&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=24h'
                r = requests.get(url)
                try:
                    res = json.loads(r.text)[0]
                    volume = float(res['total_volume'])
                    if volume >= bottom and volume <= top:
                        result.append(len(result))
                        result[len(result) - 1] = i
                    break
                except Exception as E:
                    if str(E) == Etimeout:
                        time.sleep(10)
                    else:
                        break
    return result

def OnExchangeMinVol(data, exchange, minvol, maxvol):
    return(FilterByVolumeRange(minvol, maxvol, ExchangeFilterV2(data, exchange)))

clear()

def UpdateBinance(date):
    ResetAndCheckAll(90, date)
    coins = ReturnFileData(90, date)
    return OnExchangeMinVol(XgapFix(180, 90 , coins), 'binance', 1000000, 1000000000000)
def Gecko(date):
    ResetAndCheckAll(30, date)
    coins = ReturnFileData(30, date)
    return XgapFix(180, 30, coins)

unfiltered = ReturnFileData(30, '11.03.2021')
print(FilterInactive(unfiltered, 0, 50, 50, 1))
#print(ReturnFileData(30, '11.03.2021'))
#coins, reddit_post_min, reddit_comment_min, alexa_rank_min, pull_requests_merged_min
#ResetAndCheckAll(30, '10.03.2021')
# note to myself: feature "hypedate", showing all coins, which social media attention did a y-x over the course of z - time
