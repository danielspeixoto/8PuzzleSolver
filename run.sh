#!/bin/bash
set -e

if [[ "$LANGUAGE" == "cpp" ]]; then
    echo "Compiling C++ solution..."
    g++ -std=c++11 -O2 main.cpp -o main
fi

echo "Solving instances..."
while read line; do
    echo "----------------"
    echo "Input: $line"
    if [[ "$LANGUAGE" == "cpp" ]]; then
        OUT=$(echo "$line" | ./main $*)
    else
        OUT=$(echo "$line" | ./a.py $*)
    fi
    echo "$OUT"
done < some_grids
