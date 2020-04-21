# solver-race
## Outputing Graph Procedure
For outpunting the graph whe have to do it into a docker container because our OS have dependecy problems with pygraphviz. So, in orther to output the png we have to make some steps.
· First execute the following comand in order to build the docker container and running the SAT: docker build .
· If you want to modify the cnf example file containing the cnf formula, change it into Dockerfile, in the last Run File.
. Then, to get the output u have to run the following: docker cp <containerId>:app/<nameOfFile> .
· In order to get the container id run docker ps -a and search for the container.