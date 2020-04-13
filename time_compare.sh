#! /bin/bash
echo 'TIME TABLES-------------------'
TIMEFORMAT=%U
for file in ./cnfs/*
do
    echo $file
    echo $(time python3 fracaSAT.py $file | grep user) 
done