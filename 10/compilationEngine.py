import sys

from jackTokenizer import *


class CompilationEngine(object):
    def __init__(self, fileName):
        self.tokenizer = JackTokenizer(fileName)

    
    def write(self):
        with open("testDoc.xml", 'w') as f:
            while self.tokenizer.hasMoreTokens:
                self.tokenizer.advance()
                tag = ''
                token = ''
                if self.tokenizer.tokenType == KEYWORD:
                    tag = 'keyword'
                    token = self.tokenizer.keyWord
                elif self.tokenizer.tokenType == SYMBOL:
                    tag = 'symbol'
                    token = self.tokenizer.symbol
                elif self.tokenizer.tokenType == IDENTIFIER:
                    tag = 'identifier'
                    token = self.tokenizer.identifier
                elif self.tokenizer.tokenType == INT_CONST:
                    tag = 'integerConstant'
                    token = self.tokenizer.intVal
                elif self.tokenizer.tokenType == STRING_CONST:
                    tag = 'stringConstant'
                    token = self.tokenizer.stringVal

                if len(token):
                    f.write("<{tag}>{token}</{tag}>\n".format(tag=tag, token=token))


if __name__ == "__main__":
    arg = sys.argv[1]
    eng = CompilationEngine(arg)

    eng.write()