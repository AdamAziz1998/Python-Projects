import pandas as pd
import numpy as np

class Indicators:
	def MACD_signal(
		frame, 
		slow_SMA_period, 
		fast_SMA_period,
		):

		frame['SMA_slow'] = frame.Close.rolling(slow_SMA_period).mean()
		frame['SMA_fast'] = frame.Close.rolling(fast_SMA_period).mean()
		frame['Macd'] = frame.SMA_slow - frame.SMA_fast
		frame['Signal'] = frame.Macd.ewm(span = 9, adjust=False).mean()

		return frame

	def simple_momentum(
		frame, 
		slow_SMA_period, 
		fast_SMA_period,
		):

		frame['SMA_fast'] = frame.Close.rolling(fast_SMA_period).mean()
		frame['SMA_slow'] = frame.Close.rolling(slow_SMA_period).mean()

		return frame

	def simple_momentum_stop_loss(
		frame, 
		slow_SMA_period, 
		fast_SMA_period, 
		stop_loss_pct,
		):

		frame['SMA_fast'] = frame.Close.rolling(fast_SMA_period).mean()
		frame['SMA_slow'] = frame.Close.rolling(slow_SMA_period).mean()

		return frame




#in this class we will take in a dataframe of closing prices with the corresponding indicators
#we will then create a new column with the signal line wihtin
class Strategy:
	def MACD(frame, slow_SMA_period, fast_SMA_period):
		frame = Indicators.MACD_signal(frame, slow_SMA_period, fast_SMA_period)
		frame['position'] = np.where(frame.Macd > frame.Signal, 1, 0)
		frame.dropna(inplace=True)
		frame.reset_index(drop=True, inplace=True)
		return frame

	def simple_momentum(frame, slow_SMA_period, fast_SMA_period):
		frame = Indicators.simple_momentum(frame, slow_SMA_period, fast_SMA_period)
		frame['position'] = np.where(frame.SMA_slow < frame.SMA_fast, 1, 0)
		frame.dropna(inplace=True) 
		frame.reset_index(drop=True, inplace=True)
		return frame

	def simple_momentum_stop_loss(frame, slow_SMA_period, fast_SMA_period, stop_loss_pct):

		frame = Indicators.simple_momentum_stop_loss(frame, slow_SMA_period, fast_SMA_period, stop_loss_pct)
		frame1 = frame.copy()
		frame['position_no_stop_loss'] = np.where(frame.SMA_slow < frame.SMA_fast, 1, 0)
		frame['buy_point'] = np.where(frame.position_no_stop_loss > frame.position_no_stop_loss.shift(1), frame.Close, np.nan)
		frame.buy_point.ffill(axis = 0, inplace=True)
		frame['buy_price'] = frame.position_no_stop_loss * frame.buy_point

		frame['stop_loss'] = np.where(
			(frame.Close > (frame.buy_price * (1 - stop_loss_pct))) & (frame.position_no_stop_loss==1), 
			1, 
			0)
		frame['events'] = (frame.position_no_stop_loss + frame.stop_loss).diff()
		frame.drop(frame[frame.events==0].index, inplace=True)
		frame.drop(
			frame[(frame.events==1) | (frame.events.shift(1)==1) | ((frame.events.shift(1)==-1) & (frame.events==-1))].index, 
			inplace=True)

		frame.drop(
			columns=[
				'SMA_fast', 
				'SMA_slow',
				'position_no_stop_loss',  
				'buy_point',  
				'buy_price',  
				'stop_loss',  
				'events',
				'Time',
				'Close',
				], 
			inplace=True
			)
		frame['position'] = 1
		frame = pd.concat([frame1, frame], axis=1)
		frame['cum_pos'] = frame.position.cumsum().fillna(method='ffill')
		frame.cum_pos = np.where(frame.cum_pos%2!=0, frame.cum_pos.shift(1), frame.cum_pos)
		frame.position = np.where(frame.cum_pos%2!=0, 0, 1)
		frame.drop(columns=['cum_pos'],inplace=True)

		frame.dropna(inplace=True)
		frame.reset_index(drop=True, inplace=True)
		return frame

#from sqlalchemy import create_engine
#import trading_data as td
#engine = create_engine('sqlite:///Cryptoprices.db')
#frame = td.readData('BTCUSDT', engine)
#slow_SMA_period = 100
#fast_SMA_period = 10
#stop_loss_pct = 0.03
#frame = Strategy.simple_momentum_stop_loss(frame, slow_SMA_period, fast_SMA_period, stop_loss_pct)
#
#
#pd.set_option('display.max_rows', None)
#print(frame.head(1000))