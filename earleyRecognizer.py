import re
import sys

class Node:
    pass

class Edge:
    pass

if len(sys.argv) != 3:
    print "Usage: python earleyRecognizer.py grammerFile stringFile"
    sys.exit()

grammarFile = sys.argv[1]
stringFile = sys.argv[2]

with open(grammarFile, 'r') as reader:
    for production in reader:
        production = production.replace(' ', '')
        preNodes = re.split('->|[|]|\n', production)
        '''
        The last element of preNodes is the empty string. We don't want it so
        let's pop it.
        '''
        preNodes.pop()
        #nonterminal = preNodes[0];
        nodes = set()
        for preNode in preNodes:
            for i in range(len(preNode)):
                node = preNode[:i] + '.' + preNode[i:]
                nodes.add(node)
            nodes.add(preNode + '.')
        print preNodes
        print nodes
