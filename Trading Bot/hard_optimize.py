from back_test import Backtest_Strat
from tqdm import tqdm


class optimize:

	def fixed_slow_average(frame, slow_average, ls_inputs): #this x is a fixed value
			ret_col = []
			for i in ls_inputs:
				if i < slow_average:
					bench_return, sys_return = Backtest_Strat.simple_momentum(frame, slow_average, i)
				else:
					sys_return = 0
				ret_col.append(sys_return)
			return ret_col

	def simple_momentum(frame, study_range: list, spacing: int):
		ls_inputs = [i for i in range(study_range[0], study_range[1], spacing)]

		def fixed_slow_average(frame, slow_average, ls_inputs): #this x is a fixed value
			ret_col = []
			for i in ls_inputs:
				if i < slow_average:
					bench_return, sys_return = Backtest_Strat.simple_momentum(frame, slow_average, i)
				else:
					sys_return = 0
				ret_col.append(sys_return)
			return ret_col

		Z = []
		for i1 in tqdm(ls_inputs):
			ret_col = fixed_slow_average(frame, i1, ls_inputs)
			Z.append(ret_col)
		return Z
