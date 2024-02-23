import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

experiment1 = input("Enter the name of Experiment 1: ")
experiment2 = input("Enter the name of Experiment 2: ")
overallRunLength = input("How many updates were the experiments run for?: ")

experiment1TasksDataframe = pd.read_csv(f"experiments/{experiment1}/OutputData/{experiment1}-AverageNumTasksVsUpdates.csv")
experiment2TasksDataframe = pd.read_csv(f"experiments/{experiment2}/OutputData/{experiment2}-AverageNumTasksVsUpdates.csv")
'''
experiment1LengthDataframe = pd.read_csv(f"experiments/{experiment1}/OutputData/{experiment1}-avgParasiteGenomeLengthVsUpdates.csv")
experiment2LengthDataframe = pd.read_csv(f"experiments/{experiment2}/OutputData/{experiment2}-avgParasiteGenomeLengthVsUpdates.csv")
'''
experiment1Tasks = experiment1TasksDataframe.to_numpy()
experiment2Tasks = experiment2TasksDataframe.to_numpy()

print(f"Tasks in experiment 1: {experiment1Tasks}")


#experiment1Lengths = experiment1LengthDataframe.to_numpy()
#experiment2Lengths = experiment2LengthDataframe.to_numpy()


plt.figure(0)
plt.plot(np.array([k * 100 for k in range(int(overallRunLength) // 100 + 1)]),
         experiment1Tasks[:, 1], label="Reset Interval = 24000")
plt.plot(np.array([k * 100 for k in range(int(overallRunLength) // 100 + 1)]),
         experiment2Tasks[:, 1], label="No Reset Control")
plt.legend()
'''
plt.figure(1)
plt.plot(np.array([k * 100 for k in range(overallRunLength // 100 + 1)]),
         experiment1Lengths, experiment2Lengths)
'''
plt.savefig("AvgNumTasksVsUpdatesExperimentVsControl")


