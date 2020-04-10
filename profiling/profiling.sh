python3 -m cProfile -o output_profiling ../fracaSAT.py ../exemple-50-200.cnf
python3 pstats_profiling.py > result_profiling_gsat