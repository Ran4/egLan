#!/usr/bin/env python
import unittest

import eglan
import parsing

class EgLanTests(unittest.TestCase):
    def test_GetArgOrEval(self):
        EglParser = eglan.EglParser
        
        print eglan.colored("Starting unit testing of getArgOrEval", "yellow")
        
        self.assertEqual(EglParser().getArgOrEval("2"), 2)
        self.assertEqual(EglParser(dict_addon={"HIDEERRORS": True}).getArgOrEval(""), None)
        self.assertEqual(EglParser().getArgOrEval("23"), 23)
        self.assertEqual(EglParser().getArgOrEval("1 + 2"), 3)
        self.assertEqual(EglParser().getArgOrEval("1 + 2 + 3"), 6)
        
        eglParser = EglParser()
        eglParser.run(["W = 300"])
        self.assertEqual(eglParser.getArgOrEval("W"),  300)
        
        eglParser = EglParser()
        eglParser.run(["W = 300"])
        self.assertEqual(eglParser.getArgOrEval("W+W"),  600)
        
        eglParser = EglParser()
        eglParser.run(["W = 300", "H = 200"])
        self.assertEqual(eglParser.getArgOrEval("W+H"),  500)
        
        eglParser = EglParser()
        eglParser.run(["ABC = 300", "DEF = 200"])
        self.assertEqual(eglParser.getArgOrEval("ABC+DEF"),  500)
        
        eglParser = EglParser()
        eglParser.run(["ABC = 50"])
        self.assertEqual(eglParser.getArgOrEval("2*ABC"),  100)
        
        eglParser = EglParser()
        eglParser.run(["ABC = 50"])
        self.assertEqual(eglParser.getArgOrEval("ABC"),  50)
        
        import math
        
        eglParser = EglParser()
        eglParser.run(["ABC = 1.0"])
        self.assertTrue(
            abs(eglParser.getArgOrEval("ABC*math.pi") - math.pi) < 0.001)
        
        print eglan.colored("Successfully tested getArgOrEval!", "green")
        
    def test_HLine(self):
        EglParser = eglan.EglParser
        
        print eglan.colored("Starting unit testing of hline", "yellow")
        
        eglParser = EglParser()
        eglParser.d["NODRAW"] = True
        self.assertTrue(eglParser.handleVHLine(["30"], useWith=False, vh="h"))
        self.assertTrue(eglParser.handleVHLine(["30"], useWith=False, vh="h"))
        eglParserNoOutput = EglParser(
            {"NODRAW":True, "HIDEWARNINGS": True, "HIDEERRORS": True})
        self.assertNotEqual(
            eglParserNoOutput.handleVHLine( [], useWith=False, vh="h"), True)
        
        eglParser.run(["hline 50"])
        self.assertNotEqual(eglParserNoOutput.run(["hline with y = 30"]), True)
        eglParser.run(["hline with Y = 30"])
        
        print eglan.colored("Successfully tested hline", "green")
        
def run_tests():
    parsing.testSplit()
    unittest.main()
    
if __name__ == "__main__":
    run_tests()
