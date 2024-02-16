import numpy as np
import sys
import matplotlib.pyplot as plt

#Retrieve numberOfResets or numberOfRounds as well as the overallRunLength from the commandline arguments
#and include resetInterval

print(sys.argv)

overallRunLength = int(sys.argv[1])
resetInterval = int(sys.argv[2])

numberOfResets = overallRunLength // resetInterval - 1
numberOfRounds = numberOfResets + 1
taskFilePreambleLines = 15

#9 tasks, overall run length divided by 100 + 1 (to account for beginning)
hostTasks = np.zeros((9, (overallRunLength // 100) + 1))
parasiteTasks = np.zeros((9, (overallRunLength // 100) + 1))


'''Open up task files
-add tasks at each timepoint to each column of container'''

for k in range(numberOfRounds):
    with open(f"../config/data/coevResetRun-{k}/host_tasks.dat", 'r') as taskFile:
        taskLines = taskFile.readlines()[taskFilePreambleLines:]
        #The first line, that of 0 updates, is wrong on resets: therefore, it is best to ignore it, especially as it
        #refers to the same time as the last line of the previous
        if (k == 0):
            linesToAdd = len(taskLines)
            offset = 0
        else:
            linesToAdd = len(taskLines) - 1
            offset = 1
        
        for n in range(linesToAdd):
            #This will not go outside of taskLines bounds when offset = 1 because linesToAdd subtracts 1
            tasks = taskLines[n + offset].split()[1:]
            #The above split uses array slicing because the first element will be the update number, and
            #that will be inaccurate for the reset peeps
            hostTasks[:, (k * resetInterval) // 100 + n] = tasks
        
    with open(f"../config/data/coevResetRun-{k}/parasite_tasks.dat", 'r') as taskFile:
        taskLines = taskFile.readlines()[taskFilePreambleLines:]
        #The first line, that of 0 updates, is wrong on resets: therefore, it is best to ignore it, especially as it
        #refers to the same time as the last line of the previous
        if (k == 0):
            linesToAdd = len(taskLines)
            offset = 0
        else:
            linesToAdd = len(taskLines) - 1
            offset = 1
        
        for n in range(linesToAdd):
            #This will not go outside of taskLines bounds when offset = 1 because linesToAdd subtracts 1
            tasks = taskLines[n + offset].split()[1:]
            print(tasks)
            #The above split uses array slicing because the first element will be the update number, and
            #that will be inaccurate for the reset peeps
            parasiteTasks[:, (k * resetInterval) // 100 + n] = tasks

numParasites = np.zeros((1, (overallRunLength // 100) + 1))

#Retrieving the number of parasites extant at each time (i.e. every 100 updates) from ParasiteData.dat
parasiteDataPreamble = 5
for k in range(numberOfRounds):
    with open(f"../config/data/coevResetRun-{k}/ParasiteData.dat", 'r') as taskFile:
        taskLines = taskFile.readlines()[parasiteDataPreamble:]
        if (k == 0):
            linesToAdd = len(taskLines)
            offset = 0
        else:
            linesToAdd = len(taskLines) - 1
            offset = 1
        
        for n in range(linesToAdd):
            #This will not go outside of taskLines bounds when offset = 1 because linesToAdd subtracts 1
            tasks = taskLines[n + offset].split()[1]
            print(tasks)
            #The above split uses array slicing because the first element will be the update number, and
            #that will be inaccurate for the reset peeps
            numParasites[0, (k * resetInterval) // 100 + n] = tasks



#print(f"Host Tasks = {hostTasks}\n")
#print(f"Parasite Tasks = {parasiteTasks}")
print(f"numParasites = {numParasites}")

avgParasiteTasks = np.zeros((9, (overallRunLength // 100) + 1))

for row in range(9):
    for col in range((overallRunLength // 100) + 1):
        if int(parasiteTasks[row, col]) == 0 and int(numParasites[0, col]) == 0:
            avgParasiteTasks[row, col] = 0.0
        else:
            avgParasiteTasks[row, col] = parasiteTasks[row, col] / numParasites[0, col]


avgNumParasiteTasks = np.array([np.sum(avgParasiteTasks[:, col]) for col in range((overallRunLength // 100) + 1)])

'''Plot host tasks together versus time,
 plot parasite tasks together versus time, 
 and then plot host and parasite together for each task'''

#A plot of host NOTs over time

plt.figure(0)
taskLabels = ['NOT',
           'NAND',
           'AND',
           'ORNOT',
           'OR',
           'ANDNOT',
           'NOR',
           'XOR',
           'EQUALS']
linePlots = []
for n in range(9):
    linePlots.append(plt.plot(np.array([k * 100 for k in range(overallRunLength // 100 + 1)]),
                              parasiteTasks[n, :],
                              label=taskLabels[n]))
    
#Makes dashed lines at reset marks
resetUpdates = [resetInterval * (k + 1) for k in range(overallRunLength // resetInterval - 1)]
upperYBound = np.max(parasiteTasks)

for x in resetUpdates:
    plt.plot(np.array([x for k in range(100)]), np.array([(upperYBound / 100) * k for k in range(100)]), 'r--')

plt.legend()
plt.title(f"Parasite Task Counts vs. Updates at Reset = {resetInterval}")
plt.savefig(f"../OutputData/ParasiteTaskCountsVsUpdatesAtReset{resetInterval}")

plt.figure(1)
plt.plot(np.array([k * 100 for k in range(overallRunLength // 100 + 1)]),
         parasiteTasks[0, :],
         label="Parasite-NOT")
plt.plot(np.array([k * 100 for k in range(overallRunLength // 100 + 1)]),
         hostTasks[0, :],
         label="Host-NOT")

#Makes dashed lines at reset marks
resetUpdates = [resetInterval * (k + 1) for k in range(overallRunLength // resetInterval - 1)]
upperYBound = np.max([np.max(parasiteTasks[0, :]), np.max(hostTasks[0,:])])
for x in resetUpdates:
    plt.plot(np.array([x for k in range(100)]), np.array([(upperYBound / 100) * k for k in range(100)]), 'r--')

plt.legend()
plt.title(f"Parasite and Host NOT counts vs. Updates at Reset = {resetInterval}")
plt.savefig(f"../OutputData/ParasiteHostNOTsVsUpdatesAtReset{resetInterval}")

plt.figure(2)
plt.plot(np.array([k * 100 for k in range(overallRunLength // 100 + 1)]),
         avgNumParasiteTasks)

#Makes dashed lines at reset marks
resetUpdates = [resetInterval * (k + 1) for k in range(overallRunLength // resetInterval - 1)]
upperYBound = max(avgNumParasiteTasks)
for x in resetUpdates:
    plt.plot(np.array([x for k in range(100)]), np.array([(upperYBound / 100) * k for k in range(100)]), 'r--')

plt.title(f"Average Number of Tasks in Parasite Genome vs. Updates at Reset = {resetInterval}")
plt.savefig(f"../OutputData/AverageNumTaksVsUpdatesAtReset{resetInterval}")
