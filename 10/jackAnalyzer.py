import sys
from compilationEngine import CompilationEngine
from pathlib import Path

class JackAnalyzer(object):
    def __init__(self):
        pass


if __name__ == "__main__":
    args = sys.argv[1]

    files = Path(args)    
    if files.is_dir():
        filePath = list(Path(files.name).glob('**/*.jack'))
        for eachFile in filePath:
            compiler = CompilationEngine(eachFile)
            compiler.closeFile()
    else:
        compiler = CompilationEngine(files)
        compiler.closeFile()





