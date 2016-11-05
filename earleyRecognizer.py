import sys
import GrammarFlowGraph
import sigmaSet

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

nodesToSearch.push(start)
continueSearch = True
#iterate through characters in string to parse
while counter <= len(stringToParse) && continueSearch:
    
    # string manipulation to adjust period and get character we are looking for
    
    posString = stringToParse[0:counter]+dot+stringToParse[counter:]
    charToSearch = stringToParse[0:counter]
    if len(charToSearch) == 0:
        charToSearch = "epsilon"
    elif len(charToSearch) > 1:
        charToSearch = charToSearch[-1:]
        
    #initialize sigma set with id set to counter value
    sigmaSet = sigmaSet.SSet(counter)

    #add nodes and do algorithm
    #add sigma set to list of sets
    sigmaSets.insert(sigmaSet)
    '''
    When searching nodes...
    - if the weight of edge is epsilon, add node to sigma set and continue
    - if the weight of edge is a character are looking for, add node to sigma set
        and halt search and path is still valid
    - if the weight of edge is a character we are not looking for, halt
        and path is no longer valid
    '''
    counter+=1

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

