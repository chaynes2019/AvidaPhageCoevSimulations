RESET_INT=1000

./avida -s 1 -set EVENT_FILE eventsBeginCoev.cfg

rm resetSpop.spop
rm parasiteLines.txt
cp resetSpopFileMaker.py data

cd data
mkdir coevResetRun-0
mv *.spop coevResetRun-0
mv *.dat coevResetRun-0
cp resetSpopFileMaker.py coevResetRun-0
cd coevResetRun-0
echo "Running grep!"
grep horz:int detail-${RESET_INT}.spop >> parasiteLines.txt
python3 resetSpopFileMaker.py
rm parasiteLines.txt
rm resetSpopFileMaker.py
mv resetSpop.spop ../..
cd ..
cd ..

for n in {1..1};
do
    ./avida -s 1 -set EVENT_FILE eventsResetRun.cfg
    rm resetSpop.spop
    cd data
    mkdir coevResetRun-$n
    mv *.spop coevResetRun-$n
    mv *.dat coevResetRun-$n
    cp resetSpopFileMaker.py coevResetRun-$n
    cd coevResetRun-$n
    echo "Running grep!"
    grep horz:int detail-${RESET_INT}.spop >> parasiteLines.txt
    python3 resetSpopFileMaker.py
    rm parasiteLines.txt
    rm resetSpopFileMaker.py
    mv resetSpop.spop ../..
    cd ..
    cd ..
done
