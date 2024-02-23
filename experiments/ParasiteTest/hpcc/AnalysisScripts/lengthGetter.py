import numpy as np
import sys
import matplotlib.pyplot as plt
import pandas as pd

#Retrieve numberOfResets or numberOfRounds as well as the overallRunLength from the commandline arguments
#and include resetInterval

print(sys.argv)

overallRunLength = int(sys.argv[1])
resetInterval = int(sys.argv[2])
experimentID = sys.argv[3]

numberOfResets = overallRunLength // resetInterval - 1
numberOfRounds = numberOfResets + 1

#There is no parasite genome length data for update 0
parasiteLengths = np.zeros((overallRunLength // 100))



'''Open up task files
-add tasks at each timepoint to each column of container'''

for k in range(numberOfRounds):
    for n in range((resetInterval // 100)):
        #n + 1 is used because there is no parasite_genome_list.0.dat; we still want
        #the correct number of length measurements, though
        with open(f"../config/data/coevResetRun-{k}/parasite_genome_list.{(n + 1) * 100}.dat", 'r') as lengthFile:
            genomeLines = lengthFile.readlines()
            
            sum = 0
            for line in genomeLines:
                sum += len(line)
            
            if len(genomeLines) > 0:
                avg = sum / len(genomeLines)
            else:
                avg = 0

            parasiteLengths[k * (resetInterval // 100) + n] = avg

plt.figure(0)
plt.plot(np.array([(n + 1) * 100 for n in range(overallRunLength // 100)]), parasiteLengths)

resetUpdates = [resetInterval * (k + 1) for k in range(overallRunLength // resetInterval - 1)]
upperYBound = max(parasiteLengths)
for x in resetUpdates:
    plt.plot(np.array([x for k in range(100)]), np.array([(upperYBound / 100) * k for k in range(100)]), 'r--')

plt.title(f"Average Length of Parasite Genome vs. Updates at Reset = {resetInterval}")
plt.savefig(f"../OutputData/avgParasiteGenomeLengthVsUpdates")

print(parasiteLengths)

parasiteLengthsDataframe = pd.DataFrame(parasiteLengths)
parasiteLengthsDataframe.to_csv(f"../OutputData/{experimentID}-avgParasiteGenomeLengthVsUpdates.csv")