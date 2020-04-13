
for i in 75 100 125 150 175 200 220 280 300 320 330 340 350; do
  prove=""
  SAT="SATISFIABLE"
  ./rnd-cnf-gen.py 75 $i 3 > cnfs/exemple-75-$i.cnf
  prove=$(./minisat benchmark-folder/exemple-75-$i.cnf 2>&1 /dev/null | grep SATISFIABLE)
done

