import sys

from jackTokenizer import *


class CompilationEngine(object):
    def __init__(self, fileName):
        self.tokenizer = JackTokenizer(fileName)
        self.indent = 0
        self.outputFile = None
        self.openFile('testDoc.xml')
        self.tokenizer.advance()
        self.compileClass()
        
    
    def writeTestXML(self):
        with open("testDoc.xml", 'w') as f:
            f.write("<tokens>\n")
            while self.tokenizer.hasMoreTokens:
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
                    f.write("<{tag}> {token} </{tag}>\n".format(tag=tag, token=token))
                self.tokenizer.advance()
            f.write("</tokens>\n")

    def openFile(self, fileName):
        self.outputFile = open(fileName, 'w+')

    def writeIndent(self):
        # Write indentation
        temp = '  ' * self.indent
        self.outputFile.write(temp)

    def write(self, tag=None, token=None, startTag=True):

        if token is None and startTag:
            self.writeIndent()
            self.outputFile.write('<{tag}>\n'.format(tag=tag))
            self.indent += 1
        elif token is None and not startTag:
            self.indent -= 1
            self.writeIndent()
            self.outputFile.write('</{tag}>\n'.format(tag=tag))
        else:
            self.writeIndent()
            self.outputFile.write('<{tag}> {token} </{tag}>\n'.format(
                tag=tag,
                token=token)
                )
        
    def closeFile(self):
        self.outputFile.close()
    
    def compileClass(self):
        if not self.tokenizer.keyWord == 'class':
            return

        self.write(tag='class', startTag=True)
        self.tokenizer.advance()
        
        self.write(tag='className',token=self.tokenizer.currentToken)
        self.tokenizer.advance()

        self.write(tag='symbol', token=self.tokenizer.symbol)
        self.tokenizer.advance()

        while (self.tokenizer.keyWord in ['static', 'field']):
            self.compileClassVarDec()

        while (self.tokenizer.keyWord in ['constructor', 'function', 'method', 'void']):
            self.compileSubroutine()

        self.write('class', startTag=False)
        self.tokenizer.advance()

    def compileClassVarDec(self):
        # Opening tag
        self.write(tag='classVarDec')

        self.write('keyword', self.tokenizer.keyWord)
        self.tokenizer.advance()

        self.write('keyword', self.tokenizer.currentToken)
        self.tokenizer.advance()

        self.write('identifier', self.tokenizer.identifier)
        self.tokenizer.advance()

        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        # Closing tag
        self.write(tag='classVarDec', startTag=False)

    def compileSubroutine(self):
        # Opening tag
        self.write(tag='subroutineDec')

        self.write('keyword', self.tokenizer.keyWord)
        self.tokenizer.advance()

        self.write('keyword', self.tokenizer.currentToken)
        self.tokenizer.advance()

        self.write('identifier', self.tokenizer.identifier)
        self.tokenizer.advance()

        # Open param brackets
        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        # write parameterList
        if self.tokenizer.currentToken != ')':
            self.compileParameterList() 

        # Close param brackets
        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        # Write subroutine body, open curly brackets
        self.write('symbol', token=self.tokenizer.symbol)
        self.tokenizer.advance()

        # Write variable declarations
        self.compileVarDec()
        
        # write statements
        self.compileStatements()

        # close subroutine body
        self.write('symbol', token=self.tokenizer.symbol)
        self.tokenizer.advance()

        # Closing tag
        self.write(tag='subroutineDec', startTag=False)

    def compileVarDec(self):
        # Write var declarations
        if self.tokenizer.keyWord != 'var':
            return

        # Write starting vardec tag 
        self.write('varDec')

        variableDecs = True
        while variableDecs:
            self.write('keyword', self.tokenizer.keyWord)
            self.tokenizer.advance()

            self.write('keyword', self.tokenizer.currentToken)
            self.tokenizer.advance()

            self.write('identifier', self.tokenizer.identifier)
            self.tokenizer.advance()

            extraVars = True
            while extraVars:
                if self.tokenizer.currentToken != ',':
                    extraVars = False
                    break

                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()

                self.write('identifier', self.tokenizer.identifier)
                self.tokenizer.advance()

            if self.tokenizer.currentToken == ';':
                variableDecs = False
                break
        
        self.write('symbol', token=self.tokenizer.symbol)
        self.tokenizer.advance()

        # Write ending vardec tag 
        self.write('varDec', startTag=False)

    def compileStatements(self):
        pass

    def compileDo(self):
        pass

    def compileLet(self):
        pass

    def compileWhile(self):
        pass

    def compileReturn(self):
        pass

    def compileIf(self):
        pass

    def compileExpression(self):
        pass

    def compileTerm(self):
        pass
    
    def compileParameterList(self):
        # Write starting tag
        self.write('parameterList')

        paramList = True
        while paramList:

            self.write('keyword', self.tokenizer.keyWord)
            self.tokenizer.advance()

            self.write('identifier', self.tokenizer.identifier)
            self.tokenizer.advance()
            
            if self.tokenizer.currentToken == ')':
                paramList = False
                break

            self.write('symbol', self.tokenizer.symbol)
            self.tokenizer.advance()
        
        self.write('parameterList', startTag=False)

    def compileExpressionList(self):
        pass


if __name__ == "__main__":
    arg = sys.argv[1]
    eng = CompilationEngine(arg)
    eng.closeFile()