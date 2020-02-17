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
    asmWriter.writeInit()

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
        # Write label
        asmWriter.writeLabel(cmd, segment)
        # write GOTO
        asmWriter.writeGoto(cmd, segment)
        # write IF
        asmWriter.writeIf(cmd, segment)
        # Write calls to functions
        asmWriter.writeCall(cmd, segment, index)
        # Write functions
        asmWriter.writeFunction(cmd, segment, index)
        # write Return
        asmWriter.writeReturn(cmd)
        # Write arithmetic (if command is arithmetic)
        asmWriter.writeArithmetic(cmd, segment)
        # Write stack command
        asmWriter.writePushPop(cmd, segment, index)
    # Close file when complete
    asmWriter.openFile.close()
