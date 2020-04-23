#!/usr/bin/env python3
import sys

import networkx
import pygraphviz
import fracaSAT
import random


# Classes

class Node:

    def __init__(self, num):
        self.num


class CNF():
    """A CNF formula randomly generated"""

    def __init__(self, num_nodes, edge_prob, num_colors):
        """
        Initialization
        num_nodes: Number of nodes
        edge_prob: Edge probability between two nodes
        num_colors: Number of colors to color the graph
        clauses: List of clauses
        """
        self.num_nodes = num_nodes
        self.edge_prob = edge_prob
        self.num_colors = num_colors
        self.clauses = []
        self.gen_node_clauses()
        self.gen_edge_clauses()

    def gen_node_clauses(self):
        '''Generate the ALO + AMO clauses for all the nodes'''
        for n in range(self.num_nodes):
            # ALO
            var1 = n * self.num_colors + 1
            self.clauses.append([i for i in range(var1, var1 + self.num_colors)])
            # AMO
            for v1 in range(var1, var1 + self.num_colors - 1):
                for v2 in range(v1 + 1, var1 + self.num_colors):
                    self.clauses.append([-v1, -v2])

    def gen_edge_clauses(self):
        '''Generates the clauses for each pair of nodes that have an edge with certain prob'''
        for n1 in range(self.num_nodes - 1):
            for n2 in range(n1 + 1, self.num_nodes):
                if random.random() < self.edge_prob:
                    var1 = n1 * self.num_colors + 1
                    var2 = n2 * self.num_colors + 1
                    for c in range(self.num_colors):
                        self.clauses.append([-(var1 + c), -(var2 + c)])

    def show(self):
        """Prints the formula to the stdout"""
        sys.stdout.write("c Random CNF formula\n")
        sys.stdout.write("p cnf %d %d\n" % (self.num_nodes * self.num_colors, len(self.clauses)))
        for c in self.clauses:
            sys.stdout.write("%s 0\n" % " ".join(map(str, c)))


# Main
def create_dict_color(inter, num_nodes, num_colors):
    current_node = 1
    graph = {}
    for n in range(num_nodes):
        crange = inter[(n)*num_colors:((n+1)*num_colors)]
        co = list(filter(lambda x: x > 0, crange))[0]
        graph[n+1]= co 
    return graph


def get_edges(num_nodes, num_colors, clauses):
    num_min_color = num_nodes
    num_max_colors = int(num_colors * (num_colors - 1) / 2)
    start = num_nodes + num_nodes * num_max_colors
    return list(map(lambda x: [int((abs(x[0])-1) / num_colors + 1), int((abs(x[1])- 1) / num_colors + 1)], clauses[start:]))


def get_random_color():
    random_number = random.randint(0, 16 ** 6 - 1)
    hex_number = str(hex(random_number))[2:]
    return f'#{hex_number}'


def create_graph(colors, edges, output_file):
    G = networkx.Graph(ranksep='0.5')
    for node in colors:
        G.add_node(f'{node}: {colors[node]}')
    for edge in edges:
        n1 = abs(edge[0])
        n2 = abs(edge[1])
        G.add_edge(f'{n1}: {colors[n1]}', f'{n2}: {colors[n2]}')
    A = networkx.nx_agraph.to_agraph(G)
    A.node_attr['style'] = 'filled'
    A.node_attr['width'] = '0.1'
    A.node_attr['height'] = '0.1'
    A.edge_attr['color'] = '#000000'
    color = '#000000'
    current_colors = ['#000000']
    for node in colors:
        while color in current_colors:
            color = get_random_color()
        current_colors.append(color)
        A.get_node(f'{node}: {colors[node]}').attr['fillcolor'] = color
    A.layout()
    A.draw("out.png", format='png')

def correct_usage():
    print("Correct USAGE:")
    print("\t./fracasat-graph-col.py <output-file> <cnf-file> <num-nodes> <num-colors>")
    print("or")
    print("\t./fracasat-graph-col.py <output-file> <num-nodes> <edge-prob> <num-colors> [random-seed]")
    sys.exit()

def main():
    if len(sys.argv) > 4:
        print("AAAA")
        output_file = sys.argv[1]
    else:
        correct_usage()
    if len(sys.argv) == 5 and not sys.argv[2].isdigit():
        cnf_file = sys.argv[2]
        num_nodes = int(sys.argv[3])
        num_colors = int(sys.argv[4])
        fracasat = fracaSAT.get_formula(cnf_file)
        clauses = fracasat.clauses
    elif len(sys.argv) >= 5 or len(sys.argv) <= 6:
        num_nodes = int(sys.argv[2])
        edge_prob = float(sys.argv[3])
        num_colors = int(sys.argv[4])
        seed = None
        if len(sys.argv) == 6:
            seed = int(sys.argv[5])
        random.seed(seed)
        cnf = CNF(num_nodes, edge_prob, num_colors)
        #cnf.show()
        fracasat = fracaSAT.from_clauses(cnf.num_nodes * cnf.num_colors, cnf.clauses)
        clauses = cnf.clauses
    else:
        correct_usage()
    inter = fracaSAT.solver_structure(fracasat, fracaSAT.random_walk_gsat, 0.5)
    fracaSAT.show_inter(inter)
    colors = create_dict_color(inter, num_nodes, num_colors)
    edges = get_edges(num_nodes, num_colors, clauses)
    print(colors, edges)
    create_graph(colors, edges, output_file)




if __name__ == "__main__":
    main()
