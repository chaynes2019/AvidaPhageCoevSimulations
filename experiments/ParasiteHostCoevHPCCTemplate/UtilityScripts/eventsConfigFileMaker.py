from string import Template
import sys

overallRunLength = sys.argv[1]
resetInterval = sys.argv[2]
hpcc = bool(int(sys.argv[3]))
print(hpcc)

beginCoevTemplateName = "Templates/eventsBeginCoevTemplate.cfg"

with open(beginCoevTemplateName, 'r') as templateFile:
    templateString = templateFile.read()
    beginCoevConfig = Template(templateString)

    if hpcc:
        injectionTime = 2000
    else:
        injectionTime = 500

    #First injectionTime/resetInterval refers to the variable in the template, second one to the local variable
    newBeginCoevConfigFile = beginCoevConfig.substitute(injectionTime = injectionTime, resetInterval = resetInterval)
    

with open("../config/eventsBeginCoev.cfg", 'w') as f:
    f.write(newBeginCoevConfigFile)

resetCoevTemplateName = "Templates/eventsResetRunTemplate.cfg"

with open(resetCoevTemplateName, 'r') as templateFile:
    templateString = templateFile.read()
    resetCoevConfig = Template(templateString)

    #First injectionTime/resetInterval refers to the variable in the template, second one to the local variable
    newResetCoevConfigFile = resetCoevConfig.substitute(injectionTime = injectionTime, resetInterval = resetInterval)

with open("../config/eventsResetRun.cfg", 'w') as f:
    f.write(newResetCoevConfigFile)


