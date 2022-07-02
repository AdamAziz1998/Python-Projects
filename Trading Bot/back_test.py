import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine

import trading_data as td
from strategies import Strategy

class Backtest:
	def __init__(self, frame, start_bal):
		self.frame = frame
		self.start_bal = start_bal
		self.fee_prod = (1 + 0.00075)**(-1)

	#this backtest doesnt use logarithmic returns, this means that it will take slightly mroe time
	#but, it will give a slightly better voerview of what is happening
	def backtest(self):
		#the bench balance, peak, drawdown, and returns 
		self.frame['Bench_Ret'] = self.frame.Close / self.frame.Close.shift(1)
		self.frame.Bench_Ret.iat[0] = 1
		self.frame['Bench_Bal'] = self.start_bal * self.frame.Bench_Ret.cumprod()

		#The system bal, peak, drawdown, costs, and returns
		self.frame['Sys_Ret'] = np.where(self.frame.position.shift(1) == 1, self.frame.Bench_Ret, 1)
		cost_in = np.where(self.frame.position.diff().shift(1) == 1, self.fee_prod, 1) #0.00075 are the fees
		cost_out = np.where(self.frame.position.diff() == -1, self.fee_prod, 1)
		self.frame['Sys_Cost'] = cost_in * cost_out
		self.frame['Sys_Net_Ret'] = self.frame.Sys_Ret * self.frame.Sys_Cost
		self.frame['Sys_Bal'] = self.start_bal * self.frame.Sys_Net_Ret.cumprod()
		
		return self.frame

	#the log function is more efficient, but only shows the final result, this is good for optimization
	def backtest_log_ret(self):
		self.frame['Log_Bench_Ret'] = np.log(self.frame.Close.pct_change() + 1)
		self.frame['Log_Sys_Ret'] = self.frame.position.shift(1) * self.frame.Log_Bench_Ret
		trades = self.frame.position.diff().value_counts().iloc[1:].sum()
		costs = self.fee_prod ** trades
		bench_return = np.exp((self.frame.Log_Bench_Ret).sum())
		sys_return = np.exp(self.frame.Log_Sys_Ret.sum()) * costs

		return bench_return, sys_return

	def plot_returns(self):
		self.frame = self.backtest()
		print(self.frame)
		#start
		print(f"Starting Balance: {self.start_bal}")
		#end
		print(f"Ending Balance: {self.frame.Sys_Bal.loc[self.frame.Sys_Bal.last_valid_index()]}")
		#exposure time
		print(f"Exposure [%]: {frame.position.describe().mean}")
		#return %
		print(f"Return [%]: {(self.frame.Sys_Bal.loc[self.frame.Sys_Bal.last_valid_index()] / self.start_bal) - 1}")
		#bench return %
		print(f"Buy and hold return: {(self.frame.Bench_Bal.loc[self.frame.Bench_Bal.last_valid_index()] / self.start_bal) - 1}")
		#volatility %

		#sharpe ratio

		#sortino ratio

		#max drawdown %

		#avg drawdown %

		#max drawdown duration

		#avg drawdown duration

		#Trades

		#win rate %

		#avg trade %

		#max trade duration

		#avg trade duration

		#SQN

		plt.plot(self.frame.Bench_Bal)
		plt.plot(self.frame.Sys_Bal)
		plt.legend(labels = ['Bench','System'])
		plt.show()


class Backtest_Strat: #this class made for optimizing
	def MACD(frame, slow_SMA_period, fast_SMA_period):
		frame = frame.copy()
		frame = Strategy.MACD(frame, slow_SMA_period, fast_SMA_period)
		b_test = Backtest(frame, 10000)
		bench_return, sys_return = b_test.backtest_log_ret()
		return bench_return, sys_return

	def simple_momentum(frame, slow_SMA_period, fast_SMA_period):
		frame = frame.copy()
		frame = Strategy.simple_momentum(frame, slow_SMA_period, fast_SMA_period)
		b_test = Backtest(frame, 10000)
		bench_return, sys_return = b_test.backtest_log_ret()
		return bench_return, sys_return

	def simple_momentum_stop_loss(frame, slow_SMA_period, fast_SMA_period, stop_loss_pct):
		frame = frame.copy()
		frame = Strategy.simple_momentum_stop_loss(frame, slow_SMA_period, fast_SMA_period, stop_loss_pct)
		b_test = Backtest(frame, 10000)
		bench_return, sys_return = b_test.backtest_log_ret()
		return bench_return, sys_return

engine = create_engine('sqlite:///Cryptoprices.db')
frame = td.readData('BTCUSDT', engine)
slow_SMA_period = 1074
fast_SMA_period = 381
stop_loss_pct = 0.15
frame = Strategy.simple_momentum(frame, slow_SMA_period, fast_SMA_period)

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)
B = Backtest(frame,frame.Close.loc[0])
frame = B.backtest()
print(frame)

frame.Bench_Bal.plot()
frame.Sys_Bal.plot()
frame.SMA_fast.plot()
frame.SMA_slow.plot()
plt.legend()
plt.show()
#print(Backtest_Strat.simple_momentum_stop_loss(frame, slow_SMA_period, fast_SMA_period, stop_loss_pct))