
for i in {40..85}; do
  prove=""
  SAT="SATISFIABLE"
  a=$(($i*10))
  ./rnd-cnf-gen.py 200 $i 3 > cnfs/200/exemple-200-$a.cnf
  prove=$(./minisat cnfs/200/exemple-200-$a.cnf 2>&1 /dev/null | grep SATISFIABLE)
done

