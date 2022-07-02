import numpy as np
import pandas as pd

from sqlalchemy import create_engine
from back_test import Backtest_Strat
import trading_data as td
from tqdm import tqdm
import matplotlib.pyplot as plt
from matplotlib import cm

from hard_optimize import optimize

def map_square_matrix(matrix):
	matrix = np.array(matrix)
	x_values = np.linspace(1, len(matrix), len(matrix)).astype(int)
	y_values = np.linspace(1, len(matrix), len(matrix)).astype(int)
	X, Y = np.meshgrid(x_values, y_values)

	ax = plt.axes(projection='3d')
	ax.plot_surface(X, Y, matrix, cmap=cm.coolwarm)
	ax.set_xlabel('Fast Moving Average')
	ax.set_ylabel('Slow Moving Average')
	ax.set_zlabel('Returns')
	plt.show()

def map_list(ls):
	df = pd.DataFrame(np.array(ls))
	print(df)
	df.plot()
	plt.show()

engine = create_engine('sqlite:///Cryptoprices.db')
frame = td.readData('BTCUSDT', engine)
ls_inputs = [i for i in range(1, 1074, 1)]
Z = optimize.fixed_slow_average(frame, 1075, ls_inputs)
map_list(Z)