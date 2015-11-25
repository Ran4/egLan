import sys
import math
import time

from PIL import Image
from PIL import ImageDraw

try:
    from termcolor import colored
except: #Couldn't load termcolor, use a regular function instead
    def colored(*args):
        return args[0]

class EglParser(object):
    def __init__(self):
        self.im = None
        self.draw = None
        self.setupDict()
        
    def setupDict(self):
        self.w = {"_ID":"w"
                }
        self.d = {
            "_ID": "d",
            "NODRAW": False,
            "VERBOSE": True,
            "HIDEWARNINGS": False,
            "BLACK":(0,0,0),
            "RED":(255,0,0),
            "GREEN":(0,255,0),
            "BLUE":(0,0,255),
            "BG":(255,255,255),
            "COLOR":(0,0,0),
            "RADIUS": 16,
            "FILENAME":"out.png",
            "W":500,
            "H":500,
        }
        self.stat = {
            "indent": 0,
        }
    
    def getIndentString(self):
        return  "    " * (self.stat["indent"]+0) + \
                "-> "
    
    def getValue(self, key, useWith=False):
        if key in self.w and useWith:
            if self.w["VERBOSE"] == 2 or self.d["VERBOSE"] == 2:
                print "\t\tgetValue: self.w[%s] = %s" % (key, self.w[key])
            return self.w[key]
        elif key in self.d:
            if self.d["VERBOSE"] == 2:
                print "\t\tgetValue: self.d[%s] = %s" % (key, self.d[key])
            return self.d[key]
        else:
            if useWith:
                self.printWarning("Can't find value '%s' in dictionary!" % key)
            else:
                self.printWarning("Can't find value '%s' in dictionary!" % key)
            return None
        
    def getArgOrEval(self, arg, useWith=False):
        #"W//2" -> "800//2" -> 400
        if self.getValue("VERBOSE", useWith) == 2:
            print "in getArgsOrEval, arg='%s'" % arg
        
        variableName = ""
        i = 0
        startReplaceWord = False
        while i < len(arg):
            #vars starts with ABC.., can contain 0123.. but not at the beginning
            if arg[i] in "ABCDEFGHIJKLMNOPQRSTUVWYZ_" or \
                    len(variableName) > 0 and arg[i] in "0123456789":
                variableName += arg[i]
                if self.getValue("VERBOSE", useWith) == 2:
                    print "variableName=<%s>" % (variableName)
            else:
                if variableName:
                    startReplaceWord = True
                
            if variableName and (startReplaceWord or i == (len(arg) - 1)):
                startReplaceWord = False
                
                if variableName in self.w and useWith:
                    replacedVal = str(self.w[variableName])
                elif variableName in self.d:
                    replacedVal = str(self.d[variableName])
                else:
                    print "Couldnt' find %s in dictionary!" % variableName
                    replacedVal = variableName
                
                if self.getValue("VERBOSE", useWith) == 2:
                    print "arg before: '%s'" % arg
                arg = arg.replace(variableName, replacedVal)
                i = -1
                if self.getValue("VERBOSE", useWith) == 2:
                    print "arg after:  '%s'" % arg
                variableName = ""
                
                try:
                    print "Trying to evaluate <%s>" % arg
                    possibleValue = eval(arg)
                    return possibleValue
                except:
                    print "Couldn't evaluate <%s>" % arg
                
            i += 1
                
        if not arg:
            self.printError("arg is empty!")
            return None
        
        finalValue = eval(arg)
        #print "finalValue:", finalValue
        return finalValue
    
    def getImage(self):
        if self.im:
            return self.im
        else:
            w = self.getValue("W")
            h = self.getValue("H")
            bg_col = self.getValue("BG")
            if w is not None and h is not None:
                self.im = Image.new("RGB", (w, h), color=bg_col)
            else:
                self.printError(
                        "Lacking variables W and H, can't create image!")
    
        return self.im
    
    def getDraw(self):
        if self.draw:
            return self.draw
        else:
            im = self.getImage()
            if im:
                self.draw = ImageDraw.Draw(im)
                if self.draw:
                    return self.draw
            
        self.printError("Problem getting ImageDraw.Draw function!")
        return None
        
    def printSuccess(self, s, useWith=False):
        verbose = self.getValue("VERBOSE", useWith)
        if verbose:
            print colored(self.getIndentString() + s, "green")
        
    def printError(self, s):
        print colored("ERROR: " + s, "red")
        
    def printWarning(self, s, useWith=False):
        hideWarnings = self.getValue("HIDEWARNINGS", useWith)
        if not hideWarnings:
            print colored("WARNING: " + s, "blue")
        
    def printValueSet(self, s, useWith=False):
        verbose = self.getValue("VERBOSE", useWith)
        if verbose:
            print colored(self.getIndentString() + s, "magenta")
        #red, green, yellow, blue, magenta, cyan, white.
        
    def printNotImplemented(self, s):
        print colored("%sNOT IMPLEMENTED (%s)" % \
                (self.getIndentString(), s), "cyan")
    
    def stripSeq(self, seq):
        return [x.strip() for x in seq if x.strip()]
    
    """Takes a list of strings lines and runs them as egLan script
    """
    def run(self, lines, dictionary=None):
        if type(lines) == str:
            lines = [lines.split("\n")]
        
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
            
            if line.startswith("#"):
                #print "COMMENT"
                continue
            
            if self.getValue("VERBOSE") and not line.startswith("silent"):
                print "%s%s: %s" % ("    "*self.stat["indent"], iteration, line),
                
            if line.startswith("silent"):
                #print "line starts with silent"
                line = line[len("silent"):].strip()
                self.w["VERBOSE"] = False
                useWith = True
            
            if "#" in line:
                line = line[:line.find("#")]
            
            
            #handle with statements
            if " with " in line:
                line, withArgs = line.split("with", 1)

                if withArgs:
                    self.stat["indent"] += 1
                    print
                    self.run(withArgs.split(" and "), self.w)
                    self.stat["indent"] -= 1
                    useWith = True
            
            #regular handling
            if line == "clear":
                self.clear()
            elif line.startswith("echo"):
                args = self.stripSeq(line[len("echo"):].split(","))
                self.handleEcho(args, useWith)
            elif line.startswith("save"):
                args = self.stripSeq(line[len("save"):].split(","))
                self.handleSave(args, useWith)
            elif line.startswith("show"):
                args = self.stripSeq(line[len("show"):].split(","))
                self.handleShow(args)
            elif line.startswith("line "):
                args = self.stripSeq(line[len("line"):].split(","))
                self.handleLine(args, useWith)
            elif line.startswith("hline"):
                args = self.stripSeq(line[len("hline"):].split(","))
                self.handleVHLine(args, useWith, "h")
            elif line.startswith("vline"):
                args = self.stripSeq(line[len("vline"):].split(","))
                self.handleVHLine(args, useWith, "v")
            elif line.startswith("circle"):
                args = self.stripSeq(line[len("circle"):].split(","))
                self.handleCircle(args, useWith)
                
            elif line.count("=") > 0:
                self.handleAssignment(line, dictionary)
            else:
                print colored("%sUNKNOWN COMMAND '%s'" % \
                        (self.getIndentString(), line), "yellow")
                
    def handleEcho(self, args, useWith):
        gv = self.getValue
        
        valuesToShow = []
        for arg in args:
            val = gv(arg, useWith)
            valuesToShow.append("%s == %s" % (arg, val))
        
        self.printValueSet(", ".join(valuesToShow), useWith)
    
    def handleSave(self, args, useWith):
        gv = self.getValue
        fileName = eval(args[0]) if len(args) > 0 else gv("FILENAME", useWith)
        
        if len(args) > 1:
            self.printWarning("save: Discarding args %s" % repr(args[1:]))
        
        im = self.getImage()
        if im:
            self.printSuccess("im.save(%s)" % repr(fileName), useWith)
            im.save(fileName)
            
    def handleShow(self, args):
        im = self.getImage()
        if im:
            self.printSuccess("im.show()")
            im.show()
                
    def handleAssignment(self, line, dictionary):
        d = dictionary
        a = self.stripSeq(line.split("="))
        if len(a) == 1:
            #print colored("Error parsing line '%s'" % line, "red")
            self.printError("Can't parse line '%s'" % line)
        elif len(a) == 2:
            d[a[0]] = newVal = eval(a[1])
            newValTypeStr = str(type(newVal))
            
            self.printValueSet("%s = %s%s %s" % \
                    (a[0], a[1], "" if a[0] in d.keys() else " (NEW)",
                    newValTypeStr + d["_ID"]))
        elif len(a) > 2:
            #a = b = c => b = c, a = b
            for i in range(len(a)-1, 1, -1):
                if i == len(a) - 1:
                    d[a[i-1]] = eval(a[i])
                else:
                    d[a[i-1]] = eval(d[a[i]])
        
    def handleCircle(self, args, useWith):
        gv = self.getValue
        x = eval(args[0]) if len(args) > 0 else gv("X", useWith)
        y = eval(args[1]) if len(args) > 1 else gv("Y", useWith)
        r = eval(args[2]) if len(args) > 2 else gv("RADIUS", useWith)
        col = args[2] if len(args) > 2 else gv("COLOR", useWith)
        
        if x is None: self.printError("no x given")
        elif y is None: self.printError("no y given")
        elif r is None: self.printError("no r given")
        elif col is None: self.printError("no col given")
        else:
            self.printSuccess(
            "CIRCLE(x=%s, y=%s, r=%s, col=%s)" % (x, y, r, col), useWith)
            draw = self.getDraw()
            draw.ellipse((x-r/2, y-r/2, x+r/2, y+r/2), fill=col)
            #ellipse(self, xy, fill=None, outline=None)
            
    def handleVHLine(self, args, useWith, vh):
        if vh.lower() != "v" and vh.lower() != "h":
            self.printError("Can't handle line '%s'" % vh)
            return
        
        vh = vh.lower()
        
        gv = self.getValue
        gaoe = self.getArgOrEval
        if vh == "v": #vertical line, only use X value
            x = gaoe(args[0], useWith) if len(args) > 0 else gv("X", useWith)
            col = gaoe(args[1], useWith) if len(args) > 1 else gv("COLOR", useWith)
            if x is None: self.printError("no x given")
            elif col is None: self.printError("no color given")
            else:
                self.printSuccess("VLINE(x=%s)" % x, useWith)
                im = self.getImage()
                draw = self.getDraw()
                draw.line((x, im.size[1], x, im.size[1]), fill=col)
                return True
 
        else: #vh == "h"
            y = gaoe(args[0], useWith) if len(args) > 0 else gv("Y", useWith)
            col = gaoe(args[1], useWith) if len(args) > 1 else gv("COLOR", useWith)
            if y is None: self.printError("no y given")
            elif col is None: self.printError("no color given")
            else:
                self.printSuccess("HLINE(y=%s)" % y, useWith)
                im = self.getImage()
                draw = self.getDraw()
                draw.line((0, y, im.size[0], y), fill=col)
                return True
        
    def handleLine(self, args, useWith):
        gv = self.getValue
        gaoe = self.getArgOrEval
        x1 = gaoe(args[0], useWith) if len(args) > 0 else gv("X", useWith)
        y1 = gaoe(args[1]) if len(args) > 1 else gv("Y", useWith)
        x2 = gaoe(args[2]) if len(args) > 2 else gv("X2", useWith)
        y2 = gaoe(args[3]) if len(args) > 3 else gv("Y2", useWith)
        col = gaoe(args[4]) if len(args) > 4 else gv("COLOR", useWith)
        
        if x1 is None: self.printError("no x1 given")
        elif y1 is None: self.printError("no y1 given")
        elif x2 is None: self.printError("no x2 given")
        elif y2 is None: self.printError("no y2 given")
        elif col is None: self.printError("no col given")
        else:
            self.printSuccess("LINE(x1=%s, y1=%s, x2=%s, y2=%s, col=%s)" % \
                    (x1, y1, x2, y2, col), useWith)
            draw = self.getDraw()
            draw.line((x1, y1, x2, y2), fill=col)
    
def runUnitTests():
    import unittesting
    unittesting.run()

if __name__ == "__main__":
   
    #TODO: add proper argument parsing
    if len(sys.argv) >= 2:
        lines = open(sys.argv[1]).read().split("\n")
    else:
        runUnitTests()
        
        lines = """
        hline 200
        hline
        vline with Y = 800
        Y = 300
        hline
        #echo W, H, FILENAME, LOL with LOL = 3
        
        #RADIUS = 20
        #circle 30
        #circle 30, 40
        #line 10, 10, 400, 400 with COLOR = (0, 192, 0)
        #line 10, 10, 400, 10 with COLOR = (0, 0, 255)
        #line 10, 10, 10, 400 with COLOR = (250, 0, 0)
        #save "out.png"
        #save #default is out.png
        
        #circle 30, 40 with COLOR = (20, 30, 40)
        
        #circle 30, 40
        #line 20, 30, 40, 50
        #line 20, 30 with X2 = 4 and Y2 = 2
        #hline 20
        #line 20, 30 with X2 = 4 and Y2 = 2
        
        #X = 90
        #Y = 99
        #circle with COL = (3, 4, 5)
        """.strip().split("\n")
    
    eglParser = EglParser()
    eglParser.run(lines)
