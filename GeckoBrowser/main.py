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

data = ['1inch', '2give', '2x2', '3xt', '42-coin', '4new', '5g-cash', '7finance', 'abcc-token', 'absorber', 'abulaba', 'ac-milan-fan-token', 'adelphoi', 'advertisingcoin', 'aeryus', 'aevo', 'aga-rewards', 'agetron', 'agoras', 'aiascoin', 'ai-mining', 'akita-inu', 'alchemix', 'algovest', 'alis', 'all-for-one-business', 'alliance-fan-token', 'alligator-fractal-set', 'almace-shards', 'aloha', 'alpha5', 'altcommunity-coin', 'altmarkets-coin', 'amazonacoin', 'amepay', 'amino-network', 'amz-coin', 'andes-coin', 'anime-token', 'ankreth', 'anon', 'anoncoin', 'anrkey-x', 'antimatter', 'antique-zombie-shards', 'anysale', 'apecoin', 'apholding-coin', 'apiary-fund-coin', 'apple-finance', 'aquariuscoin', 'araw-token', 'arbiswap', 'arbitragect', 'arcona', 'arcticcoin', 'argenpeso', 'arianee', 'aries-financial-token', 'arix', 'armor', 'armor-nxm', 'armx-unidos', 'artbyte', 'arth', 'asgard-finance', 'asia-reserve-currency-coin', 'asimi', 'assy-index', 'astosch', 'astro', 'auction', 'auric-network', 'aurumcoin', 'auruscoin', 'auto', 'axentro', 'axioms', 'b21', 'backpacker-coin', 'baconcoin', 'baconswap', 'baepay', 'bafi-finance-token', 'ballotbox', 'ballswap', 'bamboo-defi', 'banana-finance', 'bancor-governance-token', 'bankex', 'bankroll-vault', 'bao-finance', 'baooka-token', 'baroin', 'basis-coin-cash', 'basiscoin-share', 'basis-dollar', 'basis-dollar-share', 'basis-gold-mdex', 'basis-gold-share', 'basis-gold-share-heco', 'bbscoin', 'bdollar', 'bdollar-share', 'beast-dao', 'beefy-finance', 'beetr', 'be-gaming-coin', 'beholder', 'belugaswap', 'berry-data', 'bet-chips', 'bifi', 'bifrost', 'bigboys-industry', 'big-coin', 'bignite', 'billionhappiness', 'binance-agile-set-dollar', 'binance-eth', 'binarium', 'binjit-coin', 'bintex-futures', 'biokkoin', 'birdchain', 'birthday-cake', 'bitball-treasure', 'bitberry-token', 'bitbot-protocol', 'bitcicoin', 'bitclave', 'bitcoen', 'bitcoffeen', 'bitcoinbrand', 'bitcoin-candy', 'bitcoin-final', 'bitcoin-flash-cash', 'bitcoinhedge', 'bitcoinmono', 'bitcoin-scrypt', 'bitcoin-unicorn', 'bitcoinv', 'bitcoiva', 'bitcomo', 'bitcorn', 'bitcratic', 'bitcratic-revenue', 'bitcurate', 'bitdns', 'bitfarmings', 'bitget-defi-token', 'bitgrin', 'bithercash', 'bitjob', 'bitmoney', 'bitnautic', 'bitonyx-token', 'bitpakcointoken', 'bitpower', 'bitrent', 'bitrewards', 'bitshark', 'bitsong', 'bitstar', 'bitsum', 'bittoken', 'blackdragon-token', 'blackfisk', 'blipcoin', 'bliss-2', 'blitzpredict', 'block-array', 'block-chain-com', 'blockchain-cuties-universe', 'block-collider', 'block-duelers', 'blockgrain', 'blockport', 'blockstamp', 'blocktix', 'bloc-money', 'blurt', 'bnb48-club-token', 'bnoincoin', 'boliecoin', 'bolt-true-share', 'bonfida', 'bonpay', 'boolberry', 'boostcoin', 'boringdao-btc', 'bot-ocean', 'bountymarketcap', 'bowl-a-coin', 'br34p', 'brickblock', 'bridge-finance', 'bridge-mutual', 'bscex', 'bsc-farm', 'bscpad', 'btc-eth-75-25-weight-set', 'btc-lite', 'btc-on-chain-beta-portfolio-set', 'btc-standard-hashrate-token', 'btf', 'bt-finance', 'bubble-network', 'bulleon', 'bulls', 'bunnytoken', 'burn-yield-burn', 'business-credit-substitute', 'butterfly-protocol-2', 'buy-coin-pos', 'buy-sell', 'buyucoin-token', 'buzzcoin', 'buzzshow', 'bytus', 'bzedge', 'cactus-finance', 'cafeswap-token', 'caixa-pay', 'cajutel', 'candela-coin', 'candy-box', 'candy-protocol', 'capital-finance', 'capricoin', 'carat', 'carboneum', 'carebit', 'cashbackpro', 'cash-global-coin', 'centex', 'cexlt', 'cezo', 'chai', 'chaincoin', 'chainlink-trading-set', 'chalice-finance', 'change', 'charg-coin', 'cheeseswap', 'chess-coin', 'chronocoin', 'cipher-core-token', 'circleswap', 'cirquity', 'citadel', 'civitas-protocol', 'clash-token', 'clover', 'cmdx', 'cmitcoin', 'cobak-token', 'cocaine-cowboy-shards', 'cocktailbar', 'codeo-token', 'cofinex', 'coinall-token', 'coindom', 'coinjanitor', 'coinlancer', 'coinstarter', 'coinxclub', 'collegicoin', 'color', 'commons-earth', 'community-generation', 'community-token', 'compound-sai', 'comsa', 'connect-financial', 'cord-defi-eth', 'cover-protocol', 'covir', 'cprop', 'crave', 'cream-eth2', 'cross-finance', 'crowdwiz', 'crowns', 'crow-token', 'crudeoil-finance', 'crycash', 'crypto-accept', 'crypto-application-token', 'crypto-bank', 'cryptobet', 'crypto-candy', 'cryptocurrency-business-token', 'cryptocurrency-top-10-tokens-index', 'cryptoenergy', 'cryptoflow', 'cryptohashtank-coin', 'crypto-heroes-token', 'cryptokek', 'cryptonits', 'cryptoping', 'cryptorewards', 'cryptotipsfr', 'csc-jackpot', 'csp-dao-network', 'cts-coin', 'cudos', 'curio-governance', 'curryswap', 'custody-token', 'cvp-token', 'cyber-movie-chain', 'cyclone-protocol', 'daiquilibrium', 'danat-coin', 'dandy', 'dao-maker', 'daoventures', 'dappcents', 'dash-green', 'data-saver-coin', 'dds-store', 'debitum-network', 'decentbet', 'decentralized-mining-exchange', 'decenturion', 'deepcloud-ai', 'defi-100', 'defiato', 'defi-nation-signals-dao', 'defi-omega', 'defisocial', 'defi-top-5-tokens-index', 'defi-wizard', 'defi-yield-protocol', 'defla', 'deflect', 'degenerate-platform', 'dejave', 'delion', 'delphi-chain-link', 'dequant', 'deri-protocol', 'derivadao', 'desire', 'destiny-success', 'deus-synthetic-coinbase-iou', 'deva-token', 'dexfin', 'dexmex', 'dextrust', 'dfe-finance', 'dfinance', 'dfx-finance', 'diagon', 'die', 'digex', 'digg', 'digicol-token', 'digidinar-stabletoken', 'digimoney', 'digipharm', 'digital-antares-dollar', 'digitalprice', 'dipper', 'dipper-network', 'distributed-energy-coin', 'ditto', 'dixt-finance', 'dlike', 'dlp-duck-token', 'dnotes', 'doch-coin', 'dogefi', 'dogeyield', 'dopecoin', 'double-ace', 'dragonereum-gold', 'dragonvein', 'drc-mobility', 'dripper-finance', 'dust-token', 'dxiot', 'dymmax', 'dynamic-supply-tracker', 'e1337', 'eaglex', 'earth-token', 'easymine', 'ecc', 'e-chat', 'ecobit', 'ecoreal-estate', 'elastic-bitcoin', 'electra-protocol', 'electric-cash', 'electronic-energy-coin', 'elevate', 'elevation-token', 'elis', 'elite-swap', 'eltcoin', 'emerald-coin', 'e-money', 'employment-coin', 'energy-ledger', 'eox', 'eristica', 'escoin-token', 'espers', 'esports', 'essek-tov', 'eterbase', 'eth-12-day-ema-crossover-set', 'eth_20_day_ma_crossover_set', 'eth-20-ma-crossover-yield-set-ii', 'eth-26-day-ema-crossover-set', 'eth2-staking-by-poolx', 'eth-50-day-ma-crossover-set', 'eth-btc-rsi-ratio-trading-set', 'etheremontoken', 'ethereum-erush', 'ethereum-gold', 'ethereum-stake', 'etherinc', 'ether-kingdoms-token', 'ethichub', 'eth-limited', 'eth-momentum-trigger-set', 'eth-price-action-candlestick-set', 'eth-trending-alpha-st-set-ii', 'etoro-euro', 'etoro-new-zealand-dollar', 'etoro-pound-sterling', 'everid', 'evil-coin', 'evolution-finance', 'excavo-finance', 'exeedme', 'exgold', 'exnce', 'exor', 'exrt-network', 'extend-finance', 'eyes-protocol', 'ezystayz', 'faircoin', 'fairum', 'falopa', 'farming-bad', 'farmland-protocol', 'fastswap', 'feg-token', 'felix', 'feyorra', 'filda', 'financex-exchange', 'financex-exchange-token', 'finiko', 'finxflo', 'firdaos', 'fireball', 'fire-protocol', 'fiscus-fyi', 'five-balance', 'flapp', 'flash-stake', 'flashx-ultra', 'flixxo', 'float-protocol', 'flow', 'font', 'frax', 'frax-share', 'freeliquid', 'freicoin', 'freq-set-dollar', 'fromm-car', 'funjo', 'furucombo', 'fxpay', 'fyeth-finance', 'fyznft', 'g999', 'gadoshi', 'gains-v2', 'galilel', 'gamebetcoin', 'gamecash', 'gamestop-finance', 'game-x-coin', 'gapp-network', 'gard-governance-token', 'gas-cash-back', 'gasgains', 'gasify', 'general-attention-currency', 'generation-of-yield', 'genix', 'gera-coin', 'gg-token', 'glitch-protocol', 'global-digital-content', 'global-smart-asset', 'global-trust-coin', 'goaltime-n', 'goatcoin', 'gogo-finance', 'gokumarket-credit', 'gold', 'gold-cash', 'goldcoin', 'golden-bridge-coin', 'golden-goose', 'golden-ratio-token', 'goldenugget', 'golder-coin', 'goldfund-ico', 'goose-finance', 'gorillayield', 'gourmetgalaxy', 'governance-zil', 'govi', 'grace-period-token', 'grap-finance', 'gravity', 'green-light', 'grimm', 'groovy-finance', 'grpl-finance-2', 'guider', 'gulf-coin-gold', 'gusd-token', 'happy-birthday-coin', 'happycoin', 'hardcore-finance', 'hash-bridge-oracle', 'hashbx', 'hauteclere-shards-2', 'havy-2', 'heavens-gate', 'hecofi', 'helex-token', 'helix', 'helmet-insure', 'helper-search-token', 'hero-token', 'hex-money', 'hland-token', 'hodlcoin', 'hodltree', 'holdtowin', 'hollygold', 'holyheld-2', 'holy-trinity', 'homihelp', 'hom-token', 'honestcoin', 'honk-honk', 'hoo-token', 'hopr', 'hotnow', 'hplus', 'hrd', 'hubii-network', 'huobi-bitcoin-cash', 'huobi-ethereum', 'huobi-fil', 'huobi-litecoin', 'huobi-polkadot', 'hurify', 'hush', 'hut34-entropy', 'hydra', 'hymnode', 'hype', 'hype-finance', 'hyper-credit-network', 'hyper-pay', 'hyperquant', 'ibank', 'icex', 'idealcash', 'ideaology', 'idle-dai-risk-adjusted', 'idle-dai-yield', 'idle-susd-yield', 'idle-tusd-yield', 'idle-usdc-risk-adjusted', 'idle-usdc-yield', 'idle-usdt-risk-adjusted', 'idle-usdt-yield', 'idle-wbtc-yield', 'idl-token', 'idoneus-token', 'iftoken', 'ignite', 'ijascoin', 'impulse-by-fdr', 'imusify', 'incent', 'indexed-finance', 'indinode', 'inlock-token', 'inmax', 'insured-finance', 'intensecoin', 'interest-bearing-eth', 'interop', 'intervalue', 'investcoin', 'invox-finance', 'iote', 'isalcoin', 'istanbul-basaksehir-fan-token', 'izichain', 'jasmycoin', 'jfin-coin', 'jiaozi', 'jiviz', 'jpyq-stablecoin-by-q-dao-v1', 'juiice', 'jupiter', 'kanadecoin', 'karatgold-coin', 'katana-finance', 'kebab-token', 'keep3r-bsc-network', 'keep-calm', 'kiloample', 'kimchiswap', 'kimochi-finance', 'king-swap', 'kirobo', 'kitcoin', 'klayswap-protocol', 'klondike-btc', 'klondike-finance', 'knoxfs', 'kobocoin', 'koloop-basic', 'krios', 'k-tune', 'kush-finance', 'kuverit', 'kzcash', 'ladz', 'largo-coin', 'launchpool', 'lbrl', 'lendefi', 'lendhub', 'lendingblock', 'leocoin', 'level01-derivatives-exchange', 'levelapp', 'levelg', 'lhcoin', 'libonomy', 'libra-2', 'limestone-network', 'limitless-vip', 'linear-bsc', 'linix', 'linkbased', 'link-eth-rsi-ratio-trading-set', 'link-rsi-crossover-set', 'liquid-bank', 'liquid-defi', 'litebitcoin', 'litecoin-ultra', 'litentry', 'livenpay', 'load-network', 'lock-token', 'lotto', 'love-coin', 'lp-renbtc-curve', 'luckyseventoken', 'ludena-protocol', 'lux', 'luxurious-pro-network-token', 'lynx', 'machix', 'magnachain', 'mahadao', 'make-more-money', 'mangu', 'mantis-network', 'maps', 'marblecoin', 'marginswap', 'marlin', 'marscoin', 'mask-network', 'masq', 'matchpool', 'matic-aave-aave', 'matic-aave-link', 'matic-aave-usdc', 'matic-aave-usdt', 'matic-aave-weth', 'matic-aave-yfi', 'maxcoin', 'maya-preferred-223', 'mbm-token', 'mcbase-finance', 'mcobit', 'mdex', 'medibit', 'medican-coin', 'medooza-ecosystem', 'meetluna', 'menlo-one', 'meroechain', 'meshbox', 'metawhale-btc', 'metawhale-gold', 'mexc-token', 'midas-dollar', 'midas-dollar-share', 'mincoin', 'minds', 'minebee', 'mirrored-airbnb', 'mirrored-alibaba', 'mirrored-amazon', 'mirrored-amc-entertainment', 'mirrored-apple', 'mirrored-bitcoin', 'mirrored-ether', 'mirrored-facebook', 'mirrored-gamestop', 'mirrored-goldman-sachs', 'mirrored-google', 'mirrored-invesco-qqq-trust', 'mirrored-ishares-gold-trust', 'mirrored-ishares-silver-trust', 'mirrored-microsoft', 'mirrored-netflix', 'mirrored-proshares-vix', 'mirrored-tesla', 'mirrored-twitter', 'mirrored-united-states-oil-fund', 'mithril-share', 'mobilink-coin', 'modefi', 'molten', 'money-plant-token', 'moneyswap', 'moneytoken', 'monster-cash-share', 'monster-slayer-cash', 'moonbase', 'morcrypto-coin', 'mothership', 'mousecoin', 'mozox', 'mp3', 'mp4', 'mstable-btc', 'mti-finance', 'mt-pelerin-shares', 'mushroom', 'must', 'muzika-network', 'mvg-token', 'mybit-token', 'my-crypto-play', 'mykonos-coin', 'mynt', 'mytracknet-token', 'mytvchain', 'n3rd-finance', 'nagaswap', 'name-changing-token', 'nami-corporation-token', 'nanjcoin', 'nar-token', 'naruto-bsc', 'narwhale', 'natus-vincere-fan-token', 'nayuta-coin', 'ndex', 'netrum', 'neutrino-system-base-token', 'new-power-coin', 'newsolution', 'new-year-bull', 'nexalt', 'nextexchange', 'nftlootbox', 'nftx', 'nftx-hashmasks-index', 'nirvana', 'nitroex', 'nitrous-finance', 'noah-ark', 'noderunners', 'noiz-chain', 'noku', 'noob-finance', 'noodle-finance', 'nord-finance', 'northern', 'nova', 'novara-calcio-fan-token', 'npo-coin', 'nuvo-cash', 'nydronia', 'oasis-2', 'obee-network', 'obitan-chain', 'oduwausd', 'okexchain', 'olyseum', 'omniunit', 'one-cash', 'one-share', 'onix', 'online-expo', 'on-live', 'onx-finance', 'opennity', 'opium', 'orbitcoin', 'orbyt-token', 'orient', 'origin-dollar', 'orsgroup-io', 'oryx', 'our-pay', 'ovcode', 'ovr', 'oxbull-tech', 'p2p-solutions-foundation', 'paid-network', 'paint', 'pandacoin', 'panda-yield', 'pangolin', 'parallelcoin', 'partner', 'passive-income', 'paxex', 'payment-coin', 'paypex', 'payrue', 'payship', 'payyoda', 'pazzy', 'pbs-chain', 'peanut', 'peepcoin', 'peerplays', 'pegshares', 'percent', 'pesetacoin', 'p-ethereum', 'petrodollar', 'pgf500', 'phantom-token', 'philips-pay-coin', 'philscurrency', 'phoenixcoin', 'phoswap', 'piplcoin', 'pivx-lite', 'pizzaswap', 'playandlike', 'plex', 'plug', 'poc-blockchain', 'podo-point', 'pokeball', 'polaris-share', 'polkabase', 'polkabridge', 'polka-city', 'polkacover', 'polkainsure-finance', 'polkamarkets', 'pollux-coin', 'polyient-games-unity', 'pool-of-stake', 'pooltogether', 'poolz-finance', 'portion', 'postcoin', 'powercoin', 'predictz', 'premia', 'previse', 'prime-dai', 'prime-finance', 'primestone', 'privacy', 'project-shivom', 'propersix', 'prophecy', 'prosper', 'protocol-finance', 'provoco', 'psrs', 'psyche', 'psychic', 'ptokens-ltc', 'pub-finance', 'public-mint', 'pump-coin', 'punk', 'punk-attr-4', 'punk-attr-5', 'punk-basic', 'punk-female', 'pylon-network', 'pyro-network', 'q8e20-token', 'qdefi-rating-governance-token-v2', 'qiswap', 'qnodecoin', 'quai-dao', 'quantfury', 'quantis', 'qubitica', 'quick', 'quinads', 'qusd-stablecoin', 'r34p', 'r3fi-finance', 'rabbit-coin', 'rac', 'radicle', 'rai', 'ramenswap', 'raven-dark', 'raydium', 'razor-network', 'read-this-contract', 'real', 'realtract', 'rebased', 'reecore', 'reef-finance', 'reflector-finance', 'reflex', 'refract', 'relayer-network-2', 'relex', 'renbch', 'renewableelectronicenergycoin', 'renfil', 'reosc-ecosystem', 'rewardiqa', 'rex', 'rfbtc', 'rhegic2', 'riceswap', 'rich-lab-token', 'rich-maker', 'richway-finance', 'rigel-finance', 'rigoblock', 'rilcoin', 'rise-protocol', 'rivemont', 'rivermount', 'rivetz', 'rizen-coin', 'robot', 'rock3t', 'rocket-token', 'rocki', 'ror-universe', 'route', 'royale', 'rug-proof', 'runebase', 'rupaya', 'saave', 'safepal', 'satopay-yield-token', 'satoshivision-coin', 'saturn-classic-dao-token', 'saturn-network', 'sbnb', 'scex', 'scifi-finance', 'scrypta', 'seal-finance', 'sechain', 'secret-erc20', 'securypto', 'seos', 'sequence', 'serenity', 'sergs', 'serum-ecosystem-token', 'seur', 'sexcoin', 'shabu-shabu', 'shadow-token', 'shard', 'shareat', 'sharedstake-governance-token', 'sharpay', 'shiba-inu', 'shield-protocol', 'shitcoin-token', 'shopping-io', 'sicash', 'sifchain', 'signaturechain', 'silkchain', 'simba-storage-token', 'sinelock', 'sint-truidense-voetbalvereniging', 'siren', 'sixeleven', 'skillchain', 'sklay', 'skraps', 'skull-candy-shards', 'skyhub', 'slt', 'smartcoin', 'smart-dollar', 'smartkey', 'smartway-finance', 'snapparazzi', 'snodecoin', 'soak-token', 'soar-2', 'sociall', 'socketfinance', 'solaris', 'solomon-defi', 'somidax', 'sonocoin', 'sophiatx', 'sota-finance', 'soteria', 'sound-blockchain-protocol', 'sowing-network', 'sp8de', 'spaghetti', 'sparkle', 'sparkleswap-rewards', 'sparkpoint-fuel', 'sparkster', 'spectre-dividend-token', 'spectresecuritycoin', 'spice-finance', 'spiderdao', 'spiking', 'spindle', 'sponge', 'spore-engineering', 'sportx', 'sprint-coin', 'stake-dao', 'staked-ether', 'stakedxem', 'stakehound', 'stakehound-staked-ether', 'stamp', 'stand-cash', 'stand-share', 'starbugs-shards', 'stargaze-protocol', 'star-pacific-coin', 'sting', 'stipend', 'strain', 'streamix', 'stronghands-masternode', 'strudel-finance', 'stsla', 'student-coin', 'sucrecoin', 'sugarchain', 'sumcoin', 'superfarm', 'superskynet', 'supertron', 'supra-token', 'swaap-stablecoin', 'swapdex', 'swapship', 'swiftlance-token', 'swtcoin', 'sxag', 'sxau', 'sxmr', 'sxrp', 'sxtz', 'symverse', 'synchrobitcoin', 'tagcoin', 'talent-coin', 'tao-network', 'tapmydata', 'tap-project', 'tartarus', 'tatcoin', 'tavittcoin', 'taxi', 'tbc-mart-token', 'tcbcoin', 'tcoin-fun', 'team-finance', 'technology-innovation-project', 'tedesis', 'tenet', 'teslafunds', 'the-famous-token', 'thefutbolcoin', 'thegcccoin', 'the-graph', 'theholyrogercoin', 'themis-2', 'theresa-may-coin', 'the-smokehouse-finance', 'thingschain', 'thirm-protocol', 'thorchain-erc20', 'thore-exchange', 'tidex-token', 'timecoin-protocol', 'timeminer', 'tkn-token', 'tl-coin', 'tmc-niftygotchi', 'tokemon', 'tokenasset', 'tokengo', 'tokenlon', 'tokenstars-ace', 'tokentuber', 'topinvestmentcoin', 'tornado-cash', 'tornadocore', 'tosdis', 'toshi-token', 'touch-social', 'tozex', 'trade-butler-bot', 'trade-token', 'tradove', 'transmute', 'treelion', 'trias-token', 'trich', 'trinity-bsc', 'trinity-protocol', 'trism', 'trolite', 'trongamecenterdiamonds', 'tronnodes', 'trueaud', 'truegbp', 'truehkd', 'true-seigniorage-dollar', 'trust', 'trust-ether-reorigin', 'trustusd', 'trybe', 'try-finance', 'tsuki-dao', 'ttanslateme-network-token', 'ttcrypto', 'turbostake', 'typhoon-cash', 'ucash', 'ucoin', 'umbrella-network', 'unagii-dai', 'unagii-tether-usd', 'unagii-usd-coin', 'unidexgas', 'unifty', 'unikoin-gold', 'unilock-network', 'unimex-network', 'union-protocol-governance-token', 'unique-one', 'united-token', 'unitopia-token', 'unit-protocol-duck', 'universal-coin', 'universal-dollar', 'universal-gold', 'uptoken', 'up-token', 'urus-token', 'usdfreeliquidity', 'usdp', 'utopia-genesis-foundation', 'vai', 'vaiot', 'valid', 'valireum', 'value-usd', 'valuto', 'variable-time-dollar', 'varius', 'vault12', 'vecrv-dao-yvault', 'vega-coin', 'velo-token', 'venus-bch', 'venus-beth', 'venus-btc', 'venus-dai', 'venus-dot', 'venus-eth', 'venus-fil', 'venus-link', 'venus-ltc', 'venus-sxp', 'venus-usdc', 'venus-usdt', 'venus-xrp', 'venus-xvs', 'vera-cruz-coin', 'verasity', 'verox', 'versess-coin', 'versoview', 'vesper-finance', 'vice-industry-token', 'vidyx', 'viking-swap', 'vindax-coin', 'vinx-coin-sto', 'vip-coin', 'vivo', 'volentix-vtx', 'volume-network-token', 'vortex-defi', 'vpncoin', 'vspy', 'vsync', 'wadzpay-token', 'waletoken', 'wallet-plus-x', 'walnut-finance', 'wandx', 'warp-finance', 'water-token-2', 'wault-finance', 'waxe', 'webflix', 'web-token-pay', 'weedcash', 'whiteheart', 'wifi-coin', 'wild-beast-block', 'wild-crypto', 'winding-tree', 'winstars', 'wise-token11', 'wmatic', 'wm-professional', 'worktips', 'worldcoin', 'world-token', 'wowswap', 'wrapped-bind', 'wrapped-celo', 'wrapped-dgld', 'wrapped-filecoin', 'wrapped-polis', 'wrapped-statera', 'wrapped-terra', 'wrapped-virgin-gen-0-cryptokitties', 'wrapped-wagerr', 'wrapped-zcash', 'x8-project', 'xaavea', 'xaaveb', 'xank', 'xcoin', 'xdai', 'xdef-finance', 'xeno-token', 'xeuro', 'xfund', 'xincha', 'xinchb', 'xion-global-token', 'xknca', 'xmon', 'xnode', 'xov', 'xptoken-io', 'xrp-classic', 'xscoin', 'xsigma', 'xsnx', 'xstable-protocol', 'xsushi', 'xtock', 'xtoken', 'xvix', 'y-coin', 'yd-eth-mar21', 'yearn20moonfinance', 'yearn4-finance', 'yearn-ethereum-finance', 'yearn-finance-ecosystem', 'yearn-finance-infrastructure-labs', 'yearn-finance-passive-income', 'yearn-finance-red-moon', 'yearn-shark-finance', 'yes', 'yfiii', 'yfilend-finance', 'yfione', 'yflink-synthetic', 'yfmoonbeam', 'yfpro-finance', 'yfscience', 'yftether', 'yield-app', 'yield-farming-token', 'yieldnyan-token', 'yield-optimization-platform', 'yieldpanda', 'yottachainmena', 'young-boys-fan-token', 'yplutus', 'ytsla-finance', 'yup', 'yvs-finance', 'zer-dex', 'zero-exchange', 'zettelkasten', 'zillionlife', 'zinc', 'zkswap', 'zodiac', 'zom', 'zoom-protocol', 'zper', 'zrocor', 'ztranzit-coin', 'zupi-coin']

#print(ReturnFileData(30, '11.03.2021'))
#RedditCommentChange(coins, d1, m1, y1, d2, m2, y2, up_by):
#FilterInactive(coins, reddit_post_min, reddit_comment_min, alexa_rank_min, pull_requests_merged_min)
#ResetAndCheckAll(30, '10.03.2021')
# note to myself: feature "hypedate", showing all coins, which social media attention did a y-x over the course of z - time
print(RedditCommentChange(data, '05', '03', '2021', '12', '03', '2021', 1.5))


#TTPSConnectionPool(host='api.coingecko.com', port=443): Max retries exceeded with url: /api/v3/coins/100-waves-eth-usd-yield-set/history?date=12-03-2021&localization=false (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x0000019071572AC0>: Failed to establish a new connection: [Errno 11001] getaddrinfo failed'))
