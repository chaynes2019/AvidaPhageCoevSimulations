OVERALL_RUN_LENGTH=10000
RESET_INTERVAL=5000

cd ../config

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
