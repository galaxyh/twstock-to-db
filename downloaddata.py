import datetime
import stockconfig
from urllib import urlretrieve

# Listed companies URLs
# Example: http://www.twse.com.tw/ch/trading/fund/T86/print.php?edition=ch&filename=genpage/201406/20140615_2by_stkno.dat&type=csv&select2=ALL
INST_LISTED_URL = 'http://www.twse.com.tw/ch/trading/fund/T86/print.php?edition=ch&filename=genpage/%s/%s_2by_stkno.dat&type=csv&select2=ALL'

# Over the counter companies URLs
# Price Example: http://www.gretai.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d=103/07/02&s=0,asc,0
PRICE_OTC_URL = 'http://www.gretai.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d=%s&s=0,asc,0'

# Institution Example: http://www.gretai.org.tw/ch/stock/3insti/DAILY_TradE/3itrade_download.php?t=D&d=103/06/17&s=0,asc,0
INST_OTC_URL = 'http://www.gretai.org.tw/ch/stock/3insti/DAILY_TradE/3itrade_download.php?t=D&d=%s&s=0,asc,0'

p = stockconfig.load()
lastdownload = p['listed.lastDownload'].strip().split('-')
listedlast = datetime.date(int(lastdownload[0]), int(lastdownload[1]), int(lastdownload[2])) + datetime.timedelta(1)
lastdownload = p['otc.lastDownload'].strip().split('-')
otclast = datetime.date(int(lastdownload[0]), int(lastdownload[1]), int(lastdownload[2])) + datetime.timedelta(1)

print '[START] Downloading stock data...'
if p['listed.isDownload'] == 'false':
    print '[CONFIG] Listed companies are *NOT* being downloaded.'
if p['otc.isDownload'] == 'false':
    print '[CONFIG] Over the counter companies are *NOT* being downloaded.'

today = datetime.date.today()

if p['listed.isDownload'] != 'false':
    print '\tDownloading listed companies data...'
    lastdate = listedlast
    while lastdate < today:
        inst_url = INST_LISTED_URL % (lastdate.strftime('%Y%m'), lastdate.strftime('%Y%m%d'))

        tradedate = lastdate.strftime('%Y-%m-%d')
        print '\tDate: ' + tradedate

        try:
            urlretrieve(inst_url, p['listed.instPath'] + '/' + tradedate + '.csv')
        except IOError as e:
            print '[ERROR] I/O error({0}): {1}'.format(e.errno, e.strerror)
            break
        except:
            print '[ERROR] Content too short error({0}): {1}'.format(e.errno, e.strerror)
            break
    
        # Write back to configuration file
        p['listed.lastDownload'] = tradedate
        stockconfig.save(p)
        lastdate = lastdate + datetime.timedelta(1)

if p['otc.isDownload'] != 'false':
    print '\tDownloading over the counter companies data...'
    lastdate = otclast
    while lastdate < today:
        price_url = PRICE_OTC_URL % (str(int(lastdate.strftime('%Y')) - 1911) + lastdate.strftime('/%m/%d'))
        inst_url = INST_OTC_URL % (str(int(lastdate.strftime('%Y')) - 1911) + lastdate.strftime('/%m/%d'))
    
        tradedate = lastdate.strftime('%Y-%m-%d')
        print '\tDate: ' + tradedate

        try:
            urlretrieve(price_url, p['otc.pricePath'] + '/' + tradedate + '.csv')
            urlretrieve(inst_url, p['otc.instPath'] + '/' + tradedate + '.csv')
        except IOError as e:
            print '[ERROR] I/O error({0}): {1}'.format(e.errno, e.strerror)
            break
        except ContentTooShortError as e:
            print '[ERROR] Content too short error({0}): {1}'.format(e.errno, e.strerror)
            break
    
        # Write back to configuration file
        p['otc.lastDownload'] = tradedate
        stockconfig.save(p)
        lastdate = lastdate + datetime.timedelta(1)

print '[DONE]'
