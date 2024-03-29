from string import Template
import numpy as np

inputCheck = True

uniqname = input("Uniqname: ")

date = input("Date (in MM-DD-YYYY format): ")

overallRunLength = input("Overall Run Length (in updates): ")

resetInterval = input("Reset Interval (in updates): ")

hpcc = input("Is this on the Great Lakes HPCC? (answer 1 for yes; 0 for no): ")
hpccBool = bool(int(hpcc))

if hpccBool:
    experimentName = input("Experiment Name: ")

    replicates = input("How many replicates? : ")
    numReplicates = int(replicates)

    time = (3.2 / 20000) * int(overallRunLength)
    time = int(np.ceil(time))
    if(time >= 24):
        print("You may have to rethink how long this will take")
        inputCheck = False

    timeString = f"00-{time}:00:00"

if hpccBool:
    if numReplicates > 1:
        arraySubmissionScriptTemplateName = "Templates/hpccArraySubmissionScriptTemplate.sh"

        with open(arraySubmissionScriptTemplateName, 'r') as templateFile:
            templateString = templateFile.read()
            arraySubmissionScriptTemplate = Template(templateString)
        
        arraySubmissionScript = arraySubmissionScriptTemplate.substitute(uniqname = uniqname, 
                                                                         date = date, 
                                                                         overallRunLength = overallRunLength,
                                                                         resetInterval = resetInterval,
                                                                         hpcc = hpcc,
                                                                         experimentName = experimentName,
                                                                         numReplicates = numReplicates,
                                                                         timeString = timeString)
        
        with open('../../../runHPCCResetExperiment.sh', 'w') as f:
            f.write(arraySubmissionScript)

    else:
        singleSubmissionScriptTemplateName = "Templates/hpccSingleSubmissionScriptTemplate.sh"

        with open(singleSubmissionScriptTemplateName, 'r') as templateFile:
            templateString = templateFile.read()
            singleSubmissionScriptTemplate = Template(templateString)
        
        singleSubmissionScript = singleSubmissionScriptTemplate.substitute(uniqname = uniqname, 
                                                                         date = date, 
                                                                         overallRunLength = overallRunLength,
                                                                         resetInterval = resetInterval,
                                                                         experimentName = experimentName,
                                                                         hpcc = hpcc,
                                                                         timeString = timeString)
        
        with open('../../../runHPCCResetExperiment.sh', 'w') as f:
            f.write(singleSubmissionScript)

else:    
    submissionScriptTemplateName = "Templates/runResettingParasiteHostCoevTemplate.sh"

    with open(submissionScriptTemplateName, 'r') as templateFile:
        templateString = templateFile.read()
        submissionScriptTemplate = Template(templateString)

    submissionScript = submissionScriptTemplate.substitute(overallRunLength = overallRunLength, resetInterval = resetInterval, hpcc = hpcc)

    with open("/home/hytendf/Projects/AvidaPhageCoevSimulations/experiments/ParasiteTest/hpcc/LocalSubmissionScripts/localResettingParasiteHostCoevSubmission.sh", 'w') as f:
        f.write(submissionScript)


