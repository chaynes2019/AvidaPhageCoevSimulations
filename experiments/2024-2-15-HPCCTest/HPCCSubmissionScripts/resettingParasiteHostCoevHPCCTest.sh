#!/bin/bash
# The interpreter used to execute the script


#SBATCH --job-name=parasiteHostCoevTest
#SBATCH --mail-user=clhaynes@umich.edu
#SBATCH --mail-type=BEGIN,END
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=1000m 
#SBATCH --time=00-10:00:00
#SBATCH --account=zamanlh0
#SBATCH --partition=standard
#SBATCH --output=/home/%u/%x-%j.log

USERNAME=clhaynes
EXPERIMENT_ID=2024-2-15-HPCCTest
OUTPUT_DIR=/scratch/zamanlh_root/zamanlh0/${USERNAME}/${EXPERIMENT_ID}
CONFIG_DIR=/home/${USERNAME}/Documents/AvidaPhageCoevSimulations/experiments/${EXPERIMENT_ID}/config
#SEED_OFFSET=2100

#SEED=$((SEED_OFFSET + SLURM_ARRAY_TASK_ID - 1))
#JOB_ID=${SLURM_ARRAY_TASK_ID}
RUN_DIR=${OUTPUT_DIR}

mkdir -p ${RUN_DIR}
cd ${RUN_DIR}
mkdir AnalysisScripts
mkdir config

cd ${CONFIG_DIR}
cp * ${RUN_DIR}/config
cd ../AnalysisScripts
cp * ${RUN_DIR}/AnalysisScripts

cd ${RUN_DIR}/config

OVERALL_RUN_LENGTH=72000
RESET_INTERVAL=24000

./avida -s 30 -set EVENT_FILE eventsBeginCoev.cfg

rm resetSpop.spop
rm parasiteLines.txt

cd data
mkdir coevResetRun-0
mv *.spop coevResetRun-0
mv *.dat coevResetRun-0
cp ../resetSpopFileMaker.py coevResetRun-0
cd coevResetRun-0
echo "Running grep!"
grep horz:int detail-${RESET_INTERVAL}.spop >> parasiteLines.txt
grep div detail-${RESET_INTERVAL}.spop >> hostLines.txt
python3 resetSpopFileMaker.py
rm parasiteLines.txt
rm hostLines.txt
rm resetSpopFileMaker.py
mv resetSpop.spop ../..
cd ..
cd ..

TOTAL_ROUNDS=$(($OVERALL_RUN_LENGTH / $RESET_INTERVAL))
let NUM_RESET_ROUNDS=TOTAL_ROUNDS-1


for (( n=1; n<=NUM_RESET_ROUNDS; n++ ))
do
    echo "Entering reset round $n"
    ./avida -s 30 -set EVENT_FILE eventsResetRun.cfg
    rm resetSpop.spop
    cd data
    mkdir coevResetRun-$n
    mv *.spop coevResetRun-$n
    mv *.dat coevResetRun-$n
    cp ../resetSpopFileMaker.py coevResetRun-$n
    cd coevResetRun-$n
    echo "Running grep!"
    grep horz:int detail-${RESET_INTERVAL}.spop >> parasiteLines.txt
    grep div detail-${RESET_INTERVAL}.spop >> hostLines.txt
    python3 resetSpopFileMaker.py
    rm parasiteLines.txt
    rm hostLines.txt
    rm resetSpopFileMaker.py
    mv resetSpop.spop ../..
    cd ..
    cd ..
done

cd ../AnalysisScripts
python3 taskGetter.py ${OVERALL_RUN_LENGTH} ${RESET_INTERVAL}
