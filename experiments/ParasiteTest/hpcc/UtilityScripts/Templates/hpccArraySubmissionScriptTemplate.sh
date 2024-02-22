#!/bin/bash
# The interpreter used to execute the script


#SBATCH --job-name=$experimentName
#SBATCH --mail-user=$uniqname@umich.edu
#SBATCH --mail-type=BEGIN,END
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=500m 
#SBATCH --time=$timeString
#SBATCH --account=zamanlh0
#SBATCH --partition=standard
#SBATCH --output=/home/%u/%x-%j.log
#SBATCH --array=1-$numReplicates

USERNAME=$uniqname
EXPERIMENT_ID=$date-$experimentName

SEED_OFFSET=30

PROJECT_HOME_DIR=/home/$${USERNAME}/Documents/AvidaPhageCoevSimulations

mkdir -p experiments/$${EXPERIMENT_ID}

OUTPUT_DIR=/scratch/zamanlh_root/zamanlh0/$${USERNAME}/$${EXPERIMENT_ID}
TEMPLATE_DIR=$${PROJECT_HOME_DIR}/experiments/ParasiteHostCoevHPCCTemplate

SEED=$$((SEED_OFFSET + SLURM_ARRAY_TASK_ID - 1))
JOB_ID=${SLURM_ARRAY_TASK_ID}
RUN_DIR=${OUTPUT_DIR}/${JOB_ID}

mkdir -p $${RUN_DIR}
cd $${RUN_DIR}

cd $${TEMPLATE_DIR}

cp -r * $${RUN_DIR}

cd $${RUN_DIR}/config

OVERALL_RUN_LENGTH=$overallRunLength
RESET_INTERVAL=$resetInterval
HPCC=$hpcc

cd ../UtilityScripts
python3 eventsConfigFileMaker.py $${OVERALL_RUN_LENGTH} $${RESET_INTERVAL} $${HPCC}

cd ../config

./avida -s $${SEED} -set EVENT_FILE eventsBeginCoev.cfg >> log_0.txt

rm resetSpop.spop
rm parasiteLines.txt

cd data
mkdir coevResetRun-0
mv *.spop coevResetRun-0
mv *.dat coevResetRun-0
cp ../../UtilityScripts/resetSpopFileMaker.py coevResetRun-0
cd coevResetRun-0
echo "Running grep!"
grep horz:int detail-$${RESET_INTERVAL}.spop >> parasiteLines.txt
grep div detail-$${RESET_INTERVAL}.spop >> hostLines.txt
python3 resetSpopFileMaker.py
rm parasiteLines.txt
rm hostLines.txt
rm resetSpopFileMaker.py
mv resetSpop.spop ../..
cd ..
cd ..

TOTAL_ROUNDS=$$(($${OVERALL_RUN_LENGTH} / $${RESET_INTERVAL}))
let NUM_RESET_ROUNDS=TOTAL_ROUNDS-1


for (( n=1; n<=NUM_RESET_ROUNDS; n++ ))
do
    echo "Entering reset round $${n}"
    ./avida -s $${SEED} -set EVENT_FILE eventsResetRun.cfg >> log_$${n}.txt
    rm resetSpop.spop
    cd data
    mkdir coevResetRun-$${n}
    mv *.spop coevResetRun-$${n}
    mv *.dat coevResetRun-$${n}
    cp ../../UtilityScripts/resetSpopFileMaker.py coevResetRun-$${n}
    cd coevResetRun-$${n}
    echo "Running grep!"
    grep horz:int detail-$${RESET_INTERVAL}.spop >> parasiteLines.txt
    grep div detail-$${RESET_INTERVAL}.spop >> hostLines.txt
    python3 resetSpopFileMaker.py
    rm parasiteLines.txt
    rm hostLines.txt
    rm resetSpopFileMaker.py
    mv resetSpop.spop ../..
    cd ..
    cd ..
done

cd data
mkdir logFiles
cd ..

mv log_*.txt data/logFiles

cd ../AnalysisScripts
python3 phenotypeTasksGetter.py $${OVERALL_RUN_LENGTH} $${RESET_INTERVAL}

cp -r ../OutputData $${PROJECT_HOME_DIR}/experiments/$${EXPERIMENT_ID}

cp -r ../config/data/logFiles $${PROJECT_HOME_DIR}/experiments/$${EXPERIMENT_ID}