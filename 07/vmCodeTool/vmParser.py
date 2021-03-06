from constants import *
"""
Module for parsing virtual machine files (.vm), ready for writing into assembly (.asm) files
"""


class ParseVM(object):
    def __init__(self, filename):
        self.filename = filename
        self.input = self.readInput()
        self.index = 0

    def readInput(self):
        with open(self.filename, 'r') as f:
            temp = f.readlines()
        
        # Remove commented and blank lines
        return [line for line in (line.strip() for line in temp) if len(line) and not line.startswith("//")]
        
    @property    
    def hasMoreCommands(self):
        return self.index < len(self.input)
    
    @property
    def advance(self):
        temp = self.input[self.index]
        self.index += 1
        return temp

    def commandType(self, cmd):
        return commandLib[cmd.split()[0]]

    def arg1(self, cmd):
        if not self.commandType(cmd) == C_RETURN:
            temp = cmd.split()
            if len(temp) == 3:
                return temp[1]
            return temp[0]

    def arg2(self, cmd):
        if self.commandType(cmd) in [C_PUSH, C_POP, C_FUNCTION, C_CALL]:
            temp = cmd.split()
            if len(temp) == 3:
                return temp[2]
