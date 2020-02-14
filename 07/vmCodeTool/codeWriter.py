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

    def setFilename(self, filename):
        self.filename = filename.replace('.vm', '.asm')

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
                    "AM=M-1\n"      # Get first value
                    "D=M\n"         # Store it in D
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
                    "AM=M-1\n"      # Get first value
                    "D=M\n"         # Store it in D
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
                    "AM=M-1\n"      # Get first value
                    "D=M\n"         # Store it in D
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
            temp = [line for line in (line.strip() for line in code.split()) if len(line)]
            for line in temp:
                if '{' in line:
                    line = line.format(
                        trueN=(self.lineNo + 7),
                        falseN=(self.lineNo + 6))
                self.openFile.write(line + '\n')
                self.lineNo += 1

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
                        "@{staticName}.{staticN}\n"
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
                        "@{staticName}.{staticN}\n"
                        "A=M\n"
                        "M=D\n"
                        )
                self.staticN +=1                
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
                        "MD=D+M\n"
                        "@SP\n"
                        "AM=M-1\n"
                        "D=M\n"
                        "@{name}\n"
                        "A=M\n"
                        "M=D\n"
                        "@{index}\n"
                        "D=A\n"
                        "@{name}\n"
                        "M=M-D\n"
                    )

            temp = [line for line in (line.strip() for line in code.split()) if len(line)]
            for line in temp:
                if '{' in line:
                    line = line.format(
                        name=name,                     
                        index=index,
                        staticName=self.staticVar,
                        staticN=self.staticN
                        )
                self.openFile.write(line + '\n')
                self.lineNo += 1