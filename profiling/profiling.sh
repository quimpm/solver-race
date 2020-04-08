python3 -m cProfile -o output_profiling ../fracaSAT.py exemple_trofollo.cnf
python3 pstats_profiling.py > result_profiling