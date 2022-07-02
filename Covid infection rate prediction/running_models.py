import machine_learning as ml
import disease_models as dm
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel('data.xlsx')
gamma = 0.1
xi = 0.1/180
time = len(data)
dt = 1
S0 = 205100
I0 = 1
R0 = 0

model = dm.model().Infected_SIRS

model_inputs = ('X', gamma, xi, time, dt, S0, I0, R0)
opt_parameter_limits = [0,1]
learning_rate = 0.000000000000001
accuracy = 0.00001
max_iteration_GD = 1000
max_iteration_SA = 200
T = 4
real_data = data.activeCases.tolist()


optimum = ml.SA_GD(real_data, 
		model, 
		model_inputs,
		opt_parameter_limits,
		learning_rate,
		accuracy,
		max_iteration_GD,
		T, 
		max_iteration_SA)

result = 638

print(optimum)

print(ml.loss().plot_MSE_parameter(real_data,model, model_inputs,1000,opt_parameter_limits))
