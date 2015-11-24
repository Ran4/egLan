import sys

class EglParser(object):
    def __init__(self):
        self.setupDict()
        
    def setupDict(self):
        self.d = {
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
        return  "  " * (self.stat["indent"]+0) + \
                "-> "
    
    def run(self, lines):
        print "%sBegin running %s line%s" % \
            (self.getIndentString(),
            len(lines), "s" if len(lines)!=1 else "")
        
        stripSeq = lambda seq: [x.strip() for x in seq]
        for iteration, line in enumerate(lines):
            line = line.strip()
            d = self.d
            
            print "%s: %s" % (iteration, line)
            
            if len(line) == 0:
                continue
            
            if line == "clear":
                self.clear()
            elif line.startswith("circle "):
                line = line[len("circle "):]
                
                withArgs = None
                if " with " in line:
                    line, withArgs = line.split("with", 1)
                
                args = stripSeq(line.split(","))
                
                if withArgs:
                    self.stat["indent"] += 1
                    self.run(withArgs.split(" and "))
                    self.stat["indent"] -= 1
                
                x = args[0] if len(args) > 0 else d["X"]
                y = args[1] if len(args) > 1 else d["Y"]
                r = args[2] if len(args) > 2 else d["RADIUS"]
                col = args[2] if len(args) > 2 else d["COLOR"]
                    
                #TODO: draw circle here!
                print "%sCIRCLE(x=%s, y=%s, r=%s, col=%s)" % \
                    (self.getIndentString(), x, y, r, col)
                
            elif line.count("=") > 0:
                a = stripSeq(line.split("="))
                if len(a) == 1:
                    print "Error parsing line '%s'" % line
                    continue
                elif len(a) == 2:
                    print "%s%s = %s%s" % \
                            (self.getIndentString(), a[0], a[1],
                            "" if a[0] in d.keys() else " (NEW)")
                            
                    d[a[0]] = a[1]
                elif len(a) > 2:
                    #a = b = c => b = c, a = b
                    for i in range(len(a)-1, 1, -1):
                        if i == len(a) - 1:
                            d[a[i-1]] = a[i]
                        else:
                            d[a[i-1]] = d[a[i]]
                    


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        lines = open(sys.argv[1]).read().split()
    else:
        #args = "test.egl"
        lines = """
        RADIUS = 20
        circle 30, 40
        circle 30, 40 with COLOR = (20, 30, 40)
        """.strip().split("\n")
    
    eglParser = EglParser()
    eglParser.run(lines)
