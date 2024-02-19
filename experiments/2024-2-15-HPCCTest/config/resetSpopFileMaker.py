import numpy as np

parasitePositions = []
with open('parasiteLines.txt', 'r') as f:
    parasiteLines = f.readlines()
    for parasite in parasiteLines:
        parasiteEnumerated = parasite.split()
        if (len(parasiteEnumerated) >= 18):
            #print(parasite)
            #This parasite is still extant because it has some data on what cells it's present at
            positions = parasiteEnumerated[17]
            #Parses string of multiple positions for the parasite genotypes with multiple copies
            for position in positions.split(','):
                parasitePositions.append(position)
            #This parasite is extinct, and thus it shouldn't be included or else it... well, am I right?
                
hostPositions = []
with open('hostLines.txt', 'r') as f:
    hostLines = f.readlines()
    for host in hostLines:
        hostEnumerated = host.split()
        if (len(hostEnumerated) >= 18):
            #print(parasite)
            #This parasite is still extant because it has some data on what cells it's present at
            positions = hostEnumerated[17]
            #Parses string of multiple positions for the parasite genotypes with multiple copies
            for position in positions.split(','):
                hostPositions.append(int(position))
            #This parasite is extinct, and thus it shouldn't be included or else it... well, am I right?

hostPositions = sorted(hostPositions)
#print(hostPositions)
#print(parasiteLines)

preamble = []
with open('detail-500.spop', 'r') as f:
    for k in range(24):
        preamble.append(f.readline())

#print(preamble)

numberOfParasites = len(parasitePositions)
#print(numberOfParasites)
with open('resetSpop.spop', 'w') as f:
    f.writelines(preamble)
    f.writelines(["\n"])
    for k in range(len(hostPositions)):
        hostPositions[k] = str(hostPositions[k])
    
    gestationOffsetAndLineageLabels = ["0" for k in range(len(hostPositions))]
    hostlines = ["1 div:ext (none) (none) 0 1 320 0 0 0 0 -1 -1 0 2 transsmt ycdAoaddxccccccccccccccEEEcccccccccccccccccccccccccccccccccccccccccccccccccccgccccccccccccccccccccccccccccccccccccccccEccccDcccccccccccccccccccccccccccccccccccccccccccccccccccdccccccccccccccccccccccccccccccccccccccccccxcccccccccccccccccccccccccccccccccccccccccccccccccAcccccccccccccccccccucccccccccccccccccccccypqvcrGxab \n".format(",".join(hostPositions), ",".join(gestationOffsetAndLineageLabels), ",".join(gestationOffsetAndLineageLabels))]
    hostlines.append("2 div:int (none) 1 {} {} 320 0 0 0 0 -1 -1 0 2 transsmt ycdAoaddxccccccccccccccEEEcccccccccccccccccccccccccccccccccccccccccccccccccccgccccccccccccccccccccccccccccccccccccccccEccccDcccccccccccccccccccccccccccccccccccccccccccccccccccdccccccccccccccccccccccccccccccccccccccccccxcccccccccccccccccccccccccccccccccccccccccccccccccAcccccccccccccccccccucccccccccccccccccccccypqvcrGxab {} {} {} \n".format(len(hostPositions), len(hostPositions), ",".join(hostPositions), ",".join(gestationOffsetAndLineageLabels), ",".join(gestationOffsetAndLineageLabels)))

    f.writelines(hostlines)
    f.writelines(parasiteLines)

extraPositions = [pos for pos in parasitePositions if pos not in hostPositions]
print(f"Parasites without a home: {extraPositions}")