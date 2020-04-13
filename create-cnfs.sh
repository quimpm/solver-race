
for i in 25 50 75 100 125 150 175 200 225 250; do
  prove=""
  SAT="SATISFIABLE"
  while [ "$prove" != "$SAT" ]; do
    ./rnd-cnf-gen.py 50 $i 3 > "cnfs/exemple-50-$i.cnf"
    prove=$(./minisat benchmark-folder/exemple-75-320.cnf 2>&1 /dev/null | grep SATISFIABLE)
  done
done

