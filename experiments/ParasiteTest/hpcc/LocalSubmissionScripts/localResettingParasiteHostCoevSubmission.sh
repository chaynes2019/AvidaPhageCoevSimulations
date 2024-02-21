OVERALL_RUN_LENGTH=14000
RESET_INTERVAL=3500
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
mv parasiteLines.txt parasiteLines0.txt
mv hostLines.txt hostLines0.txt
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
    mv resetSpop.spop resetSpop$n.spop
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
    mv parasiteLines.txt parasiteLines$n.txt
    rm hostLines.txt hostLines$n.txt
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
