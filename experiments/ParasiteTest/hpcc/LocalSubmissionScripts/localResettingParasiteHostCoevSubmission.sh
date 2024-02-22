OVERALL_RUN_LENGTH=2000
RESET_INTERVAL=2000
HPCC=0

cd ../UtilityScripts
python3 eventsConfigFileMaker.py ${OVERALL_RUN_LENGTH} ${RESET_INTERVAL} ${HPCC}

cd ../config

./avida -s 30 -set EVENT_FILE eventsBeginCoev.cfg >> log_0.txt

rm resetSpop.spop
rm parasiteLines.txt

cd data
mkdir coevResetRun-0
mv *.spop coevResetRun-0
mv *.dat coevResetRun-0
cp ../../UtilityScripts/resetSpopFileMaker.py coevResetRun-0
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

TOTAL_ROUNDS=$((${OVERALL_RUN_LENGTH} / ${RESET_INTERVAL}))
let NUM_RESET_ROUNDS=TOTAL_ROUNDS-1


for (( n=1; n<=NUM_RESET_ROUNDS; n++ ))
do
    echo "Entering reset round ${n}"
    ./avida -s 30 -set EVENT_FILE eventsResetRun.cfg >> log_${n}.txt
    rm resetSpop.spop
    cd data
    mkdir coevResetRun-${n}
    mv *.spop coevResetRun-${n}
    mv *.dat coevResetRun-${n}
    cp ../../UtilityScripts/resetSpopFileMaker.py coevResetRun-${n}
    cd coevResetRun-${n}
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

cd data
mkdir logFiles
cd ..

mv log_*.txt data/logFiles

cd ../AnalysisScripts
python3 phenotypeTasksGetter.py ${OVERALL_RUN_LENGTH} ${RESET_INTERVAL}
