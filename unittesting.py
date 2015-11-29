import eglan

def testHLine():
    EglParser = eglan.EglParser
    
    print eglan.colored("Starting unit testing of hline", "yellow")
    
    eglParser = EglParser()
    eglParser.d["NODRAW"] = True
    assert(eglParser.handleVHLine(["30"], False, "h") == True)
    assert(eglParser.handleVHLine([], False, "h") != True)
    
    eglParser.run(["hline 50"])
    eglParser.run(["hline with y = 30"])
    eglParser.run(["hline with Y = 30"])
    
    print eglan.colored("Successfully tested hline", "green")

def testGetArgOrEval():
    EglParser = eglan.EglParser
    
    print eglan.colored("Starting unit testing of getArgOrEval", "yellow")
    
    eglParser = EglParser()
    assert(eglParser.getArgOrEval("2") == 2)
    eglParser = EglParser()
    assert(eglParser.getArgOrEval("") == None)
    eglParser = EglParser()
    assert(eglParser.getArgOrEval("23") == 23)
    eglParser = EglParser()
    assert(eglParser.getArgOrEval("1 + 2") == 3)
    eglParser = EglParser()
    assert(eglParser.getArgOrEval("1 + 2 + 3") == 6)
    
    eglParser = EglParser()
    eglParser.run(["W = 300"])
    assert(eglParser.getArgOrEval("W") == 300)
    
    eglParser = EglParser()
    eglParser.run(["W = 300"])
    assert(eglParser.getArgOrEval("W+W") == 600)
    
    eglParser = EglParser()
    eglParser.run(["W = 300", "H = 200"])
    assert(eglParser.getArgOrEval("W+H") == 500)
    
    eglParser = EglParser()
    eglParser.run(["ABC = 300", "DEF = 200"])
    assert(eglParser.getArgOrEval("ABC+DEF") == 500)
    
    eglParser = EglParser()
    eglParser.run(["ABC = 50"])
    assert(eglParser.getArgOrEval("2*ABC") == 100)
    
    eglParser = EglParser()
    eglParser.run(["ABC = 50"])
    assert(eglParser.getArgOrEval("ABC") == 50)
    
    import math
    
    eglParser = EglParser()
    eglParser.run(["ABC = 1.0"])
    assert(abs(eglParser.getArgOrEval("ABC*math.pi") - math.pi) < 0.001)
    
    print eglan.colored("Successfully tested getArgOrEval!", "green")
    
def run():
    testGetArgOrEval()
    testHLine()
   
if __name__ == "__main__":
    run()
