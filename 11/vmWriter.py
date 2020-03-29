from pathlib import Path

class VMWriter(object):
    def __init__(self, fileName):
        self.outputFilePath = None
        self.setOutputPaths(fileName)
        self.openFile(self.outputFilePath)
    
    def setOutputPaths(self, fileName):
        f = Path(fileName)
        if not Path.exists(f.parent / "_compiled"):
            Path.mkdir(f.parent / "_compiled") 
        self.outputFilePath = str(f.parent / "_compiled" / f.stem) + '.vm'

    def openFile(self, fileName):
        self.outputFile = open(fileName, 'w+')

    def closeFile(self):
        self.outputFile.close()

    def writePush(self, segment):
        if segment.startswith('this '):
            self.outputFile.write("push argument 0\n")
            self.outputFile.write("pop pointer 0\n")

        self.outputFile.write("push {}\n".format(segment))

    def writePop(self, segment):
        self.outputFile.write("pop {}\n".format(segment))

    def writeArithmetic(self, command):
        self.outputFile.write(command + '\n') 
    
    def writeLabel(self, label):
        pass
    
    def writeGoto(self, label):
        pass
    
    def writeIf(self, label):
        pass
    
    def writeCall(self, name, args):
        self.outputFile.write("call {} {}\n".format(name, args))
    
    def writeFunction(self, name, nLocals):
        pass
    
    def writeReturn(self):
        pass
    