class sigmaSetItem:

    def __init__(self,node,counter):
        self.node = node
        self.counter = counter

class SSet:

    def __init__(self, num):
        self.callSet = {}
        self.nodeSet = {}
        self.id = num

    def makeSigmaSetItem(node, counter):
        newSigmaSetItem = sigmaSetItem(node,counter)
        return newSigmaSetItem

    def insertSigmaSetItem(node, counter):
        sigmaItem = self.makeSigmaSetItem(node,counter)
        self.nodeSet[node.value] = sigmaItem

    def insertSigmaCallItem(node, counter):
        sigmaItem = self.makeSigmaSetItem(node,counter)
        self.callSet[node.value] = sigmaItem

    
