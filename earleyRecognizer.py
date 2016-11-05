import re
import sys

startNode = None
graphNodes = {}

class Node:
    endNode = None
    edges = []
    value = ""

    def __init__(self,node,name):
        self.endNode = node
        self.value = name

def make_node(node,name):
    newNode = Node(node,name)
    return newNode

class Edge:
    startNode = None
    endNode = None
    weight = ""
    
    def __init__(self,start,end,value):
        self.startNode = start
        self.endNode = end
        self.weight = value

def make_edge(start,end,value):
    newEdge = Edge(start,end,value)
    # add edge to list of outgoing edges in start node
    start.edges.append(newEdge);
    return newEdge

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
        nonterminal = preNodes[0]
        nonterminalStart = "."+nonterminal
        nonterminalEnd = nonterminal+"."

        if len(nonterminal) > 1:
            print "Error with production "+preNodes
            
        #for preNode in preNodes:
           #print preNode
           #for i in range(len(preNode)):
               #print i
            
        if graphNodes.get(nonterminalStart) == None:
            newEndNode = make_node(None,nonterminalEnd)
            newStartNode = make_node(newEndNode,nonterminalStart)
            graphNodes[nonterminalEnd] = newEndNode
            graphNodes[nonterminalStart] = newStartNode
        else:
            newStartNode = graphNodes.get(nonterminalStart)
            newEndNode = newStartNode.endNode
        
        if nonterminalStart == "S.":
            #Need to keep track of first node
            startNode = newStartNode
            
        print "Start node: "+newStartNode.value
        print "End node: "+newEndNode.value
        print "Production: "
        print preNodes
        print "\n"
        
        for i in range(1,len(preNodes)):
            print "\tEvaluating "+preNodes[i]
            prevNode = newStartNode
            #The [1:] gets rid of the leading period
            productionString = newStartNode.value[1:] + "->." + preNodes[i]

            newNode = make_node(None,productionString)
            newEdge = make_edge(prevNode,newNode,"epsilon")

            print "\t created node "+productionString
            print "\t created edge from "+prevNode.value+" to "+newNode.value+" weighted epsilon"
            counter = 0;
            for c in preNodes[i]:
                prevNode = newNode
                
                productionString = newStartNode.value[1:] + "->"+preNodes[i][0:counter]+c+"."+preNodes[i][counter+1:]
                newNode = make_node(None,productionString)
                counter+=1
                print "\t created node "+productionString

                '''

                If the string is a non-terminal:
                
                   Find the start and end nodes for that non-terminal
                   Create them if they don't exist
                   Add an edge from prevNode to your new non terminal start node
                   Add an edge from your new non terminal end node to Node B

                Otherwise
                
                    Add an edge from prevNode to Node B weighted c
                    
                '''
                if c.isupper():
                    ntStart = "."+c
                    ntEnd = c+"."
                    nonTerminalStartNode = graphNodes.get(ntStart)
                    if nonTerminalStartNode == None:
                        nonTerminalEndNode = make_node(None,ntEnd)
                        nonTerminalStartNode = make_node(nonTerminalEndNode,ntStart)
                        print "\t created non-terminal start node "+ntStart
                        print "\t created non-terminal end node "+ntEnd
                        graphNodes[ntStart] = nonTerminalStartNode
                        graphNodes[ntEnd] = nonTerminalEndNode
                    else:
                        nonTerminalEndNode = graphNodes.get(ntEnd)
                    newStartEdge = make_edge(prevNode,nonTerminalStartNode,"epsilon")
                    newEndEdge = make_edge(nonTerminalEndNode,newNode,"epsilon")
                    print "\t created edge from "+prevNode.value+" to "+nonTerminalStartNode.value+" weighted epsilon"
                    print "\t created edge from "+nonTerminalEndNode.value+" to "+newNode.value+" weighted epsilon"
                else:
                    newEdge = make_edge(prevNode,newNode,c)
                    print "\t created edge from "+prevNode.value+" to "+newNode.value+" weighted "+c
                    
            endEdge = make_edge(newNode,newEndNode,"epsilon")
            print "\t created edge from "+newNode.value+" to "+newEndNode.value+" weighted epsilon"
            print "\tFinished evaluating "+preNodes[i]+"\n"
            
