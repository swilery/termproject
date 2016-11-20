class sigmaSetItem:

    def __init__(self,node,counter, prevNode=None, prevCounter=0):
        self.node = node
        self.counter = counter
        self.prevNode = [[prevNode,prevCounter]]

class SSet:
    DEBUG = False
    def __init__(self, num, endNode=None):
        self.callSet = {}
        self.nodeSet = {}
        self.id = num
        self.hasEndNode = endNode
        
    def makeSigmaSetItem(self,node, counter, prevNode=None, prevCounter=0):
        newSigmaSetItem = sigmaSetItem(node,counter, prevNode, prevCounter)
        return newSigmaSetItem

    def insertSigmaSetItem(self,node, counter, prevNode=None, prevCounter=0):
        key = node.value + str(counter)
        if self.nodeSet.get(key) == None: 
            sigmaItem = self.makeSigmaSetItem(node,counter, prevNode, prevCounter)
            self.nodeSet[key] = sigmaItem
            if node.value == "S.":
                self.hasEndNode = key
        elif prevNode != None:
            self.nodeSet.get(key).prevNode.append([prevNode,prevCounter])


    def insertSigmaCallItem(self,node, counter,prevNode=None, prevCounter=0):
        key = node.value + str(counter)
        if self.callSet.get(key) == None:           
            sigmaItem = self.makeSigmaSetItem(node,counter,prevNode, prevCounter)
            self.callSet[key] = sigmaItem
        elif prevNode != None:
            self.callSet.get(key).prevNode.append([prevNode,prevCounter])

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
