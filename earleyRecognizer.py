import sys
import GrammarFlowGraph
import SigmaSet
import codecs

sigmaSets = []
DEBUG = False
DFSDEBUG = False

def isEdgeValidPath(nodeValue,ctr,counter,endNode):
    # Checks to see if we should traverse an edge
    # for a return node based on which sigma set its
    # call node is in
    nodeValue = "."+nodeValue[:-1]
    nodeValueKey = nodeValue+str(ctr)
    sset = {}
    while(counter>=0):
        sset = sigmaSets[counter]
        if sset.nodeSet.get(nodeValueKey)!= None:
            break
        counter-=1
    if counter<0:
        print "ERROR! No starting node found for "+nodeValue
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

def dfsGFG(node, char, sset,ctr,counter):
    if DFSDEBUG:
        print "Evaluating node "+node.value+" with counter "+str(ctr)+" looking for "+char
    for e in node.edges:
        end = e.endNode
        if DFSDEBUG:
            print "Evaluating edge from "+node.value+" to "+end.value
        proceed = True
        if node.isExitNode():
            if DFSDEBUG:
                print node.value + "is an exit node "
            proceed = isEdgeValidPath(node.value,ctr,counter,end)
        if not proceed:
            continue
        if e.weight != char and e.weight != "epsilon":
            if DFSDEBUG:
                print "Edge has a weight "+e.weight+" but we are looking for "+char+" quitting..."
            return 0;
        else:
            # if we found our last node but we haven't found our character, don't add it to sigma set
            if char != e.weight and end.value == "S.":
                return 0
            if end.callNode != None:
                if DFSDEBUG:
                    print end.value + " IS a call node. Adding to call set with ctr "+str(counter)
                sset.insertSigmaCallItem(end,counter)
                ctr=counter
            else:
                if DFSDEBUG:
                    print end.value + " is NOT a call node. Adding to sigma set with ctr "+str(ctr)
                sset.insertSigmaSetItem(end,ctr)
            if e.weight == "epsilon":
                if DFSDEBUG:
                    print "Edge weight is epsilon. Calling DFS again..."
                dfsGFG(end,char,sset,ctr,counter)
            else:
                if DFSDEBUG:
                    print "Edge weight is "+e.weight+" which is what we are looking for. Calling DFS with epsilon"
                # weight of edge equals char
                dfsGFG(end,"epsilon",sset,ctr,counter)
    return 0;

def main():
    if len(sys.argv) != 3:
        print "Usage: python earleyRecognizer.py grammerFile stringFile"
        sys.exit()

    grammarFile = sys.argv[1]
    stringFile = sys.argv[2]
    gfg = GrammarFlowGraph.GFG()
    gfg.build(grammarFile)
    sys.exit()
    start = gfg.startNode
    counter = 0 
    dot = "."


    #Set up our Sigma Set0 initially with the start node
    nodesToSearch = {}
    startKey = start.value + "0"
    nodesToSearch[startKey] = start
    sigmaSet = SigmaSet.SSet(0)
    sigmaSet.insertSigmaSetItem(start,counter)
    sigmaSets.append(sigmaSet)
    continueSearch = True

    with codecs.open(stringFile, encoding='utf-8',mode='r') as reader:
        parseString = reader.read().replace("\n", "")
    
    #iterate through characters in string to parse
    # we want to iterate while we have more characters to parse
    # and nodes in our last sigma set that need searching
    while counter <= (len(parseString)) and len(nodesToSearch)>0:
        # string manipulation to adjust period and get character we are looking for
        #posString = stringFile[0:counter]+dot+stringFile[counter:]
        posString = parseString[0:counter]+dot+parseString[counter:]
        charToSearch = stringFile[0:counter]
        charToSearch = parseString[0:counter]
        if len(charToSearch) == 0:
            charToSearch = "epsilon"
        elif len(charToSearch) > 1:
            charToSearch = charToSearch[-1:]   
        #get our sigma set from our list for this iteration
            
        sigmaSet = sigmaSets[counter]

        for sigmaN in nodesToSearch:
            n = nodesToSearch.get(sigmaN)
            if DEBUG:
                print sigmaN + " looking for " + charToSearch
            ctr = sigmaN[-1]
            dfsGFG(n,charToSearch, sigmaSet,ctr,counter)

        
        # find nodes in last sigma set with outgoing edges to nodes
        # not in our graph. These are the nodes we want to start our
        # search with next iteration
        # if the sigma set is empty, then nodesToSearch will also be empty
        # and our loop will quit
        nodesToSearch = sigmaSet.findEndPoints()

        #create sigma set for next round
        counter+=1
        sigmaSet = SigmaSet.SSet(counter)
        sigmaSets.append(sigmaSet)


    # if we went through the whole string, and the
    # end node is in the last sigma set
    validString = False
    #if counter>len(stringFile):
    if counter>len(parseString):
        end = start.endNode
        lastSigmaSet = sigmaSets[counter-1]
        # we don't know what the associated counter with our end node is
        # therefore we need to loop through all nodes in our last sigma set
        if lastSigmaSet.hasEndNode:
            validString = True
    if validString:
        print "This string is valid given grammar"
    else:
        print "This string is NOT valid given grammar"

if __name__ == "__main__":
    sys.exit(main())
