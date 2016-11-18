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

class Edge:
    def __init__(self,startNode,endNode):
        self.startNode = startNode
        self.endNode = endNode

    def toString(self):
        return self.startNode.toString()+" -> "+self.endNode.toString()

    def printEdge(self):
        print self.toString()

testNode1 = Node("W",1,2,NodeType.LEAF)
testNode2 = Node("Z",1,4,NodeType.AND)
testEdge = Edge(testNode2, testNode1);
testNode1.printNode()
testEdge.printEdge()
