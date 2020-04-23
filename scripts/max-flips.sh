#! /bin/bash
TIMEFORMAT=%U
for file in cnfs/200/*
do
    printf "\n$file\n"
      for i in `seq 100`; do
        echo -n $(time python3 ./fracaSAT-$1.py $file | grep user)
      done
done


