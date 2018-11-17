#!/bin/bash
# 1: trainset filename containing graphs // aido100.txt
# 2: active graph IDs filename // ca.txt
# 3: inactive graph IDs filename //ci.txt
# 4: testset filename containing graphs // aidotest.txt
mkdir data
python3 encode.py $1 $2 $3 $4