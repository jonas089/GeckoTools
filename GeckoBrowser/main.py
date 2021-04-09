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
            old_coins = pickle.load(backup)
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

                    if (reddit_average_posts_48h >= reddit_post_min and reddit_average_comments_48h >= reddit_comment_min and alexa_rank >= alexa_rank_min and pull_requests_merged >= pull_requests_merged_min):
                        result.append(len(result))
                        result[len(result) - 1] = c
                    else:
                        pass
                    break
                except Exception as E:
                    if str(E) == Etimeout:
                        time.sleep(10)
                    elif 'Max retries exceeded with url:' in str(E):
                        print('Connection Error... Waiting... ')
                        time.sleep(10)
                    else:
                        break
    return result

def RedditCommentChange(coins, d1, m1, y1, d2, m2, y2, up_by):
    Etimeout = 'Expecting value: line 1 column 1 (char 0)'
    result = []
    print('[Applying RedditCommentChange-Filter to list of ' + str(len(coins)) + ' coins]')
    with tqdm(total=len(coins)) as pbar:
        for e in range(0, len(coins)):
            pbar.update(1)
            while True:
                try:
                    c = coins[e]
                    url1 = 'https://api.coingecko.com/api/v3/coins/' + c + '/history?date=' + str(d1) + '-' + str(m1) + '-' + str(y1) + '&localization=false'
                    url2 = 'https://api.coingecko.com/api/v3/coins/' + c + '/history?date=' + str(d2) + '-' + str(m2) + '-' + str(y2) + '&localization=false'
                    r1 = requests.get(url1)
                    res1 = json.loads(r1.text)
                    r2 = requests.get(url2)
                    res2 = json.loads(r2.text)
                    reddit_average_comments_48h_t1 = 0
                    reddit_average_comments_48h_t2 = 0
                    factor = 0
                    try:
                        reddit_average_comments_48h_t1 = float(res1['community_data']['reddit_average_comments_48h'])
                        reddit_average_comments_48h_t2 = float(res2['community_data']['reddit_average_comments_48h'])
                        factor = reddit_average_comments_48h_t2 / reddit_average_comments_48h_t1
                        if factor != 0 and factor >= up_by:
                            result.append(len(result))
                            result[len(result) - 1] = c
                        break
                    except Exception as E:
                        break
                        #pass
                except Exception as NE:
                    if str(NE) == Etimeout:
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



def CoinAlytics(coin, dates):
    result = {}
    Etimeout = 'Expecting value: line 1 column 1 (char 0)'
    result['reddit_average_posts_48h'] = []
    result['reddit_average_comments_48h'] = []
    result['alexa_rank'] = []
    result['pull_requests_merged'] = []
    with tqdm(total=len(dates)) as pbar:
        for e in range(0, len(dates)):
            pbar.update(1)
            while True:
                try:
                    c = coin
                    date = dates[e]
                    url = 'https://api.coingecko.com/api/v3/coins/' + c + '/history?date=' + date + '&localization=false'
                    r = requests.get(url)
                    res = json.loads(r.text)
                    reddit_average_posts_48h = 0
                    reddit_average_comments_48h = 0
                    alexa_rank = 0
                    pull_requests_merged = 0
                    try:
                        reddit_average_posts_48h = float(res['community_data']['reddit_average_posts_48h'])
                        result['reddit_average_posts_48h'].append(len(result['reddit_average_posts_48h']))
                        result['reddit_average_posts_48h'][len(result['reddit_average_posts_48h']) - 1] = reddit_average_posts_48h
                    except Exception as E:
                        print(str(E))
                        time.sleep(10)
                        pass
                    try:
                        reddit_average_comments_48h = float(res['community_data']['reddit_average_comments_48h'])
                        result['reddit_average_comments_48h'].append(len(result['reddit_average_comments_48h']))
                        result['reddit_average_comments_48h'][len(result['reddit_average_comments_48h']) - 1] = reddit_average_comments_48h
                    except Exception as E:
                        pass
                    try:
                        alexa_rank = float(res['public_interest_stats']['alexa_rank'])
                        result['alexa_rank'].append(len(result['alexa_rank']))
                        result['alexa_rank'][len(result['alexa_rank']) - 1] = alexa_rank
                    except Exception as E:
                        pass
                    try:
                        pull_requests_merged = float(res['developer_data']['pull_requests_merged'])
                        result['pull_requests_merged'].append(len(result['pull_requests_merged']))
                        result['pull_requests_merged'][len(result['pull_requests_merged']) - 1] = alexa_rank
                    except Exception as E:
                        pass
                    break
                except Exception as E:
                    if str(E) == Etimeout:
                        time.sleep(10)
                    elif 'Max retries exceeded with url:' in str(E):
                        print('Connection Error... Waiting... ')
                        time.sleep(10)
                    else:
                        break
    return result

clear()

def UpdateBinance(date):
    ResetAndCheckAll(90, date)
    coins = ReturnFileData(90, date)
    return OnExchangeMinVol(XgapFix(180, 90 , coins), 'binance', 1000000, 1000000000000)
def Gecko(date):
    ResetAndCheckAll(30, date)
    coins = ReturnFileData(30, date)
    return XgapFix(180, 30, coins)

'''
unfiltered = ReturnFileData(90, '09.03.2021')
filtered = FilterInactive(unfiltered, 0, 0, 1, 0)
print(filtered)
print('-'*15)
print('Coins with a Social media attention delta of 50%+ (past 7 days)')
print(RedditCommentChange(filtered, '05', '03', '2021', '12', '03', '2021', 1.5))
'''

#print(ReturnFileData(30, '11.03.2021'))
#RedditCommentChange(coins, d1, m1, y1, d2, m2, y2, up_by):
#FilterInactive(coins, reddit_post_min, reddit_comment_min, alexa_rank_min, pull_requests_merged_min)
#ResetAndCheckAll(30, '10.03.2021')
# note to myself: feature "hypedate", showing all coins, which social media attention did a y-x over the course of z - time
#print(ResetAndCheckAll(90, '22.03.2021'))

with open('db_d90_07.04.2021.dat', 'rb') as dat90:
    data1 = pickle.load(dat90)

#data1 = ResetAndCheckAll(90, '08.04.2021')
try:
    data1 = XgapFix(180, 90, data1)
except Exception as E:
    pass

data2 = ExchangeFilterV2(data1, 'binance')
data3 = RedditCommentChange(data1, '07', '04', '2021', '08', '04', '2021', 1.25)
data4 = RedditCommentChange(data2, '07', '04', '2021', '08', '04', '2021', 1.25)

wresultdata = str(data1) + '\n' + '\n' + '-'*10 + '\n' + str(data2) + '\n' + '\n' + '-'*10 + '\n' + str(data3) + '\n' + '\n' + '-'*10 + '\n' + str(data4) + '\n' + '\n' + '-'*10

try:
    open('result.txt', 'x')
except Exception as E:
    pass

with open('result.txt', 'w') as resultfile:
    resultfile.write(wresultdata)

#dates = ['01-03-2021']
#print(CoinAlytics('cartesi', dates))


#TTPSConnectionPool(host='api.coingecko.com', port=443): Max retries exceeded with url: /api/v3/coins/100-waves-eth-usd-yield-set/history?date=12-03-2021&localization=false (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x0000019071572AC0>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))
