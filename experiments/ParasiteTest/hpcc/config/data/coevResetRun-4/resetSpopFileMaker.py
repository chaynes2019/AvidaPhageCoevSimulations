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
    hostlines = ["1 div:ext (none) (none) 0 1 320 0 0 0 0 -1 -1 0 2 transsmt ycdAoaddxccccccccccccccEEEcccccccccccccccccccccccccccccccccccccccccccccccccccgccccccccccccccccccccccccccccccccccccccccEccccDcccccccccccccccccccccccccccccccccccccccccccccccccccdccccccccccccccccccccccccccccccccccccccccccxcccccccccccccccccccccccccccccccccccccccccccccccccAcccccccccccccccccccucccccccccccccccccccccypqvcrGxab 0 0 0 \n"]
    for k in range(3600):
        hostlines.append("{} div:int (none) {} 1 1 320 0 0 0 0 -1 -1 0 2 transsmt ycdAoaddxccccccccccccccEEEcccccccccccccccccccccccccccccccccccccccccccccccccccgccccccccccccccccccccccccccccccccccccccccEccccDcccccccccccccccccccccccccccccccccccccccccccccccccccdccccccccccccccccccccccccccccccccccccccccccxcccccccccccccccccccccccccccccccccccccccccccccccccAcccccccccccccccccccucccccccccccccccccccccypqvcrGxab {} 0 0 \n".format(k + 2, k + 1, k))
    f.writelines(hostlines)
    f.writelines(parasiteLines)
