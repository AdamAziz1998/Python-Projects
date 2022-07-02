import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class model:

	def SIR(self, beta, gamma, time, dt, S0, I0, R0):
		N = S0 + I0 + R0
		S = np.zeros(time)
		I = np.zeros(time)
		R = np.zeros(time)
		S[0] = S0
		I[0] = I0
		R[0] = R0


		for i in range(time -1):
			S[i + 1] = S[i] - (beta * I[i] * S[i] / N)
			I[i + 1] = I[i] + (beta * S[i] * I[i] / N) - (gamma * I[i])
			R[i + 1] = R[i] + (gamma * I[i])

		simul = pd.DataFrame({'Susceptible' : S, 'Infected' : I, 'Removed': R})
		return simul[::dt]

	def SIRS(self, 
		beta : float, 
		gamma : float, 
		xi : float, 
		time : int, 
		dt : int, 
		S0 : int, 
		I0 : int, 
		R0 : int):
		N = S0 + I0 + R0
		S = np.zeros(int(time))
		I = np.zeros(int(time))
		R = np.zeros(int(time))
		S[0] = S0
		I[0] = I0
		R[0] = R0


		for i in range(time -1):
			S[i + 1] = S[i] - (beta * I[i] * S[i] / N) + (xi * R[i])
			I[i + 1] = I[i] + (beta * S[i] * I[i] / N) - (gamma * I[i])
			R[i + 1] = R[i] + (gamma * I[i]) - (xi * R[i])

		simul = pd.DataFrame({'Susceptible' : S, 'Infected' : I, 'Removed': R})
		return simul[::dt]

	# bets is now a time based vector with a length corresponding to time
	def vector_SIRS(self, 
		beta : list, 
		gamma : float, 
		xi : float, 
		S0 : int, 
		I0 : int, 
		R0 : int):
		S = [S0]
		I = [I0]
		R = [R0]
		for k in range(len(beta)):
			df = self.SIRS(beta[k],
				gamma = gamma,
				xi = xi,
				time = 1,
				dt = 1,
				S0 = S[-1],
				I0 = I[-1],
				R0 = R[-1])
			S += df.Susceptible.tolist()
			I += df.Infected.tolist()
			R += df.Removed.tolist()

		simul = pd.DataFrame({'Susceptible' : S, 'Infected' : I, 'Removed': R})
		return simul

	def Infected_SIRS(self, beta, gamma, xi, time, dt, S0, I0, R0):
		simul = self.SIRS(beta, gamma, xi, time, dt, S0, I0, R0)
		return simul.Infected

	def Infected_vector_SIRS(self, 
		beta : list, 
		gamma : float, 
		xi : float, 
		S0 : int, 
		I0 : int, 
		R0 : int):
		simul = self.vector_SIRS(beta, gamma, xi, S0, I0, R0)
		return simul.Infected

class local_SIRS:
	def __init__(self, location, susceptible, infections, removed):
		self.location = location
		self.S = susceptible
		self.I = infections
		self.R = removed
	pass
#Steps
# 1 find perfect infection rates using SA and GD with the vectorised model
# 2 create the interactivity matrix modle (try and use a class that uses objects and apply this to 1 matrix of each area)
# 3 create some graphs to represent the data