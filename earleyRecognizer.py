import sys
import GrammarFlowGraph

if len(sys.argv) != 3:
    print "Usage: python earleyRecognizer.py grammerFile stringFile"
    sys.exit()

grammarFile = sys.argv[1]
stringFile = sys.argv[2]
gfg = GrammarFlowGraph.GFG()
gfg.build(grammarFile)
