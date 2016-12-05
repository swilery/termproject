import sys
import GrammarFlowGraph
import SigmaSet
import SharedPackedParseForest
import codecs

class Parser:
    DEBUG = False

    def __init__(self,grammarFile,stringFile):
        self.gfg = GrammarFlowGraph.GFG(grammarFile)
        self.sigmaSets = []
        self.tree = SharedPackedParseForest.SPPF()
        self.parseTrees = []
        self.parse(stringFile)

    def getDot(self):
        return self.gfg.getDot()

    def parse(self,stringFile):
        '''
        First, we get our start node for the GFG (S.) that we will use to search for
        productions for our first sigma set.

        We create the number of sigma sets we will need
        (n sets where n = length of input string)

        We add a space at the beginning of the parse string to represent the first search
        '''
        start = self.gfg.startNode
        counter = 0 
        dot = self.getDot()

        with codecs.open(stringFile, encoding='utf-8',mode='r') as reader:
            parseString = reader.read().replace("\n", "")

        parseString = parseString.split(" ")
        parseString = [""]+parseString

        
        for i in range(0,len(parseString)):
            sigmaSet = SigmaSet.SSet(0)
            self.sigmaSets.append(sigmaSet)

        '''
        For the first sigma set, iterate over the productions for S.
        (Or, the outgoing edges on our GFG) and add them to our sigma set

        If the first character on the righthand side is a terminal,
        and that terminal is the next terminal we will be searching for
        (i.e. parseString[1]) then add that to our Sigma Path Set - the set
        of nodes we want to search for our next sigma set. 

        '''
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

        '''
        Now that we've created our first sigma set, we execute
        Scott's algorithm, which loops over each sigma set in order
        and creates the SPPF in place

        '''
        for i in range(0,len(parseString)):
            sset = self.sigmaSets[i]
            self.analyzeSigmaSet(sset,i,parseString)

        '''
        To check if a string is valid or not, we check if the last sigma set
        contains the end of an S production, i.e. S -> ABC.

        If it does, we get the sppf node associated with that sigma set item
        This sppf node is the root of our sppf tree
        '''
        w = None
        sset = self.sigmaSets[len(parseString)-1]
        for n in sset.nodeSet:
            endItem = sset.nodeSet.get(n)
            endNode = endItem.node
            if endNode.value[-1] == "." and endNode.value[0:endNode.value.find('-')]=="S":
                if endItem.counter == 0:
                   w = endItem.sppfNode
        
        if w != None:    
            self.tree.printSPPF(w)
            print "This string is valid given grammar"
        else:
            print "This string is NOT valid given grammar"
        
    '''
    This is a nifty helper debug function
    that loops through sigma sets and prints out their node and call sets
    '''
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

    '''
    This function does the major grunt work for Scott's algorithm
    It is a near faithful implementation of the pseudocode in her paper
    '''
    def analyzeSigmaSet(self,sset,ctr,parseString):

        '''
        We start by creating a working directory of our sigma set items that
        we will manipulate (R).

        H represents our NULLABLE set for this sigma set

        v and w will be sppf nodes that will be used to populate children later

        Each sigma set item contains three field:
        1. Node (the actual GFG node)
        2. Tag
        3. SPPF Node (initialized to None)
        
        '''
        R = []
        for n in sset.nodeSet:
            R.append(sset.nodeSet.get(n))
        for n in sset.callSet:
            R.append(sset.callSet.get(n))
        H = {}
        v = None
        w = None
        
        while len(R)>0:
            '''

            We pop items from our "working" sigma set.
            We only process them if they are
            a) a call node S -> .Ab
            b) an exit node S -> Ab.
            
            '''
            sigmaItem = R.pop()

            '''
            CALL NODES
            '''
            if sigmaItem.node.callNode != None:
                for e in sigmaItem.node.edges:
                    startNode = e.endNode
                '''
                For each production for the nonTerminal we are about to call into
                '''
                for e in startNode.edges:
                    prod = e.endNode
                    key = prod.value + str(ctr)
                    '''
                    Add it to our sigma sets and path sets as appropriate
                    '''
                    val = self.checkSigmaPathSetsAndAdd(sset,key,prod,ctr,parseString)
                    if val != None:
                        R.append(val)
                '''
                If it is nullable we want to make sure our CALL NODE goes to epsilon in our final graph
                '''
                if H.get(startNode.value[1:])!= None:
                    #TODO: check v?
                    nonTerminal = sigmaItem.node.value[0:sigmaItem.node.value.find('-')]
                    
                    y = self.tree.makeNodeAdvanced(sigmaItem.node.callNode.value,sigmaItem.counter,ctr,sigmaItem.sppfNode,v,nonTerminal)
                    newKey = sigmaItem.node.callNode.value + str(sigmaItem.counter)
                    newNode = sigmaItem.node.callNode
                    val = self.checkSigmaPathSetsAndAdd(sset,newKey,newNode,sigmaItem.counter,parseString,y)
                    if val != None:
                        R.append(val)
            '''
            EXIT NODES
            '''
            if sigmaItem.node.value[-1] == ".":
                nonTerminal = sigmaItem.node.value[0:sigmaItem.node.value.find('-')]
                
                w = sigmaItem.sppfNode

                if w == None:
                    '''
                    If this sigmaItem has no corresponding SPPF node (yet)
                    Then it's an epsilon production.
                    We first create the node for the non terminal node that produces it
                    (or associate our sigmaItem with that node if it has already been created)
                    '''
                    nodeName = nonTerminal+str(ctr)+str(ctr)
                    if self.tree.nodeNames.get(nodeName) == None:
                        
                        v = self.tree.makeNode(nodeName,ctr,ctr,1)
                        self.tree.updateNonLeafNodes(v)
                    else:
                        v = self.tree.nodeNames.get(nodeName)
                    #TODO: do i need to update w in the sigmaItem?
                    w = v
                    epsilonNode = "epsilon"+str(ctr)+str(ctr)
                    foundEpsilonChild = False
                    '''
                    Next we see if it has a family of an epsilon node. If it does not,
                    we need to add one
                    '''
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

                '''
                If it's nullable, put it in H (our nullable list)
                '''
                if sigmaItem.counter == ctr:
                    H[nonTerminal] = w

                '''
                Get the sigma set of its tag. That is, the sigma set where we first
                evaluated the production for the non terminal.
                We copy the call nodes into a working directory if they are productions
                for our non terminal
                '''
                sigmaSet = self.sigmaSets[sigmaItem.counter]
                workingSet = []
                for n in sigmaSet.callSet:
                    index = n.find(".")+1
                    if n[index:index+len(nonTerminal)] == nonTerminal:
                        item = sigmaSet.callSet.get(n)
                        workingSet.append(item)
                        
                item = ""

                '''
                For each of our call nodes for our non terminal, we want to make a node for them,
                and then enter them into sigma sets and sigma path sets as appropriate
                '''
                for item in workingSet:
                    y = self.tree.makeNodeAdvanced(item.node.callNode.value,item.counter,ctr,item.sppfNode,w,nonTerminal)
                    #TODO - can this be none?
                    newKey = item.node.callNode.value + str(item.counter)
                    newNode = item.node.callNode
                    val = self.checkSigmaPathSetsAndAdd(sset,newKey,newNode,item.counter,parseString,y)
                    if val != None:
                        R.append(val)
                        
        '''
        After processing our sigma set, we create a leaf node for the next
        terminal in our string to analyze, if one hasn't been created already
        '''
        nextTerminal = parseString[(ctr+1):(ctr+2)]
        nextChar = nextTerminal
        nextTerminal = str(nextTerminal) + str(ctr) + str(ctr+1)
        v = self.tree.nodeNames.get(nextTerminal)
        if v == None:
            v = self.tree.makeNode(nextTerminal,ctr,ctr+1,2)
            self.tree.updateNonLeafNodes(v)

        '''
        Now we loop through path set, which is all nodes of the form
        A -> a.bc where b is the character are going to analyze next
        (and the leaf node we just created)
        '''
        while len(sset.pathSet.keys())>0:
            key, path = sset.pathSet.popitem();
            '''
            Find the scan node for our node
            (for instance, if we have A -> a.bc we want A -> ab.c)
            '''
            if len(path.node.edges)==1:
                newpath = ""
                weight = ""
                for e in path.node.edges:
                    if [e.weight] != nextChar:
                        continue
                    newpath = e.endNode
                    weight = e.weight
                if newpath != "":
                    '''
                    Now we will make a new SPPF tree node (or update an existing one)
                    for our scan node with our newly created leave node as a child

                    We need to reflect the fact that our terminal A in A -> ab.c has new
                    leaf node (b) and therefore also new start and end position indicies 
                    '''
                    num = path.counter
                    w = path.sppfNode
                    y = self.tree.makeNodeAdvanced(newpath.value,num,ctr+1,w,v,weight)
                    '''
                    Finally, add this new node to the next sigma set, so we process it again
                    (whether as an exit node or if there are more non terminals to process)

                    And check to see if the next terminal, i.e. "c" in A -> ab.c is the next
                    character in our parseString we need to analyze 
                    '''
                    if(ctr<len(parseString)-1):
                        val = self.checkSigmaPathSetsAndAdd(self.sigmaSets[ctr+1],newpath.value+str(num),newpath,num,parseString,y,1)
                        if val != None:
                            sset.insertSigmaSetPathItem(newpath,num,y)

    '''
    Multiple times in Scott's algorithm we have a node and we want to:
    a) add it to a sigma set if it isn't already there
    b) check if the next character to be scanned is a terminal and, if it is,
        if that terminal is the next terminal in our parseString, in which case
        that node needs to be added to our path set

    This function does all that tedious work

    '''
    def checkSigmaPathSetsAndAdd(self,sset,key,prod,ctr,parseString,sppf=None,increment=0):
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
