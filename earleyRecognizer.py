import sys
import GrammarFlowGraph
import SigmaSet

if len(sys.argv) != 4:
    print "Usage: python earleyRecognizer.py grammerFile stringFile parseString"
    sys.exit()

grammarFile = sys.argv[1]
stringFile = sys.argv[2]
stringToParse = sys.argv[3]
gfg = GrammarFlowGraph.GFG()
gfg.build(grammarFile)

start = gfg.startNode
counter = 0 
dot = "."
sigmaSets = []

#Set up our Sigma Set0 initially with the start node
nodesToSearch = []
nodesToSearch.append(start)
sigmaSet = SigmaSet.SSet(0)
sigmaSet.insertSigmaSetItem(start,counter)
sigmaSets.append(sigmaSet)
continueSearch = True

#iterate through characters in string to parse
# we want to iterate while we have more characters to parse
# and nodes in our last sigma set that need searching
while counter <= len(stringToParse) and len(nodesToSearch)>0:
    
    # string manipulation to adjust period and get character we are looking for
    
    posString = stringToParse[0:counter]+dot+stringToParse[counter:]
    charToSearch = stringToParse[0:counter]
    if len(charToSearch) == 0:
        charToSearch = "epsilon"
    elif len(charToSearch) > 1:
        charToSearch = charToSearch[-1:]
        
    #get our sigma set from our list for this iteration
        
    sigmaSet = sigmaSets[counter]

                   
    '''

          i think recursively with dfs matches best here

          dfs(node, charToSearch, sigmaSet)
              For all outgoing edges from said node
              - if weight is epsilon,
                  add end node to sigma set
                  call dfs(node, charToSearch, sigmaSet)
              - if weight is c,
                  add end node to sigma set
                  call dfs (node, "epsilon", sigmaSet)
              - if weight is not c and not epsilon, return 0
              
    '''

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
if counter>len(stringToParse):
    end = start.endNode
    lastSigmaSet = sigmaSets[counter-1]
    if lastSigmaSet.nodeSet.get(end.value) != None:
        validString = True

if validString:
    print "This string is valid given grammar"
else:
    print "This string is NOT valid given grammar"

