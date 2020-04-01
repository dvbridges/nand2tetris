import sys
from compilationEngine import CompilationEngine
from jackTokenizer import JackTokenizer
from symbolTable import SymbolTable
from vmWriter import VMWriter
from pathlib import Path

class JackCompiler(object):
    def __init__(self):
        pass


if __name__ == "__main__":
    args = sys.argv[1]

    files = Path(args)    
    if files.is_dir():
        filePath = list(Path(files.name).glob('**/*.jack'))
        for eachFile in filePath:
            compiler = CompilationEngine(eachFile, JackTokenizer, SymbolTable, VMWriter)
            compiler.start()
            compiler.vmWriter.closeFile()
    else:
        compiler = CompilationEngine(files, JackTokenizer, SymbolTable, VMWriter)
        compiler.start()
        compiler.vmWriter.closeFile()





