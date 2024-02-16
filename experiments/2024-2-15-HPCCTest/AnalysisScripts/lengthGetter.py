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

parasiteLengths = np.zeros((1, (overallRunLength // 100) + 1))



'''Open up task files
-add tasks at each timepoint to each column of container'''

for k in range(numberOfRounds):
    for n in range(resetInterval // 100):
        with open(f"data/coevResetRun-{k}/parasiteGenome_list.{n * 100}", 'r') as lengthFile:
            genomeLines = lengthFile.readlines()
            #The first line, that of 0 updates, is wrong on resets: therefore, it is best to ignore it, especially as it
            #refers to the same time as the last line of the previous
            sum = 0
            for line in genomeLines:
                sum += len(line)
            
            avg = sum / len(genomeLines)

            parasiteLengths[k * (resetInterval // 100) + n] = avg