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
        self.hasIncoming = False
        self.edges = []

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
        # using the edges dict won't work here as that will only pick up
        # nodes with outgoing edges (aka not leaves)
        self.nodeNames = {}
        
        '''
        This may be convoluted, but the intention is to have a dictionary in
        which each key is a node u and each value is a set of nodes v such
        that there is an edge from u to v. Intuitively, each node knows its
        outgoing neighbors. It may or may not be useful for each nodes to know
        its incoming neighbors as well.

        I removed this. It is more helpful for each node to keep a list of its outgoing edges
        and keep the dictionary of node names. (I think). I am open to reverting this back though.
        '''

    def makeNode(self,name,startPos,endPos,nodeType):
        return Node(name,startPos,endPos,nodeType)

    def makeEdge(self,startNode,endNode):
        return Edge(startNode,endNode)

    def addNode(self,node):
        self.nodes.add(node)

    #again - this may be redundant. placeholder for now
    # TODO: should be a list in the event of multiple nodes with the same name
    # i don't think this will work for recursive grammars currently
    def updateNonLeafNodes(self,node):
        self.nodeNames[node.name] = node

    def addEdge(self,edge):
        edge.startNode.edges.append(edge)
        '''
        if edge.startNode in self.edges:
            self.edges[edge.startNode].add(edge.endNode)
        else:
            self.edges.update({edge.startNode:{edge.endNode}})
        '''
        edge.endNode.hasIncoming = True

    #TODO: add and nodes / "families"
    def makeNodeAdvanced(self,productionString,startPos,endPos,sppfNodew,sppfNodev,toSearch):
        after = productionString[productionString.find('.')+1:]
        if len(after)==0:
            s = productionString[0:productionString.find('-')]
        else:
            s = productionString
        alpha = productionString[productionString.find('>')+1:productionString.find('.')]
        alpha = alpha[0:alpha.find(toSearch)]
        if len(after)>0 and len(alpha)==0:
            y = sppfNodev
        else:
            nodeName = s + str(startPos) + str(endPos)
            y = self.nodeNames.get(nodeName)
            if y == None:
                print "Created "+ nodeName
                y = self.makeNode(nodeName,startPos,endPos,1)
                self.updateNonLeafNodes(y)
            else:
                print "Accessed node "+y.name
            foundV = False
            foundW = False
            if sppfNodew == None:
                for e in y.edges:
                    if e.endNode.name == sppfNodev.name:
                        foundV = True
                if not foundV:
                    e = self.makeEdge(y,sppfNodev)
                    self.addEdge(e)
            else:
                for e in y.edges:
                    if sppfNodev != None:
                        if e.endNode.name == sppfNodev.name:
                            foundV = True
                    if e.endNode.name == sppfNodew.name:
                        foundW = True
                #TODO: check if none?
                if not foundV and sppfNodev != None:
                    print "\tAdded child "+sppfNodev.name
                    e = self.makeEdge(y,sppfNodev)
                    self.addEdge(e)
                if not foundW:
                    if (sppfNodev != None and sppfNodew.name != sppfNodev.name) or sppfNodev==None:
                        print "\tAdded child "+sppfNodew.name
                        e = self.makeEdge(y,sppfNodew)
                        self.addEdge(e)
        return y
         
        
    def printSPPF(self,root):
        print {n.toString() for n in self.nodes}
        #self.printNodeInfo(root)
        # Crap, this is over 80 characters long.
        #print {u.toString()+" -> "+str({v.toString() for v in vs}) for u,vs in self.edges.items()}

    #Since I switched edges to be a list by node
    # We can use a recursive function to print out the tree info
    def printNodeInfo(self,node):
        print "Looking at "+node.name
        print node.name + " has " + str(len(node.edges)) + " children"
        for e in node.edges:
            print e.endNode.toString()
            #self.printNodeInfo(e.endNode)
            print e.endNode.name + " has " + str(len(e.endNode.edges)) + " children"
            for v in e.endNode.edges:
                print "here" + v.endNode.toString()
        if len(node.edges)>0:
            print "End of children for "+node.name

    def findNode(self,root,node):
        if root.name == node.name and root.startPos == node.startPos and root.endPos == root.endPos:
            return root
        for e in root.edges:
            endNode = e.endNode
            found = self.findNode(endNode,node)
            if found != None:
                return found
        return None
