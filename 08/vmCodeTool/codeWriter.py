"""
Module for writing into assembly (.asm) files
"""

from constants import *
from pathlib import Path


class CodeWriter(object):
    def __init__(self, filename):
        self.filename = None
        self.setFilename(filename)
        self.openFile = open(self.filename, 'w')
        self.lineNo = 0
        self.staticVar = str(Path(filename).name).split('.')[0]
        self.staticN = 0
    
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
            "@Sys.init\n"
            )
        self.write(code)

    def setFilename(self, filename):
        self.filename = filename.replace('.vm', '.asm')

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
                "D; JNE\n"
            )
            self.write(code, strFields={'label': label})
        
    def writeCall(self, cmd, fName, nArgs):
        if cmd == C_CALL:
            code = (
                "@RETURN_{fName}\n"
                "D=A\n"
                "@SP\n"
                "A=M\n"
                "M=D\n"
                "AM=M+1\n"
                "@LCL\n"
                "D=M\n"
                "@SP\n"
                "A=M\n"
                "M=D\n"
                "AM=M+1\n"
                "@ARG\n"
                "D=M\n"
                "@SP\n"
                "A=M\n"
                "M=D\n"
                "AM=M+1\n"
                "@THIS\n"
                "D=M\n"
                "@SP\n"
                "A=M\n"
                "M=D\n"
                "AM=M+1\n"
                "@THAT\n"
                "D=M\n"
                "@SP\n"
                "A=M\n"
                "M=D\n"
                "AM=M+1\n"
                "@{nArgs}\n"
                "D=A\n"
                "@5\n"
                "D=D-A\n"
                "@SP\n"
                "D=M-D\n"
                "@ARG\n"
                "M=D\n"
                "@SP\n"
                "D=M\n"
                "@LCL\n"
                "M=D\n"
                "@{fName}\n"
                "0; JMP\n"
                "(RETURN_{fname})\n"
                )
            strFields = {'fName': fName, 'nArgs': nArgs}
            self.write(code, strFields=strFields)
    
    def writeFunction(self, cmd, fName, nLocals):
        if cmd == C_FUNCTION:
            code = (
                "({fName})\n"
                "@{nLocals}\n"
                "D=A\n"
                "@R13\n"
                "M=D\n"
                "(LOOP_LOCAL)\n"
                "@0\n"
                "D=A\n"
                "@LCL\n"
                "A=M\n"
                "M=D\n"
                "@R13\n"
                "MD=M-1\n"
                "@LOOP_LOCAL\n"
                "D; JGT\n"
                )
            strFields = {'fName': fName, 'nLocals': nLocals}
            self.write(code, strFields=strFields)
    
    def writeReturn(self, cmd):
        if cmd == C_RETURN:
            code = (
                "@1\n@1\n@1\n@1\n"
                "@LCL\n"
                "D=M\n"
                "@FRAME\n"
                "M=D\n"

                "@5\n"
                "D=A\n"
                "@FRAME\n"
                "A=M-D\n"
                "D=M\n"
                "@RET\n"
                "M=D\n"

                "@SP\n"
                "AM=M-1\n"
                "D=M\n"
                "@ARG\n"
                "A=M\n"
                "M=D\n"
                "@SP\n"

                "@ARG\n"
                "D=M+1\n"
                "@SP\n"
                "M=D\n"

                "@1\n"
                "D=A\n"
                "@FRAME\n"
                "A=M-D\n"
                "D=M\n"
                "@THAT\n"
                "M=D\n"

                "@2\n"
                "D=A\n"
                "@FRAME\n"
                "A=M-D\n"
                "D=M\n"
                "@THIS\n"
                "M=D\n"

                "@3\n"
                "D=A\n"
                "@FRAME\n"
                "A=M-D\n"
                "D=M\n"
                "@ARG\n"
                "M=D\n"

                "@4\n"
                "D=A\n"
                "@FRAME\n"
                "A=M-D\n"
                "D=M\n"
                "@LCL\n"
                "M=D\n"

                "@RET\n"
                "A=D\n"
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
                    "AM=M-1\n"     # Get first value
                    "D=M\n"        # Store it in D
                    "A=A-1\n"      # Go to next value
                    "D=M-D\n"      # Calculate diff, store in M and D
                    "@{trueN}\n"   # Get next line address
                    "D=D;JEQ\n"
                    "@SP\n"
                    "A=M-1\n"
                    "M=0\n"
                    "@{falseN}\n"
                    "0;JMP\n"
                    "@{trueN}\n"   # Get next line address
                    "@SP\n"
                    "A=M-1\n"
                    "M=-1\n"
                    "@{falseN}\n"
                ) 
            if opType == 'gt':
                code = (
                    "@SP\n"
                    "AM=M-1\n"     # Get first value
                    "D=M\n"        # Store it in D
                    "A=A-1\n"      # Go to next value
                    "D=M-D\n"      # Calculate diff, store in M and D
                    "@{trueN}\n"   # Get next line address
                    "D=D;JGT\n"
                    "@SP\n"
                    "A=M-1\n"
                    "M=0\n"
                    "@{falseN}\n"
                    "0;JMP\n"
                    "@{trueN}\n"   # Get next line address
                    "@SP\n"
                    "A=M-1\n"
                    "M=-1\n"
                    "@{falseN}\n"
                )

            if opType == 'lt':
                code = (
                    "@SP\n"
                    "AM=M-1\n"     # Get first value
                    "D=M\n"        # Store it in D
                    "A=A-1\n"      # Go to next value
                    "D=M-D\n"      # Calculate diff, store in M and D
                    "@{trueN}\n"   # Get next line address
                    "D=D;JLT\n"
                    "@SP\n"
                    "A=M-1\n"
                    "M=0\n"
                    "@{falseN}\n"
                    "0;JMP\n"
                    "@{trueN}\n"   # Get next line address
                    "@SP\n"
                    "A=M-1\n"
                    "M=-1\n"
                    "@{falseN}\n"
                )
            self.write(code, strFields={
                'trueN': self.lineNo + 7,
                'falseN': self.lineNo + 6
            })

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
                        "@{staticName}.{index}\n"
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
                        "@{staticName}.{index}\n"
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
            