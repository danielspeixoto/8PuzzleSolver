#!/bin/bash
set -e

echo "Compiling C++ solution..."
g++ -std=c++11 main.cpp -o main

echo "Generating all grids..."
g++ -std=c++11 gen.cpp -o gen
./gen > all_grids

echo "Starting comparison..."
while read line; do
    echo "Input: $line"
    OUT1=$(echo "$line" | ./main)
    echo "Output 1: $OUT1"
    OUT2=$(echo "$line" | python3 main.py simple_output)
    echo "Output 2: $OUT2"
    if [[ "$OUT1" != "$OUT2" ]]; then
        echo "Difference found!"
        exit 1
    fi
done < all_grids
