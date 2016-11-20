'''
A forest is a collection of trees. A tree is a special type of graph. There
will most likely be duplications of GrammarFlowGraph.py in this file. If we
have time, (most likely we won't), we can have both GFG and SPPF inherit from
a single Graph class.
'''

class NodeType:
    AND, OR, LEAF = range(3)
    table = ("AND","OR","LEAF")  #Immutable, not pun intended

class Node:
    def __init__(self,name,startPos,endPos,nodeType):
        self.name = name
        self.startPos = startPos
        self.endPos = endPos
        self.nodeType = nodeType

    def toString(self):
        s = str(self.startPos)
        e = str(self.endPos)
        t = NodeType.table[self.nodeType]
        return "<"+self.name+","+s+","+e+","+t+">"

    def printNode(self):
        print self.toString()

    def updatePos(self,newStart,newEnd):
        if newStart < self.startPos:
            self.startPos = newStart
        if newEnd > self.endPos:
            self.endPos = newEnd

class Edge:
    def __init__(self,startNode,endNode):
        self.startNode = startNode
        self.endNode = endNode

    def toString(self):
        return self.startNode.toString()+" -> "+self.endNode.toString()

    def printEdge(self):
        print self.toString()

class SPPF:
    def __init__(self):
        self.nodes = set()
        # we need to be able to look up nodes by names.
        # didn't want to delete your code in case it does this 
        self.nodeNames = {}
        '''
        This may be convoluted, but the intention is to have a dictionary in
        which each key is a node u and each value is a set of nodes v such
        that there is an edge from u to v. Intuitively, each node knows its
        outgoing neighbors. It may or may not be useful for each nodes to know
        its incoming neighbors as well.
        '''
        self.edges = {}

    def makeNode(self,name,startPos,endPos,nodeType):
        return Node(name,startPos,endPos,nodeType)

    def makeEdge(self,startNode,endNode):
        return Edge(startNode,endNode)

    def addNode(self,node):
        self.nodes.add(node)

    #again - this may be redundant. placeholder for now
    def updateNonLeafNodes(self,node):
        self.nodeNames[node.name] = node

    def addEdge(self,edge):
        if edge.startNode in self.edges:
            self.edges[edge.startNode].add(edge.endNode)
        else:
            self.edges.update({edge.startNode:{edge.endNode}})

    def printSPPF(self):
        print {n.toString() for n in self.nodes}
        # Crap, this is over 80 characters long.
        print {u.toString()+" -> "+str({v.toString() for v in vs}) for u,vs in self.edges.items()}

'''
testNode1 = Node("W",1,2,NodeType.LEAF)
testNode2 = Node("Z",1,4,NodeType.AND)
testNode3 = Node("S",4,4,NodeType.LEAF)
testEdge1 = Edge(testNode2, testNode1);
testEdge2 = Edge(testNode2, testNode3);
#testNode1.printNode()
#testEdge.printEdge()
sppf = SPPF()
sppf.addNode(testNode1)
sppf.addNode(testNode2)
sppf.addNode(testNode3)
sppf.addEdge(testEdge1)
sppf.addEdge(testEdge2)
sppf.printSPPF()
'''
