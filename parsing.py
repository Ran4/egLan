import eglan


def split(string, splitChar=","):
    seq = list(string)
    outSeq = []
    outValue = []
    inParen = 0
    for i, ch in enumerate(seq):
        if ch == "(":
            inParen += 1
            outValue.append(ch)
        elif ch == ")":
            if inParen == 0:
                errorString = "In split,\n%s\n%s\nMismatched paranthesis!" % \
                        (string, " "*i + "^")
                eglan.EglParser._staticPrintError(None, errorString)
                return None
            
            outValue.append(ch)
            inParen -= 1
            
        elif ch == splitChar and inParen == 0:
            outSeq.append("".join(outValue).strip())
            outValue = []
        else:
            outValue.append(ch)
    
    if outValue:
        outSeq.append("".join(outValue).strip())
    return outSeq
            
            
def testSplit():
    
    inOutValues = {
            "1": ["1"],
            "1,2": ["1", "2"],
            "1,2,3": ["1", "2", "3"],
            "1,(2,3),4": ["1", "(2,3)", "4"],
            "1,(2,3,4)": ["1", "(2,3,4)"],
            "1,(2,3, 4)": ["1", "(2,3, 4)"],
            "1, (2,(8,9),3), 4": ["1", "(2,(8,9),3)", "4"],
            }
    
    print "Testing split function"
    for key in inOutValues.keys():
        assert(split(key) == inOutValues[key])
        print "%s -> %s" % (split(key), inOutValues[key]),
        print eglan.colored("OK", "green")
    
if __name__ == "__main__":
    testSplit()
