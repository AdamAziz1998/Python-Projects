from tqdm import tqdm
import pandas as pd
from binance.client import Client
from sqlalchemy import create_engine
import config

from datetime import datetime
from datetime import timedelta

client = Client(config.apiKey, config.apiSecret)
engine = create_engine('sqlite:///Cryptoprices.db')

coins = ('BTCUSDT','ETHUSDT','BNBUSDT','SOLUSDT','ADAUSDT','XRPUSDT','DOTUSDT','LUNAUSDT',
	'DOGEUSDT','AVAXUSDT','SHIBUSDT','MATICUSDT','LTCUSDT','UNIUSDT','ALGOUSDT','TRXUSDT',
	'LINKUSDT','MANAUSDT','ATOMUSDT','VETUSDT')

def getData(symbol : str, start : str, engine : object):
	frame = pd.DataFrame(client.get_historical_klines(symbol,
		'1m',
		start))
	frame = frame.loc[:,[0,3]]
	frame.columns = ['Time','Close']
	frame[['Close']] = frame[['Close']].astype(float)
	frame.Time = pd.to_datetime(frame.Time, unit='ms')
	return frame

def newDB(symbol : str, start : str, engine : object):
	frame = getData(symbol, start, engine)
	frame.to_sql(symbol, engine, index=False)

def readData(symbol : str, engine : object):
	frame = pd.read_sql(symbol, engine)
	return frame

def updateData(symbol : str, engine : object):
	frame = readData(symbol, engine)
	start_minus1 = frame.Time.loc[frame.Time.last_valid_index()] 

	start_datetime = start_minus1 + timedelta(minutes=1)

	new_data = getData(symbol, start_datetime.strftime('%Y-%m-%d %H:%M:%S'), engine)
	new_data.to_sql(symbol, engine, if_exists='append', index=False)

def updateSetData(symbols : tuple, engine : object):
	for symbol in symbols:
		updateData(symbol, engine)
		print(str(symbol)+' data updated successfully')