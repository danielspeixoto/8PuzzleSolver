#!/bin/bash
set -e

echo "Compiling C++ solution..."
g++ -std=c++11 -O2 main.cpp -o main

echo "Solving instances..."
while read line; do
    echo "----------------"
    echo "Input: $line"
    OUT=$(echo "$line" | ./main $*)
    echo "$OUT"
done < some_grids
