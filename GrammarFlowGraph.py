import re

class Node:
#    edges = []

    def __init__(self,node,name):
        self.endNode = node
        self.value = name

class Edge:
    def __init__(self,start,end,value):
        self.startNode = start
        self.endNode = end
        self.weight = value

class GFG:
    dot = "."

    def __init__(self):
        self.startNode = None
        self.graphNodes = {}

    def make_node(self,node,name):
        newNode = Node(node,name)
        return newNode

    def make_edge(self,start,end,value):
        newEdge = Edge(start,end,value)
    # add edge to list of outgoing edges in start node
#    start.edges.append(newEdge);
        return newEdge

    def build(self,grammarFile):
        with open(grammarFile,"r") as reader:
            for production in reader:
                production = production.replace(" ","")
                preNodes = re.split("->|[|]|\n",production)
                '''
                The last element of preNodes is the empty string. We don't want it so
                let's pop it.
                '''
                preNodes.pop()
                nonterminal = preNodes[0]
                nonterminalStart = self.dot+nonterminal
                nonterminalEnd = nonterminal+self.dot

                if len(nonterminal) > 1:
                    print "Error with production "+preNodes
            
                if self.graphNodes.get(nonterminalStart) == None:
                    newEndNode = self.make_node(None,nonterminalEnd)
                    newStartNode = self.make_node(newEndNode,nonterminalStart)
                    self.graphNodes[nonterminalEnd] = newEndNode
                    self.graphNodes[nonterminalStart] = newStartNode
                else:
                    newStartNode = self.graphNodes.get(nonterminalStart)
                    newEndNode = newStartNode.endNode
        
#        if nonterminalStart == "S"+dot:
            #Need to keep track of first node
#            startNode = newStartNode
            
                print "Start node: "+newStartNode.value
                print "End node: "+newEndNode.value
                print "Production: "+str(preNodes)
        
                for i in range(1,len(preNodes)):
                    print "\tEvaluating "+preNodes[i]
                    prevNode = newStartNode
                    #The [1:] gets rid of the leading period
                    productionString = newStartNode.value[1:]+"->"+self.dot+preNodes[i]

                    newNode = self.make_node(None,productionString)
                    newEdge = self.make_edge(prevNode,newNode,"epsilon")

                    print "\t created node "+productionString
                    print "\t created edge from "+prevNode.value+" to "+newNode.value+" weighted epsilon"
                    counter = 0;
                    for c in preNodes[i]:
                        prevNode = newNode
                
                        productionString = newStartNode.value[1:]+"->"+preNodes[i][0:counter]+c+self.dot+preNodes[i][counter+1:]
                        newNode = self.make_node(None,productionString)
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
                            ntStart = self.dot+c
                            ntEnd = c+self.dot
                            nonTerminalStartNode = self.graphNodes.get(ntStart)
                            if nonTerminalStartNode == None:
                                nonTerminalEndNode = self.make_node(None,ntEnd)
                                nonTerminalStartNode = self.make_node(nonTerminalEndNode,ntStart)
                                print "\t created non-terminal start node "+ntStart
                                print "\t created non-terminal end node "+ntEnd
                                self.graphNodes[ntStart] = nonTerminalStartNode
                                self.graphNodes[ntEnd] = nonTerminalEndNode
                            else:
                                nonTerminalEndNode = self.graphNodes.get(ntEnd)
                            newStartEdge = self.make_edge(prevNode,nonTerminalStartNode,"epsilon")
                            newEndEdge = self.make_edge(nonTerminalEndNode,newNode,"epsilon")
                            print "\t created edge from "+prevNode.value+" to "+nonTerminalStartNode.value+" weighted epsilon"
                            print "\t created edge from "+nonTerminalEndNode.value+" to "+newNode.value+" weighted epsilon"
                        else:
                            newEdge = self.make_edge(prevNode,newNode,c)
                            print "\t created edge from "+prevNode.value+" to "+newNode.value+" weighted "+c
                    
                    endEdge = self.make_edge(newNode,newEndNode,"epsilon")
                    print "\t created edge from "+newNode.value+" to "+newEndNode.value+" weighted epsilon"
                    print "\tFinished evaluating "+preNodes[i]+"\n"
