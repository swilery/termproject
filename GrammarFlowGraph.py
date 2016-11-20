import re
import codecs

class Node:
    # if a node is a call node with a return,
    # we want to treat that differently than
    # start/end nodes of a non-terminal
    # is there a better way to structure this?
    def __init__(self,node,name,callN):
        self.endNode = node
        self.callNode = callN
        self.value = name
        self.edges = set()

    def isExitNode(self):
        if self.value[-1] == "." and len(self.value)==2:
            return True
        else:
            return False

class Edge:
    def __init__(self,start,end,value):
        self.startNode = start
        self.endNode = end
        self.weight = value

class GFG:
    dot = "."
    DEBUG = False
    EPSILON = unichr(949)

    def __init__(self,grammarFile):
        self.startNode = None
        self.graphNodes = {}
        self.build(grammarFile)

    def getDot(self):
        return self.dot

    def make_node(self,node,name):
        newNode = Node(node,name,None)
        return newNode

    def make_edge(self,start,end,value):
        newEdge = Edge(start,end,value)
        # add edge to list of outgoing edges in start node
        start.edges.add(newEdge);
        return newEdge

    def find_edge_weight(self,start,end):
        for e in start.edges:
            if e.endNode.value == end.value:
                return e.weight
        return "epsilon"

    def dbPrint(*args):
        argsLength = len(args)
        if argsLength == 2:
            print "\t\tCreated Node: "+args[1]
        elif argsLength == 4:
            print "\t\tCreated Edge: ("+args[1]+", "+args[2]+")"
            print "\t\t\t\tWeight: "+args[3]
        else:
            print "dbPrint() was passed an invalid number of arguments"

    def build(self,grammarFile):
        with codecs.open(grammarFile, encoding='utf-8',mode='r') as reader:
            for production in reader:
                #production = production.replace(" ","")
                preNodes = re.split("->|[|]|\n",production)
                '''
                The last element of preNodes is the empty string. We don't want
                it so let's pop it.
                '''
                preNodes.pop()
                preNodes = map(lambda s: s.strip(), preNodes)
                preNodes = map(lambda s: s.split(), preNodes)
                #print preNodes
                nonterminal = preNodes[0][0]
                nonterminalStart = self.dot+nonterminal
                nonterminalEnd = nonterminal+self.dot
           
                if self.graphNodes.get(nonterminalStart) == None:
                    newEndNode = self.make_node(None,nonterminalEnd)
                    newStartNode = self.make_node(newEndNode,nonterminalStart)
                    if self.DEBUG:
                        self.dbPrint(nonterminalStart)
                        self.dbPrint(nonterminalEnd)
                    self.graphNodes[nonterminalEnd] = newEndNode
                    self.graphNodes[nonterminalStart] = newStartNode
                else:
                    newStartNode = self.graphNodes.get(nonterminalStart)
                    newEndNode = newStartNode.endNode
        
                if nonterminalStart == self.dot+"S":
                    #Need to keep track of first node
                    self.startNode = newStartNode
            
                if self.DEBUG:
                    print "Production: "+str(preNodes)
        
                for i in range(1,len(preNodes)):
                    if self.DEBUG:
                        print "\tBegin Evaluating "+preNodes[i][0]
                    prevNode = newStartNode
                    #The [1:] gets rid of the leading period
                    productionString = [newStartNode.value[1:]]+["->"]+[self.dot]+preNodes[i][0:]
                    productionString = ''.join(productionString)
                    newNode = self.make_node(None,productionString)
                    newEdge = self.make_edge(prevNode,newNode,"epsilon")

                    if self.DEBUG:
                        self.dbPrint(productionString)
                        self.dbPrint(prevNode.value, newNode.value, "epsilon")

                    counter = 0;
                    for c in preNodes[i]:
                        
                        prevNode = newNode
                        charlist = [c, self.dot]
                        productionString = [newStartNode.value[1:]]+["->"]+preNodes[i][0:counter]+charlist+preNodes[i][counter+1:]
                        productionString = ''.join(productionString)
                        newNode = self.make_node(None,productionString)
                        counter+=1

                        if self.DEBUG:
                            self.dbPrint(productionString)

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
                                if self.DEBUG:
                                    self.dbPrint(ntStart)
                                    self.dbPrint(ntEnd)
                                self.graphNodes[ntStart] = nonTerminalStartNode
                                self.graphNodes[ntEnd] = nonTerminalEndNode
                            else:
                                #nonTerminalEndNode = self.graphNodes.get(ntEnd)
                                nonTerminalStartNode = self.graphNodes.get(ntStart)
                                nonTerminalEndNode = nonTerminalStartNode.endNode
                            newStartEdge = self.make_edge(prevNode,nonTerminalStartNode,"epsilon")
                            newEndEdge = self.make_edge(nonTerminalEndNode,newNode,"epsilon")
                            # since this means prevNode and newNode are call/return blocks
                            # we will add a ref to new node in prev node
                            prevNode.callNode = newNode
                            if self.DEBUG:
                                self.dbPrint(prevNode.value, nonTerminalStartNode.value, "epsilon")
                                self.dbPrint(nonTerminalEndNode.value, newNode.value, "epsilon")
                        else:
                            if c==self.EPSILON:
                                c = "epsilon"
                            newEdge = self.make_edge(prevNode,newNode,c)
                            if self.DEBUG:
                                self.dbPrint(prevNode.value, newNode.value, c)
                    
                    endEdge = self.make_edge(newNode,newEndNode,"epsilon")
                    if self.DEBUG:
                        self.dbPrint(newNode.value, newEndNode.value, "epsilon")
                        print "\tFinished Evaluating "+preNodes[i][0]+"\n" 
