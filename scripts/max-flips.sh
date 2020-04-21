#! /bin/bash
echo 'TIME TABLES-------------------'
TIMEFORMAT=%U


for file in ./benchmark-folder/*
do
    printf "\n$file\n"
    for j in 500; do
      for i in 1 2 3 4 5 6 7 8 9; do
        t=$(($i*$j))
        printf "\n$t\n"
        for i in `seq 10`; do
          echo -n $(time python3 fracaSAT.py $file $t | grep user)
        done
      done
    done
done

