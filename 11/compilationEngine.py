import sys
import os
from pathlib import Path

from jackTokenizer import *

OP_CONVERSION = {}
OP_CONVERSION['+'] = 'add'
OP_CONVERSION['-'] = 'sub'
OP_CONVERSION['~'] = 'neg'  # TODO: check if this causes error i.e, using neg instead of not
OP_CONVERSION['='] = 'eq'
OP_CONVERSION['>'] = 'gt'
OP_CONVERSION['<'] = 'lt'
OP_CONVERSION['&'] = 'and'
OP_CONVERSION['|'] = 'or'
OP_CONVERSION['*'] = 'call Math.multiply 2'
OP_CONVERSION['/'] = 'call Math.divide 2'

VM_TYPES = {}
VM_TYPES['var'] = 'local'
VM_TYPES['argument'] = 'argument'
VM_TYPES['static'] = 'static'
VM_TYPES['field'] = 'this'


class CompilationEngine(object):
    def __init__(self, fileName, tokenizer, SymbolTable, vmWriter):
        self.outputFilePath = None
        self.setOutputPaths(fileName)
        self.openFile(self.outputFilePath)

        self.tokenizer = tokenizer(fileName)
        self.classTable = SymbolTable()
        self.subroutineTable = SymbolTable()
        self.vmWriter = vmWriter(fileName)
        self.className = None

        self.indent = 0
        self.labelIndex = -1
        self.tokenizer.advance()
    
    def start(self):
        self.compileClass()

    def setOutputPaths(self, fileName):
        f = Path(fileName)
        if not Path.exists(f.parent / "_compiled"):
            Path.mkdir(f.parent / "_compiled") 
        self.outputFilePath = str(f.parent / "_compiled" / f.stem) + '.xml'

    def openFile(self, fileName):
        self.outputFile = open(fileName, 'w+')
    
    def closeFile(self):
        self.outputFile.close()

    def writeIndent(self):
        # Write indentation
        temp = '  ' * self.indent
        self.outputFile.write(temp)

    def write(self, tag=None, token=None, extraInfo=None, startTag=True):
        
        if extraInfo is None:
            extraInfo = ''

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
            self.outputFile.write('<{tag}> {token} {extraInfo} </{tag}>\n'.format(
                tag=tag,
                token=token,
                extraInfo=extraInfo)
                )
    @property 
    def newLabel(self):
        self.labelIndex += 1
        return "L{}".format(self.labelIndex)
    
    @property
    def currentLabel(self):
        return "L{}".format(self.labelIndex)

    def compileClass(self):
        if not self.tokenizer.keyWord == 'class':
            return

        self.write(tag='class', startTag=True)
        
        self.write(tag='keyword',token=self.tokenizer.keyWord)
        self.tokenizer.advance()

        self.write(tag='identifier',token=self.tokenizer.identifier)
        self.className = self.tokenizer.identifier
        self.tokenizer.advance()

        self.write(tag='symbol', token=self.tokenizer.symbol)
        self.tokenizer.advance()

        while (self.tokenizer.keyWord in ['static', 'field']):
            self.compileClassVarDec()

        while (self.tokenizer.keyWord in ['constructor', 'function', 'method', 'void']):
            self.subroutineTable.startSubroutine()  # reset symbol table
            if self.tokenizer.keyWord == 'method':
                # First argument in a subroutine table must be reference to the object containing the method
                self.subroutineTable.define('this', self.className, 'argument')
                
            self.compileSubroutine()
        self.write(tag='symbol', token=self.tokenizer.symbol)
        self.tokenizer.advance()

        self.write('class', startTag=False)
        self.tokenizer.advance()

    def compileClassVarDec(self):
        # Opening tag
        self.write(tag='classVarDec')

        self.write('keyword', self.tokenizer.keyWord)
        kind = self.tokenizer.keyWord
        self.tokenizer.advance()

        if self.tokenizer.tokenType == KEYWORD:
            self.write('keyword', self.tokenizer.keyWord)
        else:
            self.write('identifier', self.tokenizer.identifier)
        types = self.tokenizer.currentToken
        self.tokenizer.advance()

        self.write('identifier', self.tokenizer.identifier)
        
        # Define class table entry
        name = self.tokenizer.identifier
        self.classTable.define(name, types, kind)
        
        self.write('identifier', self.tokenizer.identifier, extraInfo=("{cat} {type} {kind} {index}".format(
            cat="class", 
            type="defined", 
            kind=self.classTable.kindOf(name),
            index=self.classTable.indexOf(name))))
        
        self.tokenizer.advance()

        extraVars = True
        while extraVars:
            if self.tokenizer.currentToken == ',':

                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()

                self.write('identifier', self.tokenizer.identifier)

                # Define class table entry
                name = self.tokenizer.identifier
                self.classTable.define(name, types, kind)
                
                self.write('identifier', self.tokenizer.identifier, extraInfo=("{cat} {type} {kind} {index}".format(
                    cat="class", 
                    type="defined", 
                    kind=self.classTable.kindOf(name),
                    index=self.classTable.indexOf(name))))

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
        isMethod = self.tokenizer.keyWord == 'method'
        isConstructor = self.tokenizer.keyWord == 'constructor'

        self.tokenizer.advance()

        if self.tokenizer.tokenType == KEYWORD:
            self.write('keyword', self.tokenizer.keyWord)
        else:
            self.write('identifier', self.tokenizer.identifier)

        self.tokenizer.advance()

        # Function name
        self.write('identifier', self.tokenizer.identifier)
        functionName = self.tokenizer.identifier
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
        nLocals = self.compileVarDec()
        functionName = "{}.{}".format(self.className, functionName)
        # write function entry
        if not isConstructor:
            self.vmWriter.writeFunction(functionName, nLocals)
        else:
            nLocals = self.classTable.symbolTable['kind'].count('field')
            self.vmWriter.writeFunction(functionName, nLocals)

        # write statements
        if isMethod:
            self.vmWriter.writePush("argument 0")
            self.vmWriter.writePop("pointer 0")
        elif isConstructor:
            self.vmWriter.writePush("constant {}".format(nLocals))
            self.vmWriter.writeCall("Memory.alloc 1")
            self.vmWriter.writePop("pointer 0")
        self.compileStatements()

        # close subroutine body
        self.write('symbol', token=self.tokenizer.symbol)
        self.tokenizer.advance()
        self.write(tag='subroutineBody', startTag=False)
        
        # Closing tag
        self.write(tag='subroutineDec', startTag=False)

    def compileVarDec(self):
        
        nLocals = 0  # For counting the number of local vars

        if self.tokenizer.currentToken != 'var':
            return nLocals

        variableDecs = True

        while variableDecs:
            # Write var declarations
            if self.tokenizer.currentToken != 'var':
                variableDecs = False
                break

            # Write starting vardec tag 
            self.write('varDec')

            nLocals += 1

            self.write('keyword', self.tokenizer.keyWord)
            kind = self.tokenizer.keyWord
            self.tokenizer.advance()

            if self.tokenizer.tokenType == KEYWORD:
                self.write('keyword', self.tokenizer.keyWord)
            else:
                self.write('identifier', self.tokenizer.identifier)
            types = self.tokenizer.currentToken
            self.tokenizer.advance()

            self.write('identifier', self.tokenizer.identifier)

            # Define class table entry
            name = self.tokenizer.identifier
            self.subroutineTable.define(name, types, kind)
            
            self.write('identifier', self.tokenizer.identifier, extraInfo=("{cat} {type} {kind} {index}".format(
                cat="subroutine", 
                type="defined", 
                kind=self.subroutineTable.kindOf(name),
                index=self.subroutineTable.indexOf(name))))

            self.tokenizer.advance()

            extraVars = True
            while extraVars:
                if self.tokenizer.currentToken == ',':

                    self.write('symbol', self.tokenizer.symbol)
                    self.tokenizer.advance()

                    nLocals += 1

                    # Define class table entry
                    name = self.tokenizer.identifier
                    self.subroutineTable.define(name, types, kind)
                    
                    self.write('identifier', self.tokenizer.identifier, extraInfo=("{cat} {type} {kind} {index}".format(
                        cat="subroutine", 
                        type="defined", 
                        kind=self.subroutineTable.kindOf(name),
                        index=self.subroutineTable.indexOf(name))))

                    self.write('identifier', self.tokenizer.identifier)
                    self.tokenizer.advance()
                else:
                    extraVars = False

            self.write('symbol', token=self.tokenizer.symbol)
            self.tokenizer.advance()

            # Write ending vardec tag 
            self.write('varDec', startTag=False)
            return nLocals

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
        funName = ''
        methodCall = ''
        doStatement = True

        while doStatement:
            subroutineName = ''
            if self.tokenizer.lookAhead() == '(':
                # subroutine call 1
                self.write('identifier', self.tokenizer.identifier)
                subroutineName += self.tokenizer.identifier
                self.tokenizer.advance()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
                nExpressions = self.compileExpressionList()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
            elif self.tokenizer.lookAhead() == '.':
                obj = self.tokenizer.identifier

                try:
                    # If obj is a type of object in the subroutine table, its a local object or parameter
                    if self.subroutineTable.typeOf(obj):
                        methodCall += self.subroutineTable.typeOf(obj) 
                        objKind = self.subroutineTable.kindOf(obj)
                        n = self.subroutineTable.indexOf('this')
                        self.vmWriter.writePush("{} {}".format(objKind, n))
                except:  # otherwise, its a builtin, so just use the given token
                    methodCall += obj

                self.tokenizer.advance()
                self.write('symbol', self.tokenizer.symbol)
                methodCall += self.tokenizer.symbol
                self.tokenizer.advance()
                self.write('identifier', self.tokenizer.identifier)
                methodCall += self.tokenizer.identifier
                funName = self.tokenizer.identifier
    
                self.tokenizer.advance()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
                nExpressions = self.compileExpressionList()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()

            # Write constructor call
            if len(methodCall) > 0:
                self.vmWriter.writeCall(methodCall, nExpressions + 1)  # +1 because object first pushed onto stack
            else:
                self.vmWriter.writePush("pointer 0")  # method with no class - send this as first arg
                self.vmWriter.writeCall(subroutineName, nExpressions + 1)

            if len(funName) and "void {}".format(funName) in self.tokenizer.codeStream:
                self.vmWriter.writePop("temp 0")

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

        # Let keyword
        self.write('keyword', self.tokenizer.keyWord)
        self.tokenizer.advance()

        # var name
        self.write('identifier', self.tokenizer.identifier)
        
        # Define class table entry
        name = self.tokenizer.identifier

        try:
            kind=VM_TYPES[self.subroutineTable.kindOf(name)]  # convert kind to a VM_TYPE e.g., method vars become local
            index=self.subroutineTable.indexOf(name)
        except:
            kind=VM_TYPES[self.classTable.kindOf(name)]
            index=self.classTable.indexOf(name)

        self.write('identifier', self.tokenizer.identifier, extraInfo=("{cat} {type} {kind} {index}".format(
            cat="subroutine", 
            type="used", 
            kind=kind,
            index=index)))
        self.tokenizer.advance()

        if self.tokenizer.currentToken == '[':
            self.write('symbol', self.tokenizer.symbol)
            self.tokenizer.advance()

            self.compileExpression()

            self.write('symbol', self.tokenizer.symbol)
            self.tokenizer.advance()

        # Equal symbol
        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        self.compileExpression()

        # Semi-colon
        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        # pop value off stack
        self.vmWriter.writePop("{} {}".format(kind, index))

        # write closing tag
        self.write('letStatement', startTag=False)

    def compileWhile(self):
        # Compile opening tag
        self.write('whileStatement')

        L1 = self.newLabel
        L2 = self.newLabel

        # while
        self.write('keyword', self.tokenizer.keyWord)
        
        # while label - L1
        self.vmWriter.writeLabel(L1)
        self.tokenizer.advance()

        # open brackets
        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        self.compileExpression()

        # close brackets
        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        # if-goto L2 label
        self.vmWriter.writeArithmetic("not")
        self.vmWriter.writeIf(L2)

        # open curly brackets
        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        self.compileStatements()

        # goto L1 label
        self.vmWriter.writeGoto(L1)

        # close curly brackets
        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        # L2 label
        self.vmWriter.writeLabel(L2)

        # Compile closing tag
        self.write('whileStatement', startTag=False)

    def compileReturn(self):
        # write starting tag
        self.write('returnStatement')

        self.write('keyword', self.tokenizer.keyWord)
        self.tokenizer.advance()

        if self.tokenizer.keyWord == 'this':  # returning from a constructor
            self.vmWriter.writePush('pointer 0')
            self.tokenizer.advance()
        elif self.tokenizer.currentToken != ';':
            self.compileExpression()
        else:
            self.vmWriter.writePush('constant 0')
        self.vmWriter.writeReturn()

        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        # Write closing tag
        self.write('returnStatement', startTag=False)

    def compileIf(self):
        # Compile opening tag
        self.write('ifStatement')

        L1 = self.newLabel
        L2 = self.newLabel

        # if 
        self.write('keyword', self.tokenizer.keyWord)
        self.tokenizer.advance()

        # open brackets
        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        # expresssion
        self.compileExpression()

        # if-goto L1
        self.vmWriter.writeArithmetic("not")
        self.vmWriter.writeIf(L1)

        # close brackets
        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        # open curly brackets
        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        # write if statement body
        self.compileStatements()

        # write Goto L2
        self.vmWriter.writeGoto(L2)

        # close curly brackets
        self.write('symbol', self.tokenizer.symbol)
        self.tokenizer.advance()

        if self.tokenizer.currentToken == 'else':
            # else
            self.write('keyword', self.tokenizer.keyWord)
            self.tokenizer.advance()

            # open curly brackets
            self.write('symbol', self.tokenizer.symbol)
            self.tokenizer.advance()

            # write L1 label
            self.vmWriter.writeLabel(L1)

            # Write else body
            self.compileStatements()

            # write L2 label
            self.vmWriter.writeLabel(L2)

            # close curly brackets
            self.write('symbol', self.tokenizer.symbol)
            self.tokenizer.advance()
        
        # Compile closing tag
        self.write('ifStatement', startTag=False)

    def compileExpression(self):
        # write opening tag
        self.write('expression')
        self.compileTerm()
        
        opCollection = []  # for dealing with operators

        # write more terms
        op = self.tokenizer.currentToken in OPERATORS
        while op:
            if self.tokenizer.currentToken in CONVERT_SYMBOL:
                self.write('symbol', CONVERT_SYMBOL[self.tokenizer.currentToken])
            else:
                self.write('symbol', self.tokenizer.currentToken)
            opCollection.append(self.tokenizer.currentToken)
            self.tokenizer.advance()
            self.compileTerm()
            op = self.tokenizer.currentToken in OPERATORS
        
        # Write operators in reverse order
        opCollection.reverse()
        for op in opCollection:
            self.vmWriter.writeArithmetic(OP_CONVERSION[op])

        # Compile closing tag
        self.write('expression', startTag=False)


    def compileTerm(self):
        # compile starting tag
        self.write('term')
        opCollection = []  # For dealing with unary operators
        methodCall = ''
        isConstructor = False
        nExpressions = 0

        if self.tokenizer.tokenType == KEYWORD:
            self.write('keyword', self.tokenizer.keyWord)
            self.vmWriter.writePush("{}".format(self.tokenizer.keyWord))
            self.tokenizer.advance()
        elif self.tokenizer.tokenType == INT_CONST:
            self.write('integerConstant', self.tokenizer.intVal)
            self.vmWriter.writePush("constant {}".format(self.tokenizer.intVal))
            self.tokenizer.advance()
        elif self.tokenizer.tokenType == STRING_CONST:
            self.write('stringConstant', self.tokenizer.stringVal)
            self.vmWriter.writePush("constant {}".format(self.tokenizer.stringVal))
            self.tokenizer.advance()
        elif self.tokenizer.currentToken in UN_OP:
            self.write('symbol', self.tokenizer.symbol)
            opCollection.append(self.tokenizer.currentToken)  # append unary op
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
                # subroutine call 1 - probably redundant because functions like this called using do
                self.write('identifier', self.tokenizer.identifier)
                self.tokenizer.advance()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
                self.compileExpressionList()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
            elif self.tokenizer.lookAhead() == '.':
                # subroutine call 2 - method call
                self.write('identifier', self.tokenizer.identifier)
                obj = self.tokenizer.identifier

                # If obj is the className, its a constructor call
                if obj == self.className:  
                    methodCall += self.subroutineTable.typeOf('this')
                    isConstructor = (obj == self.className)
                else:
                    try:
                        # If obj is a type of object in the subroutine table, its a local object or parameter
                        if self.subroutineTable.typeOf(obj):
                            methodCall += self.subroutineTable.typeOf(obj) 
                            objKind = self.subroutineTable.kindOf(obj)
                            n = self.subroutineTable.indexOf('this')
                            self.vmWriter.writePush("{} {}".format(objKind, n))
                    except:  # otherwise, its a builtin, so just use the given token
                        methodCall += obj

                self.tokenizer.advance()
                self.write('symbol', self.tokenizer.symbol)
                methodCall += self.tokenizer.symbol
                self.tokenizer.advance()
                self.write('identifier', self.tokenizer.identifier)
                methodCall += self.tokenizer.identifier
    
                self.tokenizer.advance()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
                nExpressions = self.compileExpressionList()
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
            else:
                # Get table entry
                name = self.tokenizer.identifier

                try:
                    kind=self.subroutineTable.kindOf(name)
                    index=self.subroutineTable.indexOf(name)
                except:
                    kind=self.classTable.kindOf(name)
                    index=self.classTable.indexOf(name)

                self.write('identifier', self.tokenizer.identifier, extraInfo=("{cat} {type} {kind} {index}".format(
                    cat="subroutine", 
                    type="used", 
                    kind=kind,
                    index=index)))
                
                self.vmWriter.writePush("{kind} {index}".format(kind=kind, index=index))
                self.tokenizer.advance()

        # Write constructor call
        if len(methodCall) > 0:
            self.vmWriter.writeCall(methodCall, nExpressions + 1 - isConstructor)  # +1 because object first pushed onto stack

        # Write unary ops
        opCollection.reverse()
        for op in opCollection:
            self.vmWriter.writeArithmetic(OP_CONVERSION[op])

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
            
            kind = 'argument'

            self.write('keyword', self.tokenizer.keyWord)
            types = self.tokenizer.keyWord
            self.tokenizer.advance()

            self.write('identifier', self.tokenizer.identifier)
            name = self.tokenizer.identifier
            
            # Define subroutine table entry
            self.subroutineTable.define(name, types, kind)

            self.write('identifier', self.tokenizer.identifier, extraInfo=("{cat} {type} {kind} {index}".format(
                cat="subroutine", 
                type="defined", 
                kind=self.subroutineTable.kindOf(name),
                index=self.subroutineTable.indexOf(name))))
            
            self.tokenizer.advance()            

            if self.tokenizer.currentToken == ',':
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()

        self.write('parameterList', startTag=False)

    def compileExpressionList(self):
        # Write starting tag
        self.write('expressionList')
        nExpressions = 0  # number of expressions

        expList = True
        while expList:
            if self.tokenizer.currentToken == ')':
                expList = False
                break
            
            self.compileExpression()
            nExpressions += 1

            if self.tokenizer.currentToken == ',':
                self.write('symbol', self.tokenizer.symbol)
                self.tokenizer.advance()
        
        self.write('expressionList', startTag=False)
        return nExpressions


if __name__ == "__main__":
    arg = sys.argv[1]
    eng = CompilationEngine(arg)
    eng.closeFile()
