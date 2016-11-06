class sigmaSetItem:

    def __init__(self,node,counter):
        self.node = node
        self.counter = counter

class SSet:

    def __init__(self, num):
        self.callSet = {}
        self.nodeSet = {}
        self.id = num

    def makeSigmaSetItem(self,node, counter):
        newSigmaSetItem = sigmaSetItem(node,counter)
        return newSigmaSetItem

    def insertSigmaSetItem(self,node, counter):
        sigmaItem = self.makeSigmaSetItem(node,counter)
        key = node.value + str(counter)
        self.nodeSet[key] = sigmaItem

    def insertSigmaCallItem(self,node, counter):
        sigmaItem = self.makeSigmaSetItem(node,counter)
        key = node.value + str(counter)
        self.callSet[key] = sigmaItem

    def findEndPoints(self):
        '''
        Go through nodeSet and find all nodes whose end node
        with a counter matching it's own is not in the sigma set.
        These are the nodes we need to start search from on the next iteration
        Don't need to look through call set as any call node has an epsilon weighted
        edge to the start node, therefore, will never applicable
        '''
        initialNodes = []
        for n in self.nodeSet:
            sigmaItem = self.nodeSet.get(n)
            sigmaNode = sigmaItem.node
            sigmaNodeCounter = sigmaItem.counter
            noEndNode = False
            for e in sigmaNode.edges:
                end = e.endNode
                testKey = end.value + str(sigmaNodeCounter)
                if self.nodeSet.get(testKey) == None and noEndNode == False:
                    initialNodes.append(sigmaNode)
                    noEndNode = True
                    # end node not in sigma set, so we want to
                    # start searching with this node 
        return initialNodes
