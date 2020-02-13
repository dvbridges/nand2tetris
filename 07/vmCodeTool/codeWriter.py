"""
Module for writing into assembly (.asm) files
"""

from constants import *


class CodeWriter(object):
    def __init__(self, filename):
        self.filename = None
        self.setFilename(filename)
        self.openFile = open(self.filename, 'w')

    def setFilename(self, filename):
        self.filename = filename.replace('.vm', '.asm')

    def writeArithmetic(self, cmd, line, opType):
        """
        Writes the arithmetic assembly code

        Parameters
        ==========
        cmd: int
            arithmetic operator constant
        line: str
            Full command
        opType: str
            arithmetic operator as str e.g., 'add'
        """
        operation = {}
        operation['add'] = 'D=D+M'
        operation['sub'] = 'D+D-M'
        operation['and'] = 'D=D&M'
        operation['or'] = 'D=D|M'
        operation['eq'] = 'D;JEQ'
        operation['gt'] = 'D;JGT'
        operation['lt'] = 'D;JLT'
        operation['neg'] = 'D=-D'
        operation['not'] = 'D=!D'
        code = "// {line}\n"

        if cmd == C_ARITHMETIC:
            
            # Unary ops do not need two stack operations
            if opType not in ['neg', 'not']:            
                code += (
                    "@sp\n"
                    "M=M-1\n"
                    "A=M\n"
                    "D=M\n"
                    )
            code += (
                "@sp\n"
                "M=M-1\n"
                "A=M\n"
                "{op}\n"
                "@sp\n"
                "A=M\n"
                "M=D\n"
                )
            
            self.openFile.write(
                code.format(
                    line=line,
                    op=operation[opType]))

    def writePushPop(self, cmd, segment, index):
        """
        Push constant 2:
        @2
        D = A
        @sp
        A = M
        M = D
        @sp
        M = M + 1
        """
        if cmd == C_PUSH:
            code = (
                "// {segment}\n"
                "@{index}\n"
                "D=A\n"
                "@sp\n"
                "A=M\n"
                "M=D\n"
                "@sp\n"
                "M=M+1\n"
            )
        else:
            return

        self.openFile.write(
            code.format(
                segment=segment,
                index=index
                ))