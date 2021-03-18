# final-project-theoracle

## Data Generation
```
cd pin-3.18*/source/tools/ManualExamples
make all TARGET=intel64
../../../pin -t obj-intel64/pinatrace.so -- <FakePath>/pipesim -i <FakePath>/traces/instruction1.txt
```

## Execution Instructions

**Execution Command:**
```
python3 ./comparePredictors.py --history 7
```

**Help**
```
usage: comparePredictors.py [-h] [--history {2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20}]
Local Value Predictor
optional arguments:
-h, --help show this help message and exit
--history {2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20}
                         history length
```