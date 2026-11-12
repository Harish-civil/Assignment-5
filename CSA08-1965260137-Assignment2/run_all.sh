#!/usr/bin/env bash
# Runs every task and stores console output in each folder's output.txt
for q in Q1 Q2 Q3 Q4 Q5 Q6 Q7; do
  (cd $q && python3 $(ls q*.py) | tee output.txt)
done
