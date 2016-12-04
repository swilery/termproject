import SharedPackedParseForest

class sigmaSetItem:

    def __init__(self,node,counter, sppfNode=None):
        self.node = node
        self.counter = counter
        self.sppfNode = sppfNode

class SSet:
    DEBUG = False
    def __init__(self, num, endNode=None):
        self.callSet = {}
        self.nodeSet = {}
        self.id = num
        self.hasEndNode = endNode
        self.pathSet = {}
        
    def makeSigmaSetItem(self,node, counter, sppfNode=None):
        newSigmaSetItem = sigmaSetItem(node,counter, sppfNode)
        return newSigmaSetItem

    def insertSigmaSetItem(self,node, counter, sppfNode=None):
        key = node.value + str(counter)
        if self.nodeSet.get(key) == None: 
            sigmaItem = self.makeSigmaSetItem(node,counter, sppfNode)
            self.nodeSet[key] = sigmaItem
            if node.value == "S.":
                self.hasEndNode = key
        return sigmaItem

    def insertSigmaSetPathItem(self,node,counter,sppfNode=None):
        key = node.value + str(counter)
        if self.pathSet.get(key) == None:
            sigmaItem = self.makeSigmaSetItem(node,counter,sppfNode)
            self.pathSet[key] = sigmaItem
            
    def insertSigmaCallItem(self,node, counter,sppfNode=None):
        key = node.value + str(counter)
        if self.callSet.get(key) == None:           
            sigmaItem = self.makeSigmaSetItem(node,counter,sppfNode)
            self.callSet[key] = sigmaItem
        return sigmaItem

    def isItemInSigmaSet(self,node,counter):
        key = node.value + str(counter)
        if self.nodeSet.get(key) == None:
            return False
        return True

    def isItemInCallSet(self,node,counter):
        key = node.value + str(counter)
        if self.callSet.get(key) == None:
            return False
        return True
    
    def findEndPoints(self):
        '''
        Go through nodeSet and find all nodes whose end node
        with a counter matching it's own is not in the sigma set.
        These are the nodes we need to start search from on the next iteration
        Don't need to look through call set as any call node has an epsilon weighted
        edge to the start node, therefore, will never applicable
        '''
        initialNodes = {}
        for n in self.nodeSet:
            sigmaItem = self.nodeSet.get(n)
            sigmaNode = sigmaItem.node
            if self.DEBUG:
                print "evaluating node "+sigmaNode.value+" with counter "+str(sigmaItem.counter)
            sigmaNodeCounter = sigmaItem.counter
            noEndNode = False
            for e in sigmaNode.edges:
                end = e.endNode
                testKey = end.value + str(sigmaNodeCounter)
                if self.nodeSet.get(testKey) == None and noEndNode == False and self.callSet.get(testKey) == None:
                    if self.DEBUG:
                        print end.value+" not found. Therefore, "+sigmaNode.value+" is a starting pt"
                    initialNodes[n] = sigmaNode
                    noEndNode = True
                    # end node not in sigma set, so we want to
                    # start searching with this node 
        return initialNodes
        #return self.pathSet
        
