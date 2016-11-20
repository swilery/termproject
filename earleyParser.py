import sys
import GrammarFlowGraph
import SigmaSet
import codecs

class Parser:
    DEBUG = False
    DFSDEBUG = False

    def __init__(self,grammarFile,stringFile):
        self.gfg = GrammarFlowGraph.GFG(grammarFile)
        self.sigmaSets = []
        self.parse(stringFile)

    def getDot(self):
        return self.gfg.getDot()

    def isEdgeValidPath(self,nodeValue,ctr,counter,endNode):
        # Checks to see if we should traverse an edge
        # for a return node based on which sigma set its
        # call node is in
        nodeValue = self.getDot()+nodeValue[:-1]
        nodeValueKey = nodeValue+str(ctr)
        sset = {}
        if self.DEBUG:
            print "Looking for "+nodeValueKey+" in sset "+str(counter)
        while(counter>=0):
            sset = self.sigmaSets[counter]
            if sset.nodeSet.get(nodeValueKey)!= None:
                break
            counter-=1
        if counter<0:
            print "ERROR! No starting node found for "+nodeValueKey
            sys.exit()
        callSet = sset.callSet
        for callKey in callSet:
            callN = callSet.get(callKey)
            for e in callN.node.edges:
                if e.endNode.value == nodeValue:
                    returnNode = callN.node.callNode
                    if endNode.value == returnNode.value:
                        return True
        return False

    def dfsGFG(self,node,char,sset,ctr,counter):
        if self.DFSDEBUG:
            print "Evaluating node "+node.value+" with counter "+str(ctr)+" looking for "+char
        for e in node.edges:
            end = e.endNode
            if self.DFSDEBUG:
                print "Evaluating edge from "+node.value+" to "+end.value
            proceed = True
            if node.isExitNode():
                proceed = self.isEdgeValidPath(node.value,ctr,counter,end)
                if self.DFSDEBUG:
                    print node.value + "is an exit node, can we proeed? "+str(proceed)
            if not proceed:
                continue
            if e.weight != char and e.weight != "epsilon":
                if self.DFSDEBUG:
                    print "Edge has a weight "+e.weight+" but we are looking for "+char+" quitting..."
                return 0;
            else:
                # if we found our last node but we haven't found our character, don't add it to sigma set
                if char != e.weight and end.value == "S"+self.getDot():
                    return 0
                if end.callNode != None:
                    if self.DFSDEBUG:
                        print end.value + " IS a call node. Adding to call set with ctr "+str(counter)
                    sset.insertSigmaCallItem(end,counter,node,ctr)
                    ctr=counter
                else:
                    if self.DFSDEBUG:
                        print end.value + " is NOT a call node. Adding to sigma set with ctr "+str(ctr)
                    sset.insertSigmaSetItem(end,ctr,node,ctr)
                if e.weight == "epsilon":
                    if self.DFSDEBUG:
                        print "Edge weight is epsilon. Calling DFS again..."
                    '''
                    This overflows the recursion limit in Python. We need a way to
                    perform DFS without dfsGFG actually calling itself. 
                    '''
                    self.dfsGFG(end,char,sset,ctr,counter)
                else:
                    if self.DFSDEBUG:
                        print "Edge weight is "+e.weight+" which is what we are looking for. Calling DFS with epsilon"
                    # weight of edge equals char
                    self.dfsGFG(end,"epsilon",sset,ctr,counter)
        return 0;

    def parse(self,stringFile):
        start = self.gfg.startNode
        counter = 0 
        dot = self.getDot()

        #Set up our Sigma Set0 initially with the start node
        nodesToSearch = {}
        startKey = start.value + "0"
        nodesToSearch[startKey] = start
        sigmaSet = SigmaSet.SSet(0)
        sigmaSet.insertSigmaSetItem(start,counter)
        self.sigmaSets.append(sigmaSet)
        continueSearch = True

        with codecs.open(stringFile, encoding='utf-8',mode='r') as reader:
            parseString = reader.read().replace("\n", "")

        parseString = parseString.split(" ")
        parseString = [""]+parseString
        
        #iterate through characters in string to parse
        # we want to iterate while we have more characters to parse
        # and nodes in our last sigma set that need searching
        while counter < (len(parseString)) and len(nodesToSearch)>0:
            # string manipulation to adjust period and get character we are looking for
            # I just realized the bit below isn't needed
            # posString = stringFile[0:counter]+dot+stringFile[counter:]

            charToSearch = parseString[counter]
            if len(charToSearch) == 0:
                charToSearch = "epsilon"  
            #get our sigma set from our list for this iteration
                
            sigmaSet = self.sigmaSets[counter]

            for sigmaN in nodesToSearch:
                n = nodesToSearch.get(sigmaN)
                if self.DEBUG:
                    print sigmaN + " looking for " + charToSearch
                ctr = sigmaN[-1]
                self.dfsGFG(n,charToSearch,sigmaSet,ctr,counter)
               
            
            # find nodes in last sigma set with outgoing edges to nodes
            # not in our graph. These are the nodes we want to start our
            # search with next iteration
            # if the sigma set is empty, then nodesToSearch will also be empty
            # and our loop will quit
            nodesToSearch = sigmaSet.findEndPoints()

            #create sigma set for next round
            counter+=1
            sigmaSet = SigmaSet.SSet(counter)
            self.sigmaSets.append(sigmaSet)


        # if we went through the whole string, and the
        # end node is in the last sigma set
        validString = False
        last = counter - 1
        lastSigmaSet = self.sigmaSets[last]
        if counter>=len(parseString):
            end = start.endNode
            # we don't know what the associated counter with our end node is
            # therefore we need to loop through all nodes in our last sigma set
            if lastSigmaSet.hasEndNode!=None:
                validString = True
        if validString:
            # for every end node in final set, call retrace path on it
            for end in lastSigmaSet.nodeSet:
                if end[0:2] == "S.":
                    print "\nPath:\n"
                    endNode = lastSigmaSet.nodeSet.get(end)
                    self.retracePath(last,endNode)
            print "This string is valid given grammar"
            #self.debugSigmaSets(last)
        else:
            print "This string is NOT valid given grammar"

    def retracePath(self,num,endNode):
        sset = self.sigmaSets[num]
        isParent = False
        if self.gfg.graphNodes.get(endNode.node.value) != None:
            if endNode.node.value[0:2] != "S.":
                if endNode.node.value[0] == ".":
                    isParent = True
        prevValue = ""
        for nc in endNode.prevNode:
            n = nc[0]
            if n!=None:
                if n.value == prevValue:
                    continue
                else:
                    prevValue = n.value
                keyToSearch = n.value + str(nc[1])
                index = n.value.find('->')
                if isParent:
                    print "NON-LEAF NODE : "+endNode.node.value[1:]
                    print "PARENT OF PARENT NODE : "+n.value[0:index]
                if sset.nodeSet.get(keyToSearch)!=None:
                    edgeWeight = self.gfg.find_edge_weight(n,endNode.node)
                    if edgeWeight != "epsilon":
                        print "LEAF : " + edgeWeight
                        print "LEAF PARENT : "+n.value[0:index]
                    endNode = sset.nodeSet.get(keyToSearch)
                    self.retracePath(num,endNode)
                elif sset.callSet.get(keyToSearch)!=None:
                    #is this needed? will it always be epsilon
                    edgeWeight = self.gfg.find_edge_weight(n,endNode.node)
                    if edgeWeight != "epsilon":
                        print "LEAF : " + edgeWeight
                        print "LEAF PARENT : "+n.value[0:index]
                    endNode = sset.callSet.get(keyToSearch)
                    self.retracePath(num,endNode)
                else:
                    self.retracePath((num-1),endNode)

    def debugSigmaSets(self,num):
        for i in range(0,num+1):
            print "SIGMA SET "+str(i)+":"
            sset = self.sigmaSets[i]
            print "NODE SET:"
            for n in sset.nodeSet:
                print n + " from " + str(len(sset.nodeSet.get(n).prevNode)) + " other nodes"
            print "CALL SET:"
            for c in sset.callSet:
                print c
    
def main():
    if len(sys.argv) != 3:
            print "Usage: python earleyRecognizer.py grammerFile stringFile"
            sys.exit()
    grammarFile = sys.argv[1]
    stringFile = sys.argv[2]
    parser = Parser(grammarFile,stringFile)
    #parser.parse()

if __name__ == "__main__":
    sys.exit(main())
