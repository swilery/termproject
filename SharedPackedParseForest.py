'''
Our SPPF Graph class
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
        self.nodeNames = {}

    def makeNode(self,name,startPos,endPos,nodeType):
        return Node(name,startPos,endPos,nodeType)

    def makeEdge(self,startNode,endNode):
        return Edge(startNode,endNode)

    def addNode(self,node):
        self.nodes.add(node)

    def updateNonLeafNodes(self,node):
        self.nodeNames[node.name] = node

    def addEdge(self,edge):
        edge.startNode.edges.append(edge)
        edge.endNode.hasIncoming = True

    #This is based off of the pseudocode in Scott's paper
    def makeNodeAdvanced(self,productionString,startPos,endPos,sppfNodew,sppfNodev,toSearch):
        #If the production is of the form B -> ax. (end of scan) we create a node named B
        #If the production is of the form B -> x.y wecreate a node named the production
        after = productionString[productionString.find('.')+1:]
        if len(after)==0:           
            s = productionString[0:productionString.find('-')]
        else:
            s = productionString
        alpha = productionString[productionString.find('>')+1:productionString.find('.')]
        alpha = alpha[0:len(alpha)-len(toSearch)]
        
        if len(after)>0 and len(alpha)==0:
            y = sppfNodev
        else:
            #First, we create the node itself, an OR node by default,
            # or find it using our dictionary
            nodeName = s + str(startPos) + str(endPos)
            y = self.nodeNames.get(nodeName)
            if y == None:              
                y = self.makeNode(nodeName,startPos,endPos,1)
                self.updateNonLeafNodes(y)
            foundV = False
            foundW = False

            '''
            Next, we check the two nodes passed in: v and w
            If neither is null, we want to check that a family (v,w) exists for our node y
            If one or more is null, we want check that the appropriate family exists for node y
            A family is identified by an AND node of the form AND+[v]+[w]

            If a family we are expecting does not exist, we create one
            
            '''
            searchString = "AND"
            if sppfNodew != None and sppfNodev != None and sppfNodew.name == sppfNodev.name:
                sppfNodew = None
            if sppfNodew != None:
                searchString = searchString + sppfNodew.name
            if sppfNodev != None:
                searchString = searchString + sppfNodev.name
            foundFamily = False
            
            for e in y.edges:
                if e.endNode.name == searchString:
                    foundFamily = True

            if not foundFamily:
                andNode = self.makeNode(searchString,startPos,endPos,0)
                andEdge = self.makeEdge(y,andNode)
                self.addEdge(andEdge)
                if sppfNodew != None:
                    wEdge = self.makeEdge(andNode,sppfNodew)
                    self.addEdge(wEdge)
                if sppfNodev != None:
                    vEdge = self.makeEdge(andNode,sppfNodev)
                    self.addEdge(vEdge)
        return y
         
        
    def printSPPF(self,root):
        data = self.printNodeInfo(root)
        print "Nodes:"
        for d in data[0]:
            print d
        print "\n\nEdges:"
        for e in data[1]:
            print e

    def printNodeInfo(self,node):
        visited, queue = set(), [node]
        edges = set()
        while queue:
            treeNode = queue.pop(0)
            if treeNode.toString() not in visited:
                visited.add(treeNode.toString())
                for e in treeNode.edges:
                    queue.append(e.endNode)
                    edges.add(e.startNode.toString() + "->" + e.endNode.toString())
        return [visited, edges]
