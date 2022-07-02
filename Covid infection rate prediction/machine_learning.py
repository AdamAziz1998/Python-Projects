import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class loss:
	def MSE_row(self, testing_val, predicted_val):
		return (testing_val - predicted_val)**2

	def MSE(self, df): 
		#this will be a pandas dataframe of testing data and predicted data as its columns

		df['test_pred_diff'] = df.apply(lambda x : self.MSE_row(x.real_data, x.predicted_data), axis = 1)
		return df.test_pred_diff.sum()

	#this function allows for the flexible changing of a functions input to save rewriting code for new developments
	#an 'X' will go in the 'inputs' input so value can take its place later 
	def arbitrary_func_input(self, func : 'func', inputs : tuple, value):
		inputs = list(inputs)
		inputs[inputs.index('X')] = value
		inputs = tuple(inputs)
		output = func(*inputs)
		return output

	def nested_MSE_func(self, op, func, inputs, real_data):
				simul = self.arbitrary_func_input(func, inputs, op)
				MSE_df = pd.DataFrame({'real_data' : real_data, 'predicted_data' : simul})
				error = self.MSE(MSE_df)
				return error

	def plot_MSE_parameter(self, 
		real_data : list,
		model : 'function, output = series', 
		model_inputs : tuple, # There will be a str 'X' where the changing paramter will be
		res : int,
		paramter_limits : list):

		df = pd.DataFrame()
		MSE_df = pd.DataFrame(columns = ['MSE'])
		df['real_data'] = real_data

		for i in range(res):
			value = (((i + 1) / res) * (paramter_limits[1] - paramter_limits[0])) + paramter_limits[0]
			model_vals = self.arbitrary_func_input(model, model_inputs, value)
			df['predicted_data'] = model_vals.tolist()
			MSE = self.MSE(df)
			MSE_df = MSE_df.append({'MSE' : MSE}, ignore_index = True)
		MSE_df.MSE.plot()
		plt.show()
		

class gradient_decent:

	#in inputs place an 'X' on the parameter we are differentiating by
	#in parameter input the point at which we want to find the gradient
	#h is a small float
	def differential(self, func : 'func', inputs : tuple, parameter : float, h : float):

		numerator = loss().arbitrary_func_input(func, inputs, parameter + h) - loss().arbitrary_func_input(func, inputs, parameter)
		denominator = h

		return numerator / denominator



	#Model will have to return a list of results
	def GD(self,
		real_data : list, 
		model : 'func', 
		model_inputs : tuple,
		opt_parameter_limits : list, #list contains maximum and minimum values
		op0 : float,				 #initial optimizing parameter value
		learning_rate : float,
		accuracy : float,
		max_iteration : int):
		#model inputs will have all the inputs in place, the optimizing paramter will be labeled as "X"

		
		op = op0
		old_op = opt_parameter_limits[1] + 1

		iteration = 0
		while abs(op - old_op) > accuracy and max_iteration != iteration:
			class_loss = loss()
			diff_error = self.differential(class_loss.nested_MSE_func, ('X', model, model_inputs, real_data), op, 0.00000000001)

			old_op = op
			step = learning_rate * diff_error

			if op - step <= opt_parameter_limits[1] and op - step >= opt_parameter_limits[0]:
				op = op - step
			else:
				if op - step > opt_parameter_limits[1]:
					op = opt_parameter_limits[1]
				else:
					op = opt_parameter_limits[0]

			iteration += 1

		return op

class simulated_annealing:
	def neighbor(self, x, scale, opt_parameter_limits):
		prop = x + np.random.normal() * scale
		while prop < opt_parameter_limits[0] or prop > opt_parameter_limits[1]:
			prop = x + np.random.normal() * scale
		return prop

	def SA(self, 
 		real_data : list,
		model : 'func',
		model_inputs : tuple,
		opt_parameter_limits : list, #list contains maximum and minimum values
		T : float, 
		max_iterations : int):


		scale = np.sqrt(T)
		x = (opt_parameter_limits[1] - opt_parameter_limits[0]) * np.random.rand() + opt_parameter_limits[0]

		class_loss = loss()
		sol = class_loss.nested_MSE_func(x, model, model_inputs, real_data)
		history = [x]
		i = 0

		while i < max_iterations:
			i += 1
			prop = self.neighbor(x, scale, opt_parameter_limits)

			y = class_loss.nested_MSE_func(prop, model, model_inputs, real_data)

			if np.log(np.random.rand()) > (sol - y) / T:
				x = prop
				continue

			#updating values
			x = prop
			sol = y
			T *= 0.9

			history.append(x)
		return history[-1]

def SA_GD(real_data : list, 
		model : 'func', 
		model_inputs : tuple,
		opt_parameter_limits : list, #list contains maximum and minimum values
		learning_rate : float,
		accuracy : float,
		max_iteration_GD : int,
		T : float, 
		max_iteration_SA : int):
	
	SA_val = simulated_annealing().SA(real_data,
		model,
		model_inputs,
		opt_parameter_limits,
		T,
		max_iteration_SA)

	GD_val = gradient_decent().GD(real_data,
		model,
		model_inputs,
		opt_parameter_limits,
		SA_val,
		learning_rate,
		accuracy,
		max_iteration_GD)
	return GD_val