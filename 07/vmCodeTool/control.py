"""
Control module for parsing and writing assembly code.
"""

import argparse
from vmParser import ParseVM
from codeWriter import CodeWriter
from constants import *


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    argParser.add_argument('filename', help="The path to the .vm file")
    args = argParser.parse_args()
    
    if not args.filename.endswith(".vm"):
        raise Exception("You can only parse .vm files")
    
    # Create parse object
    vmParseObj = ParseVM(filename=args.filename)
    # Create code writer object
    asmWriter = CodeWriter(filename=args.filename)
    
    while vmParseObj.hasMoreCommands:
        # Get command
        line = vmParseObj.advance
        # Get command type
        cmd = vmParseObj.commandType(line)
        # Get arg 1
        segment = vmParseObj.arg1(line)
        # Get arg 2
        index = vmParseObj.arg2(line)
        # Write comment
        asmWriter.openFile.write("// {}\n".format(line))
        # Write arithmetic (if command is arithmetic)
        asmWriter.writeArithmetic(cmd, segment)
        # Write stack command
        asmWriter.writePushPop(cmd, segment, index)
    # Close file when complete
    asmWriter.openFile.close()
