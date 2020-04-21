#! /bin/bash
echo 'TIME TABLES-------------------'
TIMEFORMAT=%U


for file in ./benchmark-folder/*
do
    printf "\n$file\n"
    for j in 200; do
      for i in {10..35}; do
        t=$(($i*$j))
        printf "\n$t\n"
        for i in `seq 50`; do
          echo -n $(time python3 fracaSAT.py $file $t | grep user)
        done
      done
    done
done

