import sys
import os
from pathlib import Path

from jackTokenizer import *


class CompilationEngine(object):
    def __init__(self, fileName):
        self.outputFilePath = None
        self.setOutputPaths(fileName)
        self.openFile(self.outputFilePath)

        self.tokenizer = JackTokenizer(fileName)
        self.indent = 0
        self.tokenizer.advance()
        self.compileClass()

    def setOutputPaths(self, fileName):
        f = Path(fileName)
        if not Path.exists(f.parent / "_compiled"):
            Path.mkdir(f.parent / "_compiled") 
        self.outputFilePath = str(f.parent / "_compiled" / f.stem) + '.xml'

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
        
        self.write(tag='keyword',token=self.tokenizer.keyWord)
        self.tokenizer.advance()

        self.write(tag='identifier',token=self.tokenizer.identifier)
        self.tokenizer.advance()

        self.write(tag='symbol', token=self.tokenizer.symbol)
        self.tokenizer.advance()

        while (self.tokenizer.keyWord in ['static', 'field']):
            self.compileClassVarDec()

        while (self.tokenizer.keyWord in ['constructor', 'function', 'method', 'void']):
            self.compileSubroutine()

        self.write(tag='symbol', token=self.tokenizer.symbol)
        self.tokenizer.advance()

        self.write('class', startTag=False)
        self.tokenizer.advance()

    def compileClassVarDec(self):
        # Opening tag
        self.write(tag='classVarDec')

        self.write('keyword', self.tokenizer.keyWord)
        self.tokenizer.advance()

        if self.tokenizer.tokenType == KEYWORD:
            self.write('keyword', self.tokenizer.keyWord)
        else:
            self.write('identifier', self.tokenizer.identifier)
        self.tokenizer.advance()

        self.write('identifier', self.tokenizer.identifier)
        self.tokenizer.advance()

        extraVars = True
        while extraVars:
            if self.tokenizer.currentToken == ',':

                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()

                self.write('identifier', self.tokenizer.identifier)
                self.tokenizer.advance()
            else:
                extraVars = False

        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        # Closing tag
        self.write(tag='classVarDec', startTag=False)

    def compileSubroutine(self):
        # Opening tag
        self.write(tag='subroutineDec')

        self.write('keyword', self.tokenizer.keyWord)
        self.tokenizer.advance()

        if self.tokenizer.tokenType == KEYWORD:
            self.write('keyword', self.tokenizer.keyWord)
        else:
            self.write('identifier', self.tokenizer.identifier)
        self.tokenizer.advance()

        self.write('identifier', self.tokenizer.identifier)
        self.tokenizer.advance()

        # Open param brackets
        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        # write parameterList
        self.compileParameterList() 

        # Close param brackets
        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        # Write subroutine body, open curly brackets
        self.write(tag='subroutineBody')

        self.write('symbol', token=self.tokenizer.symbol)
        self.tokenizer.advance()

        # Write variable declarations
        self.compileVarDec()
        
        # write statements
        self.compileStatements()

        # close subroutine body
        self.write('symbol', token=self.tokenizer.symbol)
        self.tokenizer.advance()
        self.write(tag='subroutineBody', startTag=False)

        # Closing tag
        self.write(tag='subroutineDec', startTag=False)

    def compileVarDec(self):
        
        if self.tokenizer.currentToken != 'var':
            return

        variableDecs = True
        while variableDecs:
            # Write var declarations
            if self.tokenizer.currentToken != 'var':
                variableDecs = False
                break

            # Write starting vardec tag 
            self.write('varDec')

            self.write('keyword', self.tokenizer.keyWord)
            self.tokenizer.advance()

            if self.tokenizer.tokenType == KEYWORD:
                self.write('keyword', self.tokenizer.keyWord)
            else:
                self.write('identifier', self.tokenizer.identifier)
            self.tokenizer.advance()

            self.write('identifier', self.tokenizer.identifier)
            self.tokenizer.advance()

            extraVars = True
            while extraVars:
                if self.tokenizer.currentToken == ',':

                    self.write('symbol', self.tokenizer.symbol)
                    self.tokenizer.advance()

                    self.write('identifier', self.tokenizer.identifier)
                    self.tokenizer.advance()
                else:
                    extraVars = False

            self.write('symbol', token=self.tokenizer.symbol)
            self.tokenizer.advance()

            # Write ending vardec tag 
            self.write('varDec', startTag=False)

    def compileStatements(self):
        writeStatements = self.tokenizer.currentToken in ['if', 'else', 'let', 'do', 'while', 'return']
        if not writeStatements:
            return

        # Write starting statements tag 
        self.write('statements')

        while writeStatements:
            writeStatements = self.tokenizer.currentToken in ['if', 'else', 'let', 'do', 'while', 'return']
            if not writeStatements:
                break

            if self.tokenizer.currentToken in ['if', 'else']:
                self.compileIf()
            elif self.tokenizer.currentToken in ['let']:
                self.compileLet() 
            elif self.tokenizer.currentToken in ['do']:
                self.compileDo() 
            elif self.tokenizer.currentToken in ['while']:
                self.compileWhile() 
            elif self.tokenizer.currentToken in ['return']:
                self.compileReturn() 

        # Write ending statements tag 
        self.write('statements', startTag=False)

    def compileDo(self):
        # Write starting tag
        self.write('doStatement')

        self.write('keyword', self.tokenizer.keyWord)
        self.tokenizer.advance()

        doStatement = True
        while doStatement:
            if self.tokenizer.lookAhead() == '(':
                # subroutine call 1
                self.write('identifier', self.tokenizer.identifier)
                self.tokenizer.advance()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
                self.compileExpressionList()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
            elif self.tokenizer.lookAhead() == '.':
                # subroutine call 2
                self.write('identifier', self.tokenizer.identifier)
                self.tokenizer.advance()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
                self.write('identifier', self.tokenizer.identifier)
                self.tokenizer.advance()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
                self.compileExpressionList()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()

            if self.tokenizer.currentToken == ';':
                doStatement = False
                break
        
        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        # Write closing tag
        self.write('doStatement', startTag=False)

    def compileLet(self):
        # write starting tag
        self.write('letStatement')

        self.write('keyword', self.tokenizer.keyWord)
        self.tokenizer.advance()

        self.write('identifier', self.tokenizer.identifier)
        self.tokenizer.advance()

        if self.tokenizer.currentToken == '[':
            self.write('symbol', self.tokenizer.symbol)
            self.tokenizer.advance()

            self.compileExpression()

            self.write('symbol', self.tokenizer.symbol)
            self.tokenizer.advance()
        
        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        self.compileExpression()

        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        # write closing tag
        self.write('letStatement', startTag=False)

    def compileWhile(self):
        # Compile opening tag
        self.write('whileStatement')

        self.write('keyword', self.tokenizer.keyWord)
        self.tokenizer.advance()

        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        self.compileExpression()

        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        self.compileStatements()

        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        # Compile closing tag
        self.write('whileStatement', startTag=False)

    def compileReturn(self):
        # write starting tag
        self.write('returnStatement')

        self.write('keyword', self.tokenizer.keyWord)
        self.tokenizer.advance()

        if self.tokenizer.currentToken != ';':
            self.compileExpression()

        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        # Write closing tag
        self.write('returnStatement', startTag=False)

    def compileIf(self):
        # Compile opening tag
        self.write('ifStatement')

        self.write('keyword', self.tokenizer.keyWord)
        self.tokenizer.advance()

        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        self.compileExpression()

        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        self.compileStatements()

        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        if self.tokenizer.currentToken == 'else':
            self.write('keyword', self.tokenizer.keyWord)
            self.tokenizer.advance()

            self.write('symbol', self.tokenizer.symbol)
            self.tokenizer.advance()

            self.compileStatements()

            self.write('symbol', self.tokenizer.symbol)
            self.tokenizer.advance()
        
        # Compile closing tag
        self.write('ifStatement', startTag=False)

    def compileExpression(self):
        # write opening tag
        self.write('expression')
        self.compileTerm()

        # write more terms
        op = self.tokenizer.currentToken in OPERATORS
        while op:
            if self.tokenizer.currentToken in CONVERT_SYMBOL:
                self.write('symbol', CONVERT_SYMBOL[self.tokenizer.currentToken])
            else:
                self.write('symbol', self.tokenizer.currentToken)
            self.tokenizer.advance()
            self.compileTerm()
            op = self.tokenizer.currentToken in OPERATORS

        # Compile closing tag
        self.write('expression', startTag=False)

    def compileTerm(self):
        # compile starting tag
        self.write('term')

        if self.tokenizer.tokenType == KEYWORD:
            self.write('keyword', self.tokenizer.keyWord)
            self.tokenizer.advance()
        elif self.tokenizer.tokenType == INT_CONST:
            self.write('integerConstant', self.tokenizer.intVal)
            self.tokenizer.advance()
        elif self.tokenizer.tokenType == STRING_CONST:
            self.write('stringConstant', self.tokenizer.stringVal)
            self.tokenizer.advance()
        elif self.tokenizer.currentToken in UN_OP:
            self.write('symbol', self.tokenizer.symbol)
            self.tokenizer.advance()
            self.compileTerm()
        else:
            if self.tokenizer.currentToken == '(':
                # Simple expression : ( expression )
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
                self.compileExpression()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
            elif self.tokenizer.lookAhead() == '[':
                # Varname [ expression ]
                self.write('identifier', self.tokenizer.identifier)
                self.tokenizer.advance()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
                self.compileExpression()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
            elif self.tokenizer.lookAhead() == '(':
                # subroutine call 1
                self.write('identifier', self.tokenizer.identifier)
                self.tokenizer.advance()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
                self.compileExpressionList()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
            elif self.tokenizer.lookAhead() == '.':
                # subroutine call 2
                self.write('identifier', self.tokenizer.identifier)
                self.tokenizer.advance()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
                self.write('identifier', self.tokenizer.identifier)
                self.tokenizer.advance()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
                self.compileExpressionList()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
            else:
                self.write('identifier', self.tokenizer.identifier)
                self.tokenizer.advance()

        # Compile closing tag
        self.write('term', startTag=False)

    def compileParameterList(self):
        # Write starting tag
        self.write('parameterList')

        paramList = True
        while paramList:
            
            if self.tokenizer.currentToken == ')':
                paramList = False
                break

            self.write('keyword', self.tokenizer.keyWord)
            self.tokenizer.advance()

            self.write('identifier', self.tokenizer.identifier)
            self.tokenizer.advance()            

            if self.tokenizer.currentToken == ',':
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()

        self.write('parameterList', startTag=False)

    def compileExpressionList(self):
        # Write starting tag
        self.write('expressionList')

        expList = True
        while expList:
            if self.tokenizer.currentToken == ')':
                expList = False
                break
            
            self.compileExpression()

            if self.tokenizer.currentToken == ',':
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
        
        self.write('expressionList', startTag=False)


if __name__ == "__main__":
    arg = sys.argv[1]
    eng = CompilationEngine(arg)
    eng.closeFile()