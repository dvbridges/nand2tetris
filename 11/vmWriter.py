from pathlib import Path

class VMWriter(object):
    def __init__(self, fileName):
        self.outputFilePath = None
        self.setOutputPaths(fileName)
        self.openFile(self.outputFilePath)
    
    def setOutputPaths(self, fileName):
        f = Path(fileName)
        print("Compiling {}...".format(f))
        self.outputFilePath = str(f.parent / f.stem) + '.vm'

    def openFile(self, fileName):
        self.outputFile = open(fileName, 'w+')

    def closeFile(self):
        self.outputFile.close()

    def writePush(self, first, second=0):
        if first.startswith('this'):
            self.outputFile.write("push argument 0\n")
            self.outputFile.write("pop pointer 0\n")

        self.outputFile.write("push {} {}\n".format(first, second))

    def writePop(self, first, second=0):
        self.outputFile.write("pop {} {}\n".format(first, second))

    def writeArithmetic(self, command):
        self.outputFile.write(command + '\n') 
    
    def writeLabel(self, label):
        self.outputFile.write("label {}\n".format(label))
    
    def writeGoto(self, label):
        self.outputFile.write("goto {}\n".format(label))
    
    def writeIf(self, label):
        self.outputFile.write("if-goto {}\n".format(label))
    
    def writeCall(self, name, args=None):
        if args in [None, 0] :
            args = 0 

        self.outputFile.write("call {} {}\n".format(name, args))
    
    def writeFunction(self, name, nLocals):
        self.outputFile.write("// function {}\n".format(name, nLocals))
        self.outputFile.write("function {} {}\n".format(name, nLocals))
    
    def writeReturn(self):
        self.outputFile.write("return\n")
    