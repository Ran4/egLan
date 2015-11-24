import sys
from termcolor import colored

class EglParser(object):
    def __init__(self):
        self.setupDict()
        
    def setupDict(self):
        self.w = {"_ID":"w"
                }
        self.d = {
            "_ID": "d",
            "BLACK":(0,0,0),
            "RED":(255,0,0),
            "GREEN":(0,255,0),
            "BLUE":(0,0,255),
            "BG":(255,255,255),
            "COLOR":(0,0,0),
            "RADIUS": 16,
            "H":500,
            "W":500
        }
        self.stat = {
                "indent": 0,
        }
    
    def getIndentString(self):
        return  "    " * (self.stat["indent"]+0) + \
                "-> "
    
    def getValue(self, key, useWith):
        if key in self.w and useWith:
            #print "\t\tgetValue: self.w[%s] = %s" % (key, self.w[key])
            return self.w[key]
        elif key in self.d:
            #print "\t\tgetValue: self.d[%s] = %s" % (key, self.d[key])
            return self.d[key]
        else:
            if useWith:
                print "Can't find value '%s' in self.d or self.w" % key
            else:
                print "Can't find value '%s' in self.d, can't check self.w"%key
            return None
        
    def printSuccess(self, s):
        print colored(self.getIndentString() + s, "green")
        
    def printError(self, s):
        print colored("ERROR: " + s, "red")
        
    def printValueSet(self, s):
        print colored(self.getIndentString() + s, "magenta")
        #red, green, yellow, blue, magenta, cyan, white.
        
    def printNotImplemented(self, s):
        print colored("%sNOT IMPLEMENTED (%s)" % (self.getIndentString(), s), "cyan")
    
    def stripSeq(self, seq):
        return [x.strip() for x in seq if x.strip()]
    
    def run(self, lines, dictionary=None):
        if dictionary is None:
            dictionary = self.d
            
        #print "%s BEGIN %s line%s" % \
        #    ("\n" + "    "*self.stat["indent"] + "*"*8,
        #    len(lines), "s" if len(lines)!=1 else "")
        
        d = dictionary
        gv = self.getValue
        
        for iteration, line in enumerate(lines):
            useWith = False
            line = line.strip()
            
            if len(line) == 0:
                #print ""
                continue
            
            print "%s%s: %s" % ("    "*self.stat["indent"], iteration, line),
            
            
            #handle with statements
            if " with " in line:
                line, withArgs = line.split("with", 1)

                if withArgs:
                    self.w = {"_ID":"w"}
                    self.stat["indent"] += 1
                    print
                    self.run(withArgs.split(" and "), self.w)
                    self.stat["indent"] -= 1
                    useWith = True
            
            #regular handling
            if line == "clear":
                self.clear()
            elif line.startswith("line "):
                args = self.stripSeq(line[len("line "):].split(","))
                self.handleLine(args, useWith)
                
            elif line.startswith("hline "):
                self.printNotImplemented("hline")

            elif line.startswith("circle"):
                args = self.stripSeq(line[len("circle"):].split(","))
                self.handleCircle(args, useWith)
                
            elif line.count("=") > 0:
                self.handleAssignment(line, dictionary)
            else:
                print colored("%sUNKNOWN line '%s'" % (self.getIndentString(), line), "yellow")
                
                
    def handleAssignment(self, line, dictionary):
        d = dictionary
        a = self.stripSeq(line.split("="))
        if len(a) == 1:
            #print colored("Error parsing line '%s'" % line, "red")
            self.printError("Can't parse line '%s'" % line)
        elif len(a) == 2:
            self.printValueSet("%s = %s%s <%s>" % (a[0], a[1], "" if a[0] in d.keys() else " (NEW)", d["_ID"]))
                    
            d[a[0]] = eval(a[1])
        elif len(a) > 2:
            #a = b = c => b = c, a = b
            for i in range(len(a)-1, 1, -1):
                if i == len(a) - 1:
                    d[a[i-1]] = eval(a[i])
                else:
                    d[a[i-1]] = eval(d[a[i]])
        
    def handleCircle(self, args, useWith):
        gv = self.getValue
        x = args[0] if len(args) > 0 else gv("X", useWith)
        y = args[1] if len(args) > 1 else gv("Y", useWith)
        r = args[2] if len(args) > 2 else gv("RADIUS", useWith)
        col = args[2] if len(args) > 2 else gv("COLOR", useWith)
        
        if x is None: self.printError("no x given")
        elif y is None: self.printError("no y given")
        elif r is None: self.printError("no r given")
        elif col is None: self.printError("no col given")
        else: self.printSuccess(
            "CIRCLE(x=%s, y=%s, r=%s, col=%s)" % (x, y, r, col))
        
    def handleLine(self, args, useWith):
        gv = self.getValue
        x1 = args[0] if len(args) > 0 else gv("X", useWith)
        y1 = args[1] if len(args) > 1 else gv("Y", useWith)
        x2 = args[2] if len(args) > 2 else gv("X2", useWith)
        y2 = args[3] if len(args) > 3 else gv("Y2", useWith)
        col = args[4] if len(args) > 4 else gv("COLOR", useWith)
        
        if x1 is None: self.printError("no x1 given")
        elif y1 is None: self.printError("no y1 given")
        elif x2 is None: self.printError("no x2 given")
        elif y2 is None: self.printError("no y2 given")
        elif col is None: self.printError("no col given")
        else: self.printSuccess(
            "LINE(x1=%s, y1=%s, x2=%s, y2=%s, col=%s)" % (x1, y1, x2, y2, col))
                
                            

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        lines = open(sys.argv[1]).read().split()
    else:
        #args = "test.egl"
        lines = """
        RADIUS = 20
        circle 30
        
        circle 30, 40
        circle 30, 40 with COLOR = (20, 30, 40)
        
        circle 30, 40
        line 20, 30, 40, 50
        line 20, 30 with X2 = 4 and Y2 = 2
        hline 20
        line 20, 30 with X2 = 4 and Y2 = 2
        
        X = 90
        Y = 99
        circle with COL = (3, 4, 5)
        """.strip().split("\n")
    
    eglParser = EglParser()
    eglParser.run(lines)
