import sys
import GrammarFlowGraph
import SigmaSet
import SharedPackedParseForest
import codecs

class Parser:
    DEBUG = False
    DFSDEBUG = False

    def __init__(self,grammarFile,stringFile):
        self.gfg = GrammarFlowGraph.GFG(grammarFile)
        self.sigmaSets = []
        self.tree = SharedPackedParseForest.SPPF()
        self.parseTrees = []
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
        sset = self.sigmaSets[int(str(ctr))]
        if sset.nodeSet.get(nodeValueKey)== None:
            print "ERROR! No start key found for "+nodeValueKey
            sys.exit()
        callSet = sset.callSet
        for callKey in callSet:
            callN = callSet.get(callKey)
            for e in callN.node.edges:
                if e.endNode.value == nodeValue:
                    returnNode = callN.node.callNode
                    if endNode.value == returnNode.value:
                        return callN.counter
        return None

    def dfsGFG(self,node,char,sset,ctr,counter):
        if self.DFSDEBUG:
            print "Evaluating node "+node.value+" with counter "+str(ctr)+" looking for "+char
        for e in node.edges:
            end = e.endNode
            #if self.DFSDEBUG:
                #print "Evaluating edge from "+node.value+" to "+end.value
            proceed = True
            if node.isExitNode():
                proceed = self.isEdgeValidPath(node.value,ctr,counter,end)
                if self.DFSDEBUG:
                    print node.value + "is an exit node, can we proceed? "+str(proceed)
                if proceed != None:
                    ctr = proceed
            if proceed==None:
                continue
            if e.weight != char and e.weight != "epsilon":
                #if self.DFSDEBUG:
                    #print "Edge has a weight "+e.weight+" but we are looking for "+char+" quitting..."
                return 0;
            else:
                # if we found our last node but we haven't found our character, don't add it to sigma set
                # only insert if not in sigma set
                # only call dfs again if inserted (i.e. sigma set changed)
                haveInserted = False
                if char != e.weight and end.value == "S"+self.getDot():
                    return 0
                if end.callNode != None:
                    if self.DFSDEBUG:
                        print end.value + " IS a call node. Adding to call set with ctr "+str(ctr)
                    if not sset.isItemInCallSet(end,ctr):
                        sset.insertSigmaCallItem(end,ctr)
                        ctr=counter
                        haveInserted = True
                else:
                    if self.DFSDEBUG:
                        print end.value + " is NOT a call node. Adding to sigma set with ctr "+str(ctr)
                    if not sset.isItemInSigmaSet(end,ctr):
                        sset.insertSigmaSetItem(end,ctr)
                        haveInserted = True
                    else:
                        key = end.value + str(ctr)
                        #sset.addPrevNodeToSigmaSetItem(key,node,ctr)
                        
                if e.weight == "epsilon":
                    #if self.DFSDEBUG:
                        #print "Edge weight is epsilon. Calling DFS again..."
                    
                    #This overflows the recursion limit in Python. We need a way to
                    #perform DFS without dfsGFG actually calling itself. 
                    
                    if haveInserted:
                        self.dfsGFG(end,char,sset,ctr,counter)
                else:
                    #if self.DFSDEBUG:
                        #print "Edge weight is "+e.weight+" which is what we are looking for. Calling DFS with epsilon"
                    # weight of edge equals char
                    if haveInserted:
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
        #sigmaSet.insertSigmaSetItem(start,counter)
        continueSearch = True

        with codecs.open(stringFile, encoding='utf-8',mode='r') as reader:
            parseString = reader.read().replace("\n", "")

        parseString = parseString.split(" ")
        parseString = [""]+parseString

        #sigmaSet = SigmaSet.SSet(0)
        #self.sigmaSets.append(sigmaSet)
        
        for i in range(0,len(parseString)):
            sigmaSet = SigmaSet.SSet(0)
            self.sigmaSets.append(sigmaSet)
        
        sset = self.sigmaSets[0]
        for e in start.edges:
            end = e.endNode
            if end.callNode != None:
                sset.insertSigmaCallItem(end,0)
            else:
                sset.insertSigmaSetItem(end,0)
            dot_index = end.value.find(".")
            if dot_index<(len(end.value)-1):
                if end.value[dot_index+1] == parseString[1]:
                    print end.value
                    sset.insertSigmaSetPathItem(end,0)

        for i in range(0,len(parseString)):
            sset = self.sigmaSets[i]
            print "ANALYZING SIGMA SET "+str(i)
            self.analyzeSigmaSet(sset,i,parseString)

        #self.debugSigmaSets(3)

        w = None
        sset = self.sigmaSets[len(parseString)-1]
        for n in sset.nodeSet:
            endItem = sset.nodeSet.get(n)
            endNode = endItem.node
            if endNode.value[-1] == "." and endNode.value[0:endNode.value.find('-')]=="S":
                if endItem.counter == 0:
                   w = endItem.sppfNode
        '''

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

            #analyze sigma set
            #remove sigma items with null points next sigmaset[counter++]
            
            # find nodes in last sigma set with outgoing edges to nodes
            # not in our graph. These are the nodes we want to start our
            # search with next iteration
            # if the sigma set is empty, then nodesToSearch will also be empty
            # and our loop will quit
            nodesToSearch = sigmaSet.findEndPoints()
            
            #self.analyzeSigmaSet(sigmaSet,nodesToSearch,counter)
            
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
        print validString
        

        '''
        
        if w != None:    
            #self.tree.printSPPF(w)
            print "This string is valid given grammar"
        else:
            print "This string is NOT valid given grammar"
        

    # this is a helper debug function
    # that loops through sigma sets and prints out their node and call sets
    def debugSigmaSets(self,num, start=0):
        for i in range(start,num+1):
            print "SIGMA SET "+str(i)+":"
            sset = self.sigmaSets[i]
            print "NODE SET:"
            for n in sset.nodeSet:
                print n + " from " + str(len(sset.nodeSet.get(n).prevNode)) + " other nodes"
                print sset.nodeSet.get(n).sppfNode
            print "CALL SET:"
            for c in sset.callSet:
                print c

    def analyzeSigmaSet(self,sset,ctr,parseString):
        R = []
        for n in sset.nodeSet:
            R.append(sset.nodeSet.get(n))
        for n in sset.callSet:
            R.append(sset.callSet.get(n))
        H = {}
        v = None
        w = None
        while len(R)>0:
            sigmaItem = R.pop()
            if sigmaItem.node.callNode != None:
                print sigmaItem.node.value + " evaluating call node"
                for e in sigmaItem.node.edges:
                    startNode = e.endNode
                for e in startNode.edges:
                    prod = e.endNode
                    key = prod.value + str(ctr)
                    val = self.checkSigmaPathSetsAndAdd(sset,key,prod,ctr,parseString)
                    if val != None:
                        R.append(val)
                if H.get(startNode.value[1:])!= None:
                    print "XXX in NULLABLE"+startNode.value[1:]
                    #TODO: check v?
                    nonTerminal = sigmaItem.node.value[0:sigmaItem.node.value.find('-')]
                    
                    y = self.tree.makeNodeAdvanced(sigmaItem.node.callNode.value,sigmaItem.counter,ctr,sigmaItem.sppfNode,v,nonTerminal)
                    newKey = sigmaItem.node.callNode.value + str(sigmaItem.counter)
                    newNode = sigmaItem.node.callNode
                    val = self.checkSigmaPathSetsAndAdd(sset,newKey,newNode,sigmaItem.counter,parseString,y)
                    if val != None:
                        R.append(val)               
            if sigmaItem.node.value[-1] == ".":
                print sigmaItem.node.value + " evaluating"
                nonTerminal = sigmaItem.node.value[0:sigmaItem.node.value.find('-')]
                
                w = sigmaItem.sppfNode

                if w == None:
                    nodeName = nonTerminal+str(ctr)+str(ctr)
                    if self.tree.nodeNames.get(nodeName) == None:
                        
                        v = self.tree.makeNode(nodeName,ctr,ctr,2)
                        self.tree.updateNonLeafNodes(v)
                    else:
                        v = self.tree.nodeNames.get(nodeName)
                    #TODO: do i need to update w in the sigmaItem?
                    w = v
                    epsilonNode = "epsilon"+str(ctr)+str(ctr)
                    foundEpsilonChild = False
                    for e in w.edges:
                        if e.endNode.name == "AND"+epsilonNode:
                            foundEpsilonChild = True
                    if not foundEpsilonChild:
                        ep = self.tree.makeNode(epsilonNode,ctr,ctr,2)
                        self.tree.updateNonLeafNodes(ep)
                        epsilonAnd = self.tree.makeNode("AND"+epsilonNode,ctr,ctr,0)
                        e = self.tree.makeEdge(w,epsilonAnd)
                        self.tree.addEdge(e)
                        e2 = self.tree.makeEdge(epsilonAnd,ep)
                        self.tree.addEdge(e2)
                print "about to add "+sigmaItem.node.value            
                if sigmaItem.counter == ctr:
                    H[nonTerminal] = w
                    print "ADDING TO NULLABLE"+nonTerminal
                sigmaSet = self.sigmaSets[sigmaItem.counter]
                for n in sigmaSet.callSet:
                    index = n.find(".")+1
                    if n[index:index+len(nonTerminal)] == nonTerminal:
                        item = sigmaSet.callSet.get(n)
                        y = self.tree.makeNodeAdvanced(item.node.callNode.value,item.counter,ctr,item.sppfNode,w,nonTerminal)
                        #TODO - can this be none?
                        '''
                        if y!=None:
                            print "XXX \t "+y.name
                        if w != None:
                            print "XXX \t child: "+w.name
                            '''
                        newKey = item.node.callNode.value + str(item.counter)
                        newNode = item.node.callNode
                        val = self.checkSigmaPathSetsAndAdd(sset,newKey,newNode,item.counter,parseString,y)
                        if val != None:
                            R.append(val)
        nextTerminal = parseString[(ctr+1):(ctr+2)]
        nextChar = nextTerminal
        nextTerminal = str(nextTerminal) + str(ctr) + str(ctr+1)
        v = self.tree.nodeNames.get(nextTerminal)
        if v == None:
            v = self.tree.makeNode(nextTerminal,ctr,ctr+1,2)
            self.tree.updateNonLeafNodes(v)
        while len(sset.pathSet.keys())>0:
            key, path = sset.pathSet.popitem();
            if len(path.node.edges)==1:
                newpath = ""
                weight = ""
                for e in path.node.edges:
                    if [e.weight] != nextChar:
                        continue
                    newpath = e.endNode
                    weight = e.weight
                if newpath != "":
                    
                    num = path.counter
                    w = path.sppfNode
                    print "From node "+path.node.value+" we are now looking at "+newpath.value
                    if w != None:
                        print "And we are using w = "+w.name
                    y = self.tree.makeNodeAdvanced(newpath.value,num,ctr+1,w,v,weight)
                    #if y != None:
                        #print "ZZZ \t "+y.name
                    if(ctr<len(parseString)-1):
                        val = self.checkSigmaPathSetsAndAdd(self.sigmaSets[ctr+1],newpath.value+str(num),newpath,num,parseString,y,1)
                        if val != None:
                            sset.insertSigmaSetPathItem(newpath,num,y)

    def checkSigmaPathSetsAndAdd(self,sset,key,prod,ctr,parseString,sppf=None,increment=0):
        #print sppf
        item = None
        if sset.nodeSet.get(key) == None and sset.callSet.get(key) == None:
            if prod.callNode != None:
                item = sset.insertSigmaCallItem(prod,ctr,sppf)
            else:
                item = sset.insertSigmaSetItem(prod,ctr,sppf)
        dot_index = prod.value.find(".")
        if dot_index<(len(prod.value)-1) and ctr < len(parseString)-1:
            if prod.value[dot_index+1] == parseString[ctr+1+increment]:
                sset.insertSigmaSetPathItem(prod,ctr,sppf)
        return item
        #TODO: if it's already in the set, do we still update it with sppf?
            
    
def main():
    if len(sys.argv) != 3:
            print "Usage: python earleyRecognizer.py grammerFile stringFile"
            sys.exit()
    grammarFile = sys.argv[1]
    stringFile = sys.argv[2]
    parser = Parser(grammarFile,stringFile)

if __name__ == "__main__":
    sys.exit(main())
