# -*- coding: utf-8 -*-
import os
import sys
import csv
import datetime
import stockconfig
import MySQLdb as mdb

MAX_ID_LENGTH = 10

p = stockconfig.load()
lastupdate = p['listed.lastUpdateDb'].strip().split('-')
listedlast = datetime.date(int(lastupdate[0]), int(lastupdate[1]), int(lastupdate[2])) + datetime.timedelta(1)
lastupdate = p['otc.lastUpdateDb'].strip().split('-')
otclast = datetime.date(int(lastupdate[0]), int(lastupdate[1]), int(lastupdate[2])) + datetime.timedelta(1)

print '[START] Updating stock data...'
if p['listed.isUpdateDb'] == 'false':
    print '[CONFIG] Listed companies are *NOT* being updated.'
if p['otc.isUpdateDb'] == 'false':
    print '[CONFIG] Over the counter companies are *NOT* being updated.'

con = mdb.connect('localhost', 'stock', 'stock', 'TW_STOCK')
with con:
    cur = con.cursor()
    today = datetime.date.today()
    
    if p['listed.isUpdateDb'] != 'false':
        print '\tUpdating listed companies data...'
        
        lastdate = listedlast       
        while lastdate < today:
            tradedate = lastdate.strftime('%Y-%m-%d')
            print '\tDate: ' + tradedate

            # Update price
            with open(p['listed.pricePath'] + '/' + tradedate + '.csv', 'r') as f:            
                reader = csv.reader(f)
                for row in reader:
                    if len(row) != 16: # Skip illegal rows
                        continue

                    firstcol = row[0].decode('big5').encode('utf8').strip();
                    if (firstcol == '證券代號') or (len(firstcol) > MAX_ID_LENGTH): # Skip header
                        continue

                    stockid = row[0].decode('big5').replace('"', '').replace('=', '')
                    popen = row[5].strip().replace(',', '')
                    if popen[1] == '-': # Ignore records with price equals to '--'
                        continue
                    phigh = row[6].strip().replace(',', '')
                    plow = row[7].strip().replace(',', '')
                    pclose = row[8].strip().replace(',', '')
                    vol = row[2].strip().replace(',', '')
                    per = row[15].strip().replace(',','')
                    cur.execute('INSERT INTO DAILY_TRADE (ID,TYPE,TRADE_DATE,OPEN,HIGH,LOW,CLOSE,VOL,PER) ' +
                                'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE ' +
                                'TYPE=%s,OPEN=%s,HIGH=%s,LOW=%s,CLOSE=%s,VOL=%s,PER=%s;',
                                (stockid, 'L', tradedate, popen, phigh, plow, pclose, vol, per,
                                'L', popen, phigh, plow, pclose, vol, per));
            
            # Update institution net buy data
            with open(p['listed.instPath'] + '/' + tradedate + '.csv', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) != 9: # Skip illegal rows
                        continue
                    
                    firstcol = row[0].decode('big5').encode('utf8').strip();
                    if (firstcol == '證券代號') or (len(firstcol) > MAX_ID_LENGTH): # Skip header
                        continue
                    
                    stockid = row[0].decode('big5').replace('"', '').replace('=', '')
                    fii = int(row[2].strip().replace(',', '')) - int(row[3].strip().replace(',', ''))
                    di = int(row[4].strip().replace(',', '')) - int(row[5].strip().replace(',', ''))
                    dealer = int(row[6].strip().replace(',', '')) - int(row[7].strip().replace(',', ''))
                    cur.execute("UPDATE DAILY_TRADE SET FII_CAPITAL=%s, DI_CAPITAL=%s, DEALER_CAPITAL=%s " +
                                "WHERE ID=%s AND TRADE_DATE=%s AND TYPE='L';", (fii, di, dealer, stockid, tradedate));
            cur.execute('COMMIT;')
            
            # Write back to configuration file
            p['listed.lastUpdateDb'] = tradedate
            stockconfig.save(p)
            lastdate = lastdate + datetime.timedelta(1)
    
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
                    
                    firstcol = row[0].decode('big5').encode('utf8').strip();
                    if (firstcol == '代號') or (len(firstcol) > MAX_ID_LENGTH): # Skip header
                        continue

                    stockid = row[0].strip()
                    if len(stockid) > 4: # Skip warrant
                        continue

                    popen = row[4].strip().replace(',', '')
                    if popen[1] == '-': # Ignore records with price equals to '---'
                        continue
                    phigh = row[5].strip().replace(',', '')
                    plow = row[6].strip().replace(',', '')
                    pclose = row[2].strip().replace(',', '')
                    vol = row[8].strip().replace(',', '')
                    cur.execute('INSERT INTO DAILY_TRADE (ID,TYPE,TRADE_DATE,OPEN,HIGH,LOW,CLOSE,VOL) ' +
                                'VALUES (%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE ' +
                                'TYPE=%s,OPEN=%s,HIGH=%s,LOW=%s,CLOSE=%s,VOL=%s;',
                                (stockid, 'O', tradedate, popen, phigh, plow, pclose, vol,
                                'O', popen, phigh, plow, pclose, vol));

            # Update institution net buy data
            with open(p['otc.instPath'] + '/' + tradedate + '.csv', 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) != 12: # Skip illegal rows
                        continue
                    
                    firstcol = row[0].decode('big5').encode('utf8').strip();
                    if (firstcol == '代號') or (len(firstcol) > MAX_ID_LENGTH): # Skip header
                        continue
                    
                    stockid = row[0].strip()
                    fii = row[4].strip().replace(',', '')
                    di = row[7].strip().replace(',', '')
                    dealer = row[10].strip().replace(',', '')
                    cur.execute("UPDATE DAILY_TRADE SET FII_CAPITAL=%s, DI_CAPITAL=%s, DEALER_CAPITAL=%s " +
                                "WHERE ID=%s AND TRADE_DATE=%s AND TYPE='O';", (fii, di, dealer, stockid, tradedate));
            
            cur.execute('COMMIT;')
            
            # Write back to configuration file
            p['otc.lastUpdateDb'] = tradedate
            stockconfig.save(p)
            lastdate = lastdate + datetime.timedelta(1)

stockconfig.save(p)
print '[DONE]'