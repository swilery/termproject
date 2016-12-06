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
        self.pathSet = {}
        
    def makeSigmaSetItem(self,node, counter, sppfNode=None):
        newSigmaSetItem = sigmaSetItem(node,counter, sppfNode)
        return newSigmaSetItem

    def insertSigmaSetItem(self,node, counter, sppfNode=None):
        key = node.value + str(counter)
        if self.nodeSet.get(key) == None: 
            sigmaItem = self.makeSigmaSetItem(node,counter, sppfNode)
            self.nodeSet[key] = sigmaItem
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
        
