# -*- coding: utf-8 -*-
import os
import sys
import csv
import datetime
import stockconfig
import MySQLdb as mdb

p = stockconfig.load()
lastupdatedb = p['listed.lastUpdateDb'].strip().split('-')
listedlast = datetime.date(int(lastupdatedb[0]), int(lastupdatedb[1]), int(lastupdatedb[2])) + datetime.timedelta(1)
lastupdatedb = p['otc.lastUpdateDb'].strip().split('-')
otclast = datetime.date(int(lastupdatedb[0]), int(lastupdatedb[1]), int(lastupdatedb[2])) + datetime.timedelta(1)

print '[START] Updating stock data...'
if p['listed.isUpdateDb'] == 'false':
    print '[CONFIG] Listed companies are *NOT* being updated.'
if p['otc.isUpdateDb'] == 'false':
    print '[CONFIG] Over the counter companies are *NOT* being updated.'

con = mdb.connect('localhost', 'stock', 'stock', 'TW_STOCK')
with con:
    cur = con.cursor()
    today = datetime.date.today()
    
    #if p['listed.isUpdateDb'] != 'false':
        # TODO: Add update code here.
    
    if p['otc.isUpdateDb'] != 'false':
        print '\tUpdating over the counter companies data...'
        
        lastdate = otclast       
        while lastdate < today:
            tradedate = lastdate.strftime('%Y-%m-%d')
            print '\tDate: ' + tradedate

            # Update price
            with open(p['otc.pricePath'] + '/' + tradedate + '.csv', 'r') as f:            
                reader = csv.reader(f)
                for row in reader:
                    if len(row) != 17: # Skip illegal rows
                        continue
                    if len(row[0].decode('big5').strip()) < 4: # Skip header
                        continue
                    
                    stockid = row[0].strip()
                    stocktype = 'O' # Over the Counter companies
                    popen = row[4].strip().replace(',', '')
                    if popen[1] == '-': # Ignore records with price equals to '---'
                        continue
                    phigh = row[5].strip().replace(',', '')
                    plow = row[6].strip().replace(',', '')
                    pclose = row[2].strip().replace(',', '')
                    vol = row[8].strip().replace(',', '')
                    cur.execute('INSERT INTO DAILY_TRADE (ID,TRADE_DATE,TYPE,OPEN,HIGH,LOW,CLOSE,VOL) ' +
                                'VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE ' +
                                'TYPE=%s,OPEN=%s,HIGH=%s,LOW=%s,CLOSE=%s,VOL=%s;',
                                (stockid, tradedate, stocktype, popen, phigh, plow, pclose, vol,
                                stocktype, popen, phigh, plow, pclose, vol));

            # Update institution net buy data
            with open(p['otc.instPath'] + '/' + tradedate + '.csv', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) != 12: # Skip illegal rows
                        continue
                    if len(row[0].decode('big5').strip()) < 4: # Skip header
                        continue
                    
                    stockid = row[0].strip()
                    fii = row[4].strip().replace(',', '')
                    di = row[7].strip().replace(',', '')
                    dealer = row[10].strip().replace(',', '')
                    cur.execute('UPDATE DAILY_TRADE SET FII_CAPITAL=%s, DI_CAPITAL=%s, DEALER_CAPITAL=%s ' +
                                'WHERE ID=%s AND TRADE_DATE=%s;', (fii, di, dealer, stockid, tradedate));
            
            cur.execute('COMMIT;')
            
            # Write back to configuration file
            p['otc.lastUpdateDb'] = tradedate
            stockconfig.save(p)
            lastdate = lastdate + datetime.timedelta(1)

print '[DONE]'