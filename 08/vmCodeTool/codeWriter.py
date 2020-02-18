"""
Module for writing into assembly (.asm) files
"""

from constants import *
from pathlib import Path


class CodeWriter(object):
    def __init__(self, filename):
        self.filename = None
        self.openFile = open(filename, 'w')
        self.lineNo = 0
        self.staticVar = str(Path(filename).name).split('.')[0]
        self.staticN = 0
        self.nCall = 0
        self.conditionalCount = 0
    
    def setFilename(self, filename):
        self.filename = filename.replace('.vm', '.asm')
        self.staticVar = Path(filename).name

    def write(self, code, strFields=None):
        
        temp = [line for line in (line.strip() for line in code.split('\n')) if len(line)]
        for line in temp:
            if '{'  in line:
                line = line.format(**strFields)
            self.openFile.write(line + '\n')
            self.lineNo += 1
    
    def Close(self):
        self.openFile.close()

    def writeInit(self):
        code = (
            "@256\n"
            "D=A\n"
            "@SP\n"
            "AM=D\n"
            )
        self.write(code)

    def writeLabel(self, cmd, label):
        if cmd == C_LABEL:
            self.write("({label})\n", strFields = {'label': label})
    
    def writeGoto(self, cmd, label):
        if cmd == C_GOTO:
            code = (
                "@{label}\n"
                "0; JMP\n"
            )
            self.write(code, strFields={'label': label})

    def writeIf(self, cmd, label):
        if cmd == C_IF:
            code = (
                "@SP\n"
                "AM=M-1\n"
                "D=M\n"
                "@{label}\n"
                "D;JNE\n"
            )
            self.write(code, strFields={'label': label})
        
    def writeCall(self, cmd, fName, nArgs):
        if cmd == C_CALL:
            code = (
                "@RETURN${fName}${nCall}\n"
                "D=A\n"
                "@SP\n"
                "A=M\n"
                "M=D\n"
                "@SP\n"
                "M=M+1\n"
                "@LCL\n"
                "D=M\n"
                "@SP\n"
                "A=M\n"
                "M=D\n"
                "@SP\n"
                "M=M+1\n"
                "@ARG\n"
                "D=M\n"
                "@SP\n"
                "A=M\n"
                "M=D\n"
                "@SP\n"
                "M=M+1\n"
                "@THIS\n"
                "D=M\n"
                "@SP\n"
                "A=M\n"
                "M=D\n"
                "@SP\n"
                "M=M+1\n"
                "@THAT\n"
                "D=M\n"
                "@SP\n"
                "A=M\n"
                "M=D\n"
                "@SP\n"
                "M=M+1\n"

                "@SP\n"
                "D=M\n"
                "@{nArgs}\n"
                "D=D-A\n"
                "@5\n"
                "D=D-A\n"
                "@ARG\n"
                "M=D\n"
                "@SP\n"
                "D=M\n"
                "@LCL\n"
                "M=D\n"
                "@{fName}\n"
                "0; JMP\n"
                "(RETURN${fName}${nCall})\n"
                )
            strFields = {'fName': fName, 'nArgs': nArgs, 'nCall': self.nCall}
            self.write(code, strFields=strFields)
            self.nCall += 1
    
    def writeFunction(self, cmd, fName, nLocals):
        if cmd == C_FUNCTION:
            code = "({fName})\n"
            self.write(code, strFields={'fName': fName})
            for n in range(int(nLocals)):
                self.writePushPop(C_PUSH, 'constant', 0)
    
    def writeReturn(self, cmd):
        if cmd == C_RETURN:
            code = (
                "@LCL\n"
                "D=M\n"
                "@SAVEFRAME\n"
                "M=D\n"

                "@5\n"
                "D=A\n"
                "@SAVEFRAME\n"
                "D=M-D\n"
                "A=D\n"
                "D=M\n"
                "@RET_ADDR\n" 
                "M=D\n"
            )
            self.write(code)
            self.writePushPop(C_POP, 'argument', 0)

            code = (
                "@ARG\n"
                "D=M+1\n"
                "@SP\n"
                "M=D\n"

                "@1\n"
                "D=A\n"
                "@SAVEFRAME\n"
                "A=M-D\n"
                "D=M\n"
                "@THAT\n"
                "M=D\n"

                "@2\n"
                "D=A\n"
                "@SAVEFRAME\n"
                "A=M-D\n"
                "D=M\n"
                "@THIS\n"
                "M=D\n"

                "@3\n"
                "D=A\n"
                "@SAVEFRAME\n"
                "A=M-D\n"
                "D=M\n"
                "@ARG\n"
                "M=D\n"

                "@4\n"
                "D=A\n"
                "A=M\n"
                "@SAVEFRAME\n"
                "A=M-D\n"
                "D=M\n"
                "@LCL\n"
                "M=D\n"

                "@RET_ADDR\n"
                "A=M\n"
                "0;JMP\n"
                )
            
            self.write(code)


    def writeArithmetic(self, cmd, opType):
        """
        Writes the arithmetic assembly code

        Parameters
        ==========
        cmd: int
            arithmetic operator constant
        opType: str
            arithmetic operator as str e.g., 'add'
        """

        if cmd == C_ARITHMETIC:

            if opType == 'neg':
                code = (
                    "@SP\n"
                    "A=M-1\n"
                    "M=-M\n"
                ) 
            if opType == 'not':
                code = (
                    "@SP\n"
                    "A=M-1\n"
                    "M=!M\n"
                ) 
            if opType == 'add':
                code = (
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    "A=A-1\n"
                    "M=M+D\n"
                )
            if opType == 'sub':
                code = (
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    "A=A-1\n"
                    "M=M-D\n"
                ) 
            if opType == 'and':
                code = (
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    "A=A-1\n"
                    "M=M&D\n"
                ) 
            if opType == 'or':
                code = (
                    "@SP\n"
                    "AM=M-1\n"
                    "D=M\n"
                    "A=A-1\n"
                    "M=M|D\n"
                ) 
            if opType == 'eq':
                code = (
                    "@SP\n"
                    "AM=M-1\n"     
                    "D=M\n"        
                    "A=A-1\n"      
                    "D=M-D\n"      
                    "@EQ_TRUE_{nConditional}\n"
                    "D;JEQ\n"
                    "@SP\n"
                    "A=M-1\n"
                    "M=0\n"
                    "@EQ_FALSE_{nConditional}\n"
                    "0;JMP\n"
                    "(EQ_TRUE_{nConditional})\n"
                    "@SP\n"
                    "A=M-1\n"
                    "M=-1\n"
                    "(EQ_FALSE_{nConditional})\n"
                ) 
            if opType == 'gt':
                code = (
                    "@SP\n"
                    "AM=M-1\n"     
                    "D=M\n"        
                    "A=A-1\n"      
                    "D=M-D\n"      
                    "@GT_TRUE_{nConditional}\n"
                    "D;JGT\n"
                    "@SP\n"
                    "A=M-1\n"
                    "M=0\n"
                    "@GT_FALSE_{nConditional}\n"
                    "0;JMP\n"
                    "(GT_TRUE_{nConditional})\n"
                    "@SP\n"
                    "A=M-1\n"
                    "M=-1\n"
                    "(GT_FALSE_{nConditional})\n"
                )
            if opType == 'lt':
                code = (
                    "@SP\n"
                    "AM=M-1\n"     
                    "D=M\n"        
                    "A=A-1\n"      
                    "D=M-D\n"      
                    "@LT_TRUE_{nConditional}\n"
                    "D;JLT\n"
                    "@SP\n"
                    "A=M-1\n"
                    "M=0\n"
                    "@LT_FALSE_{nConditional}\n"
                    "0;JMP\n"
                    "(LT_TRUE_{nConditional})\n"
                    "@SP\n"
                    "A=M-1\n"
                    "M=-1\n"
                    "(LT_FALSE_{nConditional})\n"
                )
            self.write(code, strFields={
                'nConditional': self.conditionalCount
            })

            if opType in ['eq', 'lt', 'gt']:
                self.conditionalCount += 1

    def writePushPop(self, cmd, segment, index):
        """
        Write stack operations
        """
        if cmd in [C_PUSH, C_POP]:
            if segment == 'constant':
                name = index
                if cmd == C_PUSH:
                    code = (
                        "@{name}\n"
                        "D=A\n"
                        "@SP\n"
                        "A=M\n"
                        "M=D\n"
                        "@SP\n"
                        "AM=M+1\n"
                    )
                elif cmd == C_POP:
                    code = (
                        "@SP\n"
                        "AM=M-1\n"
                        "D=M\n"
                        "@{name}\n"
                        "A=M\n"
                        "M=D\n"
                        )

            elif segment == 'static':
                name = False
                if cmd == C_PUSH:
                    code = (
                        "@R13\n"
                        "M=D\n"
                        "@{staticName}.{index}\n"
                        "D=A\n"
                        "@R14\n"
                        "M=D\n"
                        "@R13\n"
                        "D=M\n"
                        "@R14\n"
                        "A=M\n"
                        "D=M\n"
                        "@SP\n"
                        "A=M\n"
                        "M=D\n"
                        "@SP\n"
                        "AM=M+1\n"
                    )
                elif cmd == C_POP:
                    code = (
                        "@SP\n"
                        "AM=M-1\n"
                        "D=M\n"
                        "@R13\n"
                        "M=D\n"
                        "@{staticName}.{index}\n"
                        "D=A\n"
                        "@R14\n"
                        "M=D\n"
                        "@R13\n"
                        "D=M\n"
                        "@R14\n"
                        "A=M\n"
                        "M=D\n"
                        )
                self.staticN +=1  # Increment static var counter
            elif segment == 'pointer':
                name = False
                if cmd == C_PUSH:
                    code = (
                        "@{index}\n"
                        "D=A\n"
                        "@R3\n"
                        "A=D+A\n"
                        "D=M\n"
                        "@SP\n"
                        "A=M\n"
                        "M=D\n"
                        "@SP\n"
                        "AM=M+1\n"
                    )
                elif cmd == C_POP:
                    code = (
                        "@{index}\n"
                        "D=A\n"
                        "@R3\n"
                        "D=D+A\n"
                        "@R13\n"
                        "M=D\n"
                        "@SP\n"
                        "AM=M-1\n"
                        "D=M\n"
                        "@R13\n"
                        "A=M\n"
                        "M=D\n"
                    )
            elif segment == 'temp':
                name = False
                if cmd == C_PUSH:
                    code = (
                        "@{index}\n"
                        "D=A\n"
                        "@R5\n"
                        "A=D+A\n"
                        "D=M\n"
                        "@SP\n"
                        "A=M\n"
                        "M=D\n"
                        "@SP\n"
                        "AM=M+1\n"
                    )
                elif cmd == C_POP:
                    code = (
                        "@{index}\n"
                        "D=A\n"
                        "@R5\n"
                        "D=D+A\n"
                        "@R13\n"
                        "M=D\n"
                        "@SP\n"
                        "AM=M-1\n"
                        "D=M\n"
                        "@R13\n"
                        "A=M\n"
                        "M=D\n"
                    )
            else:
                name = stackOp[segment]
                if cmd == C_PUSH:
                    code = (
                        "@{index}\n"
                        "D=A\n"
                        "@{name}\n"
                        "A=D+M\n"
                        "D=M\n"
                        "@SP\n"
                        "A=M\n"
                        "M=D\n"
                        "@SP\n"
                        "AM=M+1\n"
                    )
                elif cmd == C_POP:
                    code = (
                        "@{index}\n"
                        "D=A\n"
                        "@{name}\n"
                        "D=D+M\n"
                        "@R13\n"
                        "M=D\n"
                        "@SP\n"
                        "AM=M-1\n"
                        "D=M\n"
                        "@R13\n"
                        "A=M\n"
                        "M=D\n"
                    )

            self.write(code, strFields={
                'name': name,
                'index': index,
                'staticName': self.staticVar
            })
            