import sys
import argparse


# Constants
A_COMMAND = 0
C_COMMAND = 1
L_COMMAND = 2

jumpDict = {}
jumpDict['null'] = '000'
jumpDict['JMP'] = '111'
jumpDict['JGT'] = '001'
jumpDict['JEQ'] = '010'
jumpDict['JGE'] = '011'
jumpDict['JLT'] = '100'
jumpDict['JNE'] = '101'
jumpDict['JLE'] = '110'

controlDict_0 = {}
controlDict_1 = {}

symbolTable = {}
symbolTable['SP'] = 0
symbolTable['LCL'] = 1
symbolTable['ARG'] = 2
symbolTable['THIS'] = 3
symbolTable['THAT'] = 4
symbolTable['R0'] = 0
symbolTable['R1'] = 1
symbolTable['R2'] = 2
symbolTable['R3'] = 3
symbolTable['R4'] = 4
symbolTable['R5'] = 5
symbolTable['R6'] = 6
symbolTable['R7'] = 7
symbolTable['R8'] = 8
symbolTable['R9'] = 9
symbolTable['R10'] = 10
symbolTable['R11'] = 11
symbolTable['R12'] = 12
symbolTable['R13'] = 13
symbolTable['R14'] = 14
symbolTable['R15'] = 15
symbolTable['SCREEN'] = 16384
symbolTable['KBD'] = 24576


class SymbolTable():
    """
    Responsible for symbol table operations.
    """
    def __init__(self):
        self.table = symbolTable
        self.index = 16

    def addEntry(self, val, idx=None):
        if not self.contains(val):
            if idx is not None:
                self.table[val] = idx
            else:
                self.table[val] = self.index
                self.index += 1

    def contains(self, val):
        return val in self.table

    def getAddress(self, val):
        return self.table[val]


## Get control codes from text file
with open("controls.txt") as f:
    for line in f:
        temp = line.strip().split(',')
        controlDict_0[temp[0]] = temp[1]
        if len(temp[2]):
            controlDict_1[temp[2]] = temp[1]


class Parser(object):
    def __init__(self, filename):
        self.filename = filename
        self.outputFile = self.filename.replace('asm', 'hack')
        self.input = self.readInput()
        self.symbolTable = SymbolTable()
        self.indexLabels()
        self.nLines = len(self.input)
        self.currentLine = -1  
        self.currentCommand = None 
        self.writeOutput()

    def writeOutput(self):
        """
        Write output to hack file
        """
        with open(self.outputFile, 'w') as f:
            while self.advance():
                if self.commandType == L_COMMAND:
                    continue
                elif self.commandType == A_COMMAND:
                    temp = self.address
                elif self.commandType == C_COMMAND:
                    temp = '{types}11{comp}{dest}{jump}'.format(
                        types=self.commandType,
                        comp=self.comp,
                        dest=self.dest,
                        jump=self.jump)
                f.write(temp)
                f.write('\n')

    def readInput(self):
        """
        Reads input file into list

        Returns
        -------
        List
            All lines in file
        """
        with open(self.filename, 'r') as f:
            lines = [line.strip() for line in f.readlines() if len(line.strip()) and not line.startswith('//')]
            # Remove comments from lines
            return [line.split('//')[0] for line in lines]

    def indexLabels(self):
        """
        Add label address to ROM
        """
        counter = 0
        for val in self.input:
            if val.startswith('('):
                temp = val.strip()[1:-1]
                if not self.symbolTable.contains(temp):
                    self.symbolTable.addEntry(temp, counter)
            else:
                counter += 1
                
    @property
    def hasMoreCommands(self):
        """
        Returns bool showing if more command lines can be processed from input
        """
        return self.currentLine < (self.nLines)
    
    def advance(self):
        """
        Get next line
        """
        self.currentLine += 1
        if self.hasMoreCommands:
            self.currentCommand = self.input[self.currentLine].strip().replace(' ', '')
            return True
        else:
            return False

    @property
    def commandType(self):
        """
        Return command type.
        """
        if self.currentCommand.startswith('@'):
            return A_COMMAND
        elif '=' in self.currentCommand or ';' in self.currentCommand:
            return C_COMMAND
        elif self.currentCommand.startswith('('):
            return L_COMMAND

    @property
    def symbol(self):
        val = symbolTable[self.currentCommand[1:-1]]
        return f'0{val:015b}'

    @property
    def address(self):
        """
        Take int, or find symbol address in table, 
        and convert to binary address.
        """
        val = self.currentCommand.split('@')[-1]

        # If isdigit, this is a normal address
        if val.isdigit():
            return f'0{int(val):015b}'

        # This is a variable, load into symbol table
        if not self.symbolTable.contains(val):
            self.symbolTable.addEntry(val)
        return f'0{self.symbolTable.getAddress(val):015b}'

    @property
    def dest(self):
        """
        Construct dest code in binary
        """
        destStr = ''
        if '=' in self.currentCommand:
            destCode = list(self.currentCommand.split('=')[0])
        else:
           return '000' 

        destCode = [code.upper() for code in destCode]

        for code in ['A', 'D', 'M']:
            if code in destCode:
                destStr += '1'
            else:
                destStr += '0'
        return destStr

    @property
    def comp(self):
        
        """
        Construct c-instruction in binary
        """
        if '=' in self.currentCommand:
            compCode = self.currentCommand.split('=')[1]
        else:
            compCode = self.currentCommand.split(';')[0]

        if compCode.upper() in controlDict_0:
            code = '0'
            code += controlDict_0[compCode.upper()]
        else:
            code = '1'
            code += controlDict_1[compCode.upper()]
        return code

    @property
    def jump(self):
        """
        Construct jump instruction in binary
        """
        if '=' in self.currentCommand:
            return jumpDict['null']

        jumpCode = self.currentCommand.split(';')[-1].upper()

        if jumpCode not in jumpDict:
            return jumpDict['null']
        return jumpDict[jumpCode]


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("filename", help="You must add the .asm file as a positional argument")

    try:
        args = argparser.parse_args()
    except SystemExit:
        print("Please enter an assembly file to parse.")
        sys.exit()

    if not args.filename.endswith(".asm"):
        raise TypeError("You can only parse assembly files (*.asm)")

    asmParser = Parser(args.filename)