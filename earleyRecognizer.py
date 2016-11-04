import re
import sys

'''
The GFG is made up of nodes and edges. I think it will be useful to have each
node and edge be an instance of a class. Currently, these classes are unused.
'''
class Node:
    def __init__(self, name):
        self.name = name

    def printNode(self):
        print self.name

class Edge:
    pass

if len(sys.argv) != 3:
    print "Usage: python earleyRecognizer.py grammerFile stringFile"
    sys.exit()

nodes = set()

def constructNodes(preNodes):
    for preNode in preNodes:
        for i in range(len(preNode)):
            node = preNode[: i] + dot + preNode[i :]
            nodes.add(node)
        nodes.add(preNode + dot)

grammarFile = sys.argv[1]
stringFile = sys.argv[2]
nonterminals = set()
dot = '.'
productions = []
edges = {}

with open(grammarFile, 'r') as reader:
    for production in reader:
        production = production.replace(' ', '')
        preNodes = re.split('->|[|]|\n', production)
        '''
        The last element of preNodes is the empty string. We don't want it so
        let's pop it.
        '''
        preNodes.pop()
        print 'preNodes: ' + str(preNodes)
        productions.append(preNodes)
        nonterminals.add(preNodes[0])
        constructNodes(preNodes)

'''
Currently this does not produce correct edges because this doesn't take into
account call/return edges. We can check for call/return edges by checking
whether the next character is in nonterminals.
'''
for production in productions:
    nonterminal = production[0]
    startNode = dot + nonterminal
    for preNode in production:
        for i in range(len(preNode)):
            u = preNode[: i] + dot + preNode[i :]
            v = preNode[: i + 1] + dot + preNode[i + 1 :] 
            edges.update({u : v})

print 'nonterminals: ' + str(nonterminals)
print 'nodes: ' + str(nodes)
print 'productions: ' + str(productions)
print 'edges: ' + str(edges)

