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
        self.nLines = len(self.input)
        self.currentLine = -1  
        self.currentCommand = None 
        self.writeOutput()

    def writeOutput(self):
        """
        Write output to hack file
        """
        with open(self.outputFile, 'w') as f:
            for idx, line in enumerate(range(self.nLines)):
                self.advance()
                if self.commandType == A_COMMAND:
                    temp = self.address
                elif self.commandType == C_COMMAND:
                    temp = '{types}11{comp}{dest}{jump}'.format(
                        types=self.commandType,
                        comp=self.comp,
                        dest=self.dest,
                        jump=self.jump,
                    )
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
        with open("exampleAssembly.asm", 'r') as f:
            return [line for line in f.readlines() if len(line.strip())]

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
        else:
            return L_COMMAND

    def symbol(self):
        pass

    @property
    def address(self):
        if self.commandType == A_COMMAND:
            val = int(self.currentCommand.split('@')[-1])
            return f'0{val:015b}'

    @property
    def dest(self):
        """
        Construct dest code in binary
        """
        destStr = ''
        if self.commandType == C_COMMAND:
            if '=' in self.currentCommand:
                destCode = list(self.currentCommand.split('=')[0])
            else:
                destCode = list(self.currentCommand.split(';')[0])
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
        if self.commandType == C_COMMAND:
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
        if self.commandType == C_COMMAND:
            if '=' in self.currentCommand:
                return jumpDict['null']
            jumpCode = self.currentCommand.split(';')[-1].upper()
            if jumpCode not in jumpDict:
                return jumpDict['null']
            return jumpDict[jumpCode]
        return jumpDict['null']


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