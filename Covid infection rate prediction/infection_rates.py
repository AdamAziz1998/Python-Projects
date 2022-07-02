# This file will carry out calculations to find the infection rate of different models
# The different models can be found in disease_models

import disease_models as dm
import machine_learning as ml



class beta_vals:
	def __init__(self,
		real_data : 'series',
		population : int,
		learning_rate : float,
		accuracy : float,
		max_iteration_GD : int,
		T : float,
		max_iteration_SA : float):

		self.real_data = real_data
		self.learning_rate = learning_rate
		self.accuracy = accuracy
		self.max_iteration_GD = max_iteration_GD
		self.T = T
		self.max_iteration_SA = max_iteration_SA

		self.opt_parameter_limits = [0,1]

		#the pre-imposed inputs for the models below
		self.gamma = 0.1
		self.xi = 0.1/180
		self.time = len(self.real_data)
		self.dt = 1
		self.S0 = population
		self.I0 = self.real_data.iloc[0]
		self.R0 = 0

	def SA_GD(self,
		model : 'func', 
		model_inputs : tuple):
	
		self.SA_val = simulated_annealing().SA(self.real_data,
			model,
			model_inputs,
			self.opt_parameter_limits,
			self.T,
			self.max_iteration_SA)

		GD_val = gradient_decent().GD(self.real_data,
			model,
			model_inputs,
			self.opt_parameter_limits,
			self.SA_val,
			self.learning_rate,
			self.accuracy,
			self.max_iteration_GD)
		return GD_val

	def beta_SIRS(self):
		model = dm.model().SIRS


		model_inputs = ('X',
			self.gamma,
			self.xi,
			self.time,
			self.dt,
			self.S0,
			self.I0,
			self.R0)

		opt_beta = self.SA_GD(model, model_inputs)

		return opt_bate

	def beta_vector_SIRS(self):
		model = dm.model().SIRS

		self.time = 1
		self.betas = []

		for k in range(len(beta)):

			model_inputs = ('X',
				self.gamma,
				self.xi,
				self.time,
				self.dt,
				self.S0,
				self.I0,
				self.R0)

			opt_beta = SA_GD(model, model_inputs)
			self.betas.append(opt_beta)

			self.S0, self.I0, self.R0 = dm.model().SIRS(opt_beta,
				self.gamma,
				self.xi,
				self.time,
				self.dt,
				self.S0,
				self.I0,
				self.R0)

		return betas



				






