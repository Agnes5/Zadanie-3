#!/bin/bash

a=( 3 5 0 -2 -5 9)
b=( 3 6 -1 2 0 10)
c=( 3 5 2 3 5 11)
d=( 4 5 3 4 2 7)
e=( 4 6 0 -2 -10 10)
f=( 2 4 20 12 0 -1)
g=( 7 10 4 2 5 9)

r=( 1 0 1 1 1 1)

for ind in `seq 0 5`; do
  out=`python zadanie3neg.py ${a[$ind]} ${b[$ind]} ${c[$ind]} ${d[$ind]} ${e[$ind]} ${f[$ind]} ${g[$ind]}`
  if [ "$out" != "${r[ind]}" ]
  then
    echo "input" ${a[$ind]} ${b[$ind]} ${c[$ind]} ${d[$ind]} ${e[$ind]} ${f[$ind]} ${g[$ind]} 
    echo "output actual" $out
    echo "output expected" ${r[$ind]}
  fi
done