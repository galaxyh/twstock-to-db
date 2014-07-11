import os.path
from pyjavaproperties import Properties

# Default configuration file name
DEFAULT_CONFIG_FILENAME = 'stock.properties'

# The default path for downloaded data
DEFAULT_LISTED_PRICE_PATH = 'price_listed'
DEFAULT_LISTED_INST_PATH = 'inst_listed'
DEFAULT_OTC_PRICE_PATH = 'price_otc'
DEFAULT_OTC_INST_PATH = 'inst_otc'

# The default date of the latest data processed
DEFAULT_START_DATE = '2011-12-31'

def load(filename=DEFAULT_CONFIG_FILENAME):
    p = Properties()
    if os.path.isfile(filename):
        p.load(open('stock.properties'))

    if not p['listed.pricePath'].strip():
        p['listed.pricePath'] = DEFAULT_LISTED_PRICE_PATH
    if not p['listed.instPath'].strip():
        p['listed.instPath'] = DEFAULT_LISTED_INST_PATH
    
    if not p['listed.lastDownload'].strip():
        p['listed.lastDownload'] = DEFAULT_START_DATE
    if p['listed.isDownload'].strip() != 'false':
        p['listed.isDownload'] = 'true'
    
    if not p['listed.lastUpdateDb'].strip():
        p['listed.lastUpdateDb'] = DEFAULT_START_DATE
    if p['listed.isUpdateDb'].strip() != 'false':
        p['listed.isUpdateDb'] = 'true'

    if not p['otc.pricePath'].strip():
        p['otc.pricePath'] = DEFAULT_OTC_PRICE_PATH
    if not p['otc.instPath'].strip():
        p['otc.instPath'] = DEFAULT_OTC_INST_PATH
        
    if not p['otc.lastDownload'].strip():
        p['otc.lastDownload'] = DEFAULT_START_DATE
    if p['otc.isDownload'].strip() != 'false':
        p['otc.isDownload'] = 'true'
    
    if not p['otc.lastUpdateDb'].strip():
        p['otc.lastUpdateDb'] = DEFAULT_START_DATE
    if p['otc.isUpdateDb'].strip() !='false':
        p['otc.isUpdateDb'] = 'true'

    if not p['db.server'].strip():
        p['db.server'] = 'SERVER_NAME'
    if not p['db.username'].strip():
        p['db.username'] = 'USERNAME'
    if not p['db.password'].strip():
        p['db.password'] = 'PASSWORD'
    if not p['db.database'].strip():
        p['db.database'] = 'DATABASE_NAME'

    return p

def save(config, filename=DEFAULT_CONFIG_FILENAME):
    config.store(open(filename,'w')) 
