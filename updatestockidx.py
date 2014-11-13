# -*- coding: utf-8 -*-
import os
import sys
import datetime
import math
import stockconfig
import MySQLdb as mdb
import stockidx as idx
from decimal import *

class WinSize:
    WEEK = 5
    MONTH = 20
    SEASON = 60
    AVAILABLE_SIZE = {WEEK, MONTH, SEASON}
    
def iswinvalid(size):
    return size in WinSize.AVAILABLE_SIZE

def getallid(cur, stocktype):
    cur.execute('SELECT DISTINCT ID FROM DAILY_TRADE WHERE TYPE=%s;', stocktype)
    return zip(*cur.fetchall())[0]
    
def decimalround(value):
    if math.isnan(value):
        return value
    else:
        return Decimal(value).quantize(Decimal('.01'), rounding = ROUND_HALF_UP)
    
def update_ma(cur, stockid, stocktype, lastdate, window):
    if not iswinvalid(window):
        raise ValueError("Invalid window size!")

    cur.execute('SELECT TRADE_DATE FROM DAILY_TRADE WHERE ID=%s AND TYPE=%s AND TRADE_DATE<=%s ORDER BY TRADE_DATE DESC LIMIT %s',
                (stockid, stocktype, lastdate, window))
    rows = cur.fetchall()
    if len(rows) == 0:
        basedate = lastdate
        predays = 0
    else:
        basedate = rows[-1][0]
        predays = len(rows) - 1

    cur.execute('SELECT ID, TRADE_DATE, TYPE, CLOSE FROM DAILY_TRADE WHERE ID=%s AND TRADE_DATE>=%s AND TYPE=%s ORDER BY TRADE_DATE ASC',
                (stockid, basedate, stocktype));
    rowst = zip(*cur.fetchall())
    if len(rowst) == 0 or len(rowst[1]) < window:
        return
    
    ma = idx.moving_avg(rowst[3], window)
    for i in range(predays, len(rowst[1])):
        roundval = None if math.isnan(ma[i]) else decimalround(ma[i])
        cur.execute('INSERT INTO DAILY_INDEX (ID,TYPE,TRADE_DATE,MA_CLOSE_' + `window` +') ' +
                    'VALUES (%s,%s,%s,%s) ON DUPLICATE KEY UPDATE ' +
                    'MA_CLOSE_' + `window` + '=%s;',
                    (stockid, stocktype, rowst[1][i], roundval, roundval));
    cur.execute('COMMIT;')

if __name__ == '__main__':    
    p = stockconfig.load()
    lastupdate = p['listed.lastUpdateIdx'].strip().split('-')
    listedlast = datetime.date(int(lastupdate[0]), int(lastupdate[1]), int(lastupdate[2])) + datetime.timedelta(1)
    lastupdate = p['otc.lastUpdateIdx'].strip().split('-')
    otclast = datetime.date(int(lastupdate[0]), int(lastupdate[1]), int(lastupdate[2])) + datetime.timedelta(1)

    print '[START] Updating stock index...'
    if p['listed.isUpdateIdx'] == 'false':
        print '[CONFIG] Listed companies are *NOT* being updated.'
    if p['otc.isUpdateIdx'] == 'false':
        print '[CONFIG] Over the counter companies are *NOT* being updated.'

    con = mdb.connect('localhost', 'stock', 'stock', 'TW_STOCK')
    with con:
        cur = con.cursor()
        today = datetime.date.today()
    
        if p['listed.isUpdateIdx'] != 'false':
            print '\tUpdating listed companies stock index...'
        
            lastdate = listedlast
            if lastdate < today:
                lastdatestr = lastdate.strftime('%Y-%m-%d')
                stocktype = 'L'
                stocklist = getallid(cur, stocktype)
                
                # Moving averages
                for ws in WinSize.AVAILABLE_SIZE:
                    print '\tProcessing ' + `ws` + '-day moving average'
                    for stockid in stocklist:
                        #print '\tID: ' + stockid
                        update_ma(cur, stockid, stocktype, lastdatestr, ws)
        
            # Write back to configuration file
            p['listed.lastUpdateIdx'] = (today - datetime.timedelta(1)).strftime('%Y-%m-%d')
            stockconfig.save(p)
            
        if p['otc.isUpdateIdx'] != 'false':
            print '\tUpdating over the counter companies stock index...'
        
            lastdate = otclast
            if lastdate < today:
                lastdatestr = lastdate.strftime('%Y-%m-%d')
                stocktype = 'O'
                stocklist = getallid(cur, stocktype)
                
                # Moving averages
                for ws in WinSize.AVAILABLE_SIZE:
                    print '\tProcessing ' + `ws` + '-day moving average'
                    for stockid in stocklist:
                        #print '\tID: ' + stockid
                        update_ma(cur, stockid, stocktype, lastdatestr, ws)

            # Write back to configuration file
            p['otc.lastUpdateIdx'] = (today - datetime.timedelta(1)).strftime('%Y-%m-%d')
            stockconfig.save(p)

    print '[DONE]'