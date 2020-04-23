
for i in {20..42}; do
  prove=""
  SAT="SATISFIABLE"
  a=$((200*$i/10))
  ./rnd-cnf-gen.py 200 $a 3 > cnfs/200/exemple-200-$a.cnf
  prove=$(./minisat cnfs/200/exemple-200-$a.cnf 2>&1 /dev/null | grep SATISFIABLE)
done

