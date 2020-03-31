import sys
import os
import re
from pathlib import Path

from jackTokenizer import *

OP_CONVERSION = {}
OP_CONVERSION['+'] = 'add'
OP_CONVERSION['-'] = 'sub'
OP_CONVERSION['~'] = 'not'  # TODO: check if this causes error i.e, using neg instead of not
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

        self.tokenizer = tokenizer(fileName)
        self.classTable = SymbolTable()
        self.subroutineTable = SymbolTable()
        self.vmWriter = vmWriter(fileName)
        self.className = None
        self.functions = []  # lists functions in class - i.e., not methods or constructors

        self.indent = 0
        self.labelIndex = -1
        self.tokenizer.advance()
    
    def start(self):
        self.compileClass()

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

        # class keyword
        self.tokenizer.advance()

        # class name identifier
        self.className = self.tokenizer.identifier
        self.tokenizer.advance()

        # open class body
        self.tokenizer.advance()

        while (self.tokenizer.keyWord in ['static', 'field']):
            self.compileClassVarDec()

        while (self.tokenizer.keyWord in ['constructor', 'function', 'method', 'void']):
            self.subroutineTable.startSubroutine()  # reset symbol table
            if self.tokenizer.keyWord in ['method']:
                # First argument in a subroutine table must be reference to the object containing the method
                self.subroutineTable.define('this', self.className, 'argument')
            self.compileSubroutine()
        
        # Close class body
        self.tokenizer.advance()
        # Class line
        self.tokenizer.advance()

    def compileClassVarDec(self):
        # Static or field var
        kind = self.tokenizer.keyWord
        self.tokenizer.advance()

        # Get variable type
        types = self.tokenizer.currentToken
        self.tokenizer.advance()

        # Get variable name
        name = self.tokenizer.identifier

        # Define class var symbol table entry
        self.classTable.define(name, types, kind)
        self.tokenizer.advance()

        extraVars = True
        while extraVars:
            if self.tokenizer.currentToken == ',':
                
                # comma separator
                self.tokenizer.advance()

                # get variable name
                # Define class table entry
                name = self.tokenizer.identifier
                self.classTable.define(name, types, kind)
                self.tokenizer.advance()
            else:
                extraVars = False

        # Semi colon1
        self.tokenizer.advance()

    def compileSubroutine(self):

        # function type, method, constructor etc
        isMethod = self.tokenizer.keyWord == 'method'
        isConstructor = self.tokenizer.keyWord == 'constructor'
        isFunction = self.tokenizer.keyWord == 'function'
        self.tokenizer.advance()

        # Function name or type - can be void, or a class type
        self.tokenizer.advance()

        # Function name identifier
        functionName = self.tokenizer.identifier
        if isFunction:
            self.functions.append(functionName)

        self.tokenizer.advance()

        # Open param brackets
        self.tokenizer.advance()

        # write parameterList
        self.compileParameterList() 
        # Close param brackets
        self.tokenizer.advance()

        # Write subroutine body, open curly brackets
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
            self.vmWriter.writePush("argument", "0")
            self.vmWriter.writePop("pointer", "0")
        elif isConstructor:
            self.vmWriter.writePush("constant", nLocals)
            self.vmWriter.writeCall("Memory.alloc", "1")
            self.vmWriter.writePop("pointer", "0")
        self.compileStatements()

        # close subroutine body
        self.tokenizer.advance()

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

            nLocals += 1
            # var declaration
            kind = self.tokenizer.keyWord
            self.tokenizer.advance()

            # Variable type
            types = self.tokenizer.currentToken
            self.tokenizer.advance()

            # variable name / identifier
            name = self.tokenizer.identifier
            
            # Define class table entry
            self.subroutineTable.define(name, types, kind)
            self.tokenizer.advance()

            extraVars = True
            while extraVars:
                if self.tokenizer.currentToken == ',':
                    
                    # comma separator
                    self.tokenizer.advance()

                    nLocals += 1

                    # variable name / identifier
                    name = self.tokenizer.identifier

                    # Define class table entry
                    self.subroutineTable.define(name, types, kind)
                    self.tokenizer.advance()
                else:
                    extraVars = False

            # Semi colon
            self.tokenizer.advance()
        return nLocals

    def compileStatements(self):
        writeStatements = self.tokenizer.currentToken in ['if', 'else', 'let', 'do', 'while', 'return']
        if not writeStatements:
            return

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

    def compileDo(self):

        # do keyword
        self.tokenizer.advance()

        funName = ''
        methodCall = ''
        useBuiltin = False
        doStatement = True

        while doStatement:
            subroutineName = ''
            if self.tokenizer.lookAhead() == '(':
                # subroutine call 1
                # function name
                subroutineName += self.tokenizer.identifier
                funName = self.tokenizer.identifier
                self.tokenizer.advance()
                # open brackets
                self.tokenizer.advance()
                nExpressions = self.compileExpressionList()
                # close brackets
                self.tokenizer.advance()
            elif self.tokenizer.lookAhead() == '.':

                # method class name
                obj = self.tokenizer.identifier

                try:
                    # If obj is a type of object in the subroutine table, its a local object or parameter
                    if self.subroutineTable.typeOf(obj):
                        methodCall += self.subroutineTable.typeOf(obj) 
                        objKind=VM_TYPES[self.subroutineTable.kindOf(obj)]  # convert kind to a VM_TYPE e.g., method vars become local
                        n = self.subroutineTable.indexOf('this')
                        self.vmWriter.writePush(objKind, n)
                except:  # otherwise, its a builtin, so just use the given token
                    methodCall += obj
                    useBuiltin = True

                self.tokenizer.advance()

                # dot separator
                methodCall += self.tokenizer.symbol
                self.tokenizer.advance()
                # function name
                methodCall += self.tokenizer.identifier
                funName = self.tokenizer.identifier
                self.tokenizer.advance()
                # Open brackets
                self.tokenizer.advance()
                nExpressions = self.compileExpressionList()
                # close brackets
                self.tokenizer.advance()

            # Write constructor call
            # Check variable is a method
            regex = re.compile( r'method (\w+) {}'.format(funName) )
            match = re.search(regex, self.tokenizer.codeStream)
            if match:
                nExpressions += 1

            if len(methodCall) > 0:
                self.vmWriter.writeCall(methodCall, nExpressions) 
            else:
                self.vmWriter.writeCall(subroutineName, nExpressions)

            # Check if method call is a void method
            if len(funName) and "void {}".format(funName) in self.tokenizer.codeStream or useBuiltin:
                self.vmWriter.writePop("temp", "0")

            if self.tokenizer.currentToken == ';':
                doStatement = False
                break
                
        # Semi colon
        self.tokenizer.advance()

    def compileLet(self):

        isArray = False

        # Let keyword
        self.tokenizer.advance()

        # var name
        name = self.tokenizer.identifier

        if self.tokenizer.lookAhead() == '[':
            isArray = True

        # Get the kind and index, as a local or class variable
        try:
            kind=VM_TYPES[self.subroutineTable.kindOf(name)]  # convert kind to a VM_TYPE e.g., method vars become local
            index=self.subroutineTable.indexOf(name)
        except:
            kind=VM_TYPES[self.classTable.kindOf(name)]
            index=self.classTable.indexOf(name)

        self.tokenizer.advance()

        # We have an array
        if isArray:
            # Push array address
            self.vmWriter.writePush(kind, index)

            # open square brackets
            self.tokenizer.advance()

            # Compile expression
            self.compileExpression()

            # add expression to array address
            self.vmWriter.writeArithmetic('add')

            # close square brackets
            self.tokenizer.advance()

        # Equal symbol
        self.tokenizer.advance()

        # Compile expression
        self.compileExpression()

        if isArray:
            # send expression to temp
            self.vmWriter.writePop("temp", "0")
            # send first array address to that
            self.vmWriter.writePop("pointer", "0")
            # Push temp value of expression 2 to stack
            self.vmWriter.writePush("temp", "0")
            # Send temp value to array address
            self.vmWriter.writePop("that", "0")

        # Semi-colon
        self.tokenizer.advance()

        # pop value off stack
        if not isArray:
            self.vmWriter.writePop(kind, index)

    def compileWhile(self):

        L1 = self.newLabel
        L2 = self.newLabel

        # while label - L1
        self.vmWriter.writeLabel(L1)

        # while statement
        self.tokenizer.advance()

        # open brackets
        self.tokenizer.advance()

        self.compileExpression()

        # close brackets
        self.tokenizer.advance()

        # if-goto L2 label
        self.vmWriter.writeArithmetic("not")
        self.vmWriter.writeIf(L2)

        # open curly brackets
        self.tokenizer.advance()

        self.compileStatements()

        # goto L1 label
        self.vmWriter.writeGoto(L1)

        # close curly brackets
        self.tokenizer.advance()

        # L2 label
        self.vmWriter.writeLabel(L2)
    
    def compileReturn(self):
        
        # return
        self.tokenizer.advance()

        if self.tokenizer.keyWord == 'this':  # returning from a constructor
            self.vmWriter.writePush('pointer', '0')
            self.tokenizer.advance()
        elif self.tokenizer.currentToken != ';':
            self.compileExpression()
        else:
            self.vmWriter.writePush('constant', '0')
        self.vmWriter.writeReturn()

        # semi colon
        self.tokenizer.advance()

    def compileIf(self):

        L1 = self.newLabel
        L2 = self.newLabel

        # if 
        self.tokenizer.advance()

        # open brackets
        self.tokenizer.advance()

        # expresssion
        self.compileExpression()

        # if-goto L1
        self.vmWriter.writeArithmetic("not")
        self.vmWriter.writeIf(L1)

        # close brackets
        self.tokenizer.advance()

        # open curly brackets
        self.tokenizer.advance()

        # write if statement body
        self.compileStatements()

        # write Goto L2
        # self.vmWriter.writeGoto(L2)

        # close curly brackets
        self.tokenizer.advance()

        if self.tokenizer.currentToken == 'else':
            # write Goto L2
            self.vmWriter.writeGoto(L2)

            # else
            self.tokenizer.advance()

            # open curly brackets
            self.tokenizer.advance()

            # write L1 label
            self.vmWriter.writeLabel(L1)

            # Write else body
            self.compileStatements()

            # write L2 label
            self.vmWriter.writeLabel(L2)

            # close curly brackets
            self.tokenizer.advance()
        else:
            # write L1 label
            self.vmWriter.writeLabel(L1)

        
    def compileExpression(self):
        self.compileTerm()
        
        opCollection = []  # for dealing with operators

        # write more terms
        op = self.tokenizer.currentToken in OPERATORS
        while op:
            opCollection.append(self.tokenizer.currentToken)
            # operator
            self.tokenizer.advance()
            self.compileTerm()
            op = self.tokenizer.currentToken in OPERATORS
        
        # Write operators in reverse order
        opCollection.reverse()
        for op in opCollection:
            self.vmWriter.writeArithmetic(OP_CONVERSION[op])

    def compileTerm(self):
        opCollection = []  # For dealing with unary operators
        methodCall = ''
        isConstructor = False
        isMethod = False
        nExpressions = 0
        
        if self.tokenizer.tokenType == KEYWORD:

            if self.tokenizer.keyWord == 'true':
                self.vmWriter.writePush("constant", "1")
                self.vmWriter.writeArithmetic("neg")

            elif self.tokenizer.keyWord == 'false':
                self.vmWriter.writePush("constant", "0")
            else:
                self.vmWriter.writePush("{}".format(self.tokenizer.keyWord))
            self.tokenizer.advance()
        elif self.tokenizer.tokenType == INT_CONST:
            self.vmWriter.writePush("constant", "{}".format(self.tokenizer.intVal))
            self.tokenizer.advance()
        elif self.tokenizer.tokenType == STRING_CONST:
            self.vmWriter.writePush("constant", self.tokenizer.stringVal)
            self.tokenizer.advance()
        elif self.tokenizer.currentToken in UN_OP:
            opCollection.append(self.tokenizer.currentToken)  # append unary op
            self.tokenizer.advance()
            self.compileTerm()
        else:
            if self.tokenizer.currentToken == '(':
                # Simple expression : ( expression )
                # open brackets
                self.tokenizer.advance()
                self.compileExpression()
                # close brackets
                self.tokenizer.advance()
            elif self.tokenizer.lookAhead() == '[':
                # Varname [ expression ]
                # array name
                self.tokenizer.advance()
                # open square brackets
                self.tokenizer.advance()
                self.compileExpression()
                # close square brackets
                self.tokenizer.advance()
            elif self.tokenizer.lookAhead() == '(':
                # subroutine call 1 - probably redundant because functions like this called using do
                # method object/class name
                funName = self.tokenizer.identifier
                methodCall += funName
                self.tokenizer.advance()
                # open brackets
                self.tokenizer.advance()
                self.compileExpressionList()
                # close brackets
                self.tokenizer.advance()
            elif self.tokenizer.lookAhead() == '.':
                # subroutine call 2 - method call
                obj = self.tokenizer.identifier
                try:
                    # If obj is a type of object in the subroutine table, its a local object or parameter
                    if self.subroutineTable.typeOf(obj):
                        methodCall += self.subroutineTable.typeOf(obj) 
                        objKind=VM_TYPES[self.subroutineTable.kindOf(obj)]  # convert kind to a VM_TYPE e.g., method vars become local
                        n = self.subroutineTable.indexOf('this')
                        self.vmWriter.writePush(objKind, n)
                except:  # otherwise, its a builtin or is the class, so just use the given token
                    methodCall += obj

                self.tokenizer.advance()
                # dot separator
                methodCall += self.tokenizer.symbol
                self.tokenizer.advance()
                # function name
                methodCall += self.tokenizer.identifier
                funName = self.tokenizer.identifier
    
                self.tokenizer.advance()
                # open brackets
                self.tokenizer.advance()
                nExpressions = self.compileExpressionList()
                # close brackets
                self.tokenizer.advance()
            else:
                # Get table entry
                # variable name
                name = self.tokenizer.identifier

                try:
                    kind=self.subroutineTable.kindOf(name)
                    index=self.subroutineTable.indexOf(name)
                except:
                    kind=self.classTable.kindOf(name)
                    index=self.classTable.indexOf(name)

                self.vmWriter.writePush(VM_TYPES[kind], index)
                self.tokenizer.advance()

        # Write method call
        if len(methodCall) > 0:
            
            # Check variable is not a function type
            regex = re.compile( r'method (\w+) {}'.format(funName) )
            match = re.search(regex, self.tokenizer.codeStream)

            # Check if call is to a constructor - this not pushed on constructors
            if match:
                isMethod = True

            self.vmWriter.writeCall(methodCall, nExpressions + isMethod) 

        # Write unary ops
        opCollection.reverse()
        for op in opCollection:
            self.vmWriter.writeArithmetic(OP_CONVERSION[op])

    def compileParameterList(self):
        paramList = True
        while paramList:
            
            if self.tokenizer.currentToken == ')':
                paramList = False
                break
            
            kind = 'argument'

            # arg type
            types = self.tokenizer.keyWord
            self.tokenizer.advance()

            # arg identifier name
            name = self.tokenizer.identifier
            
            # Define subroutine table entry
            self.subroutineTable.define(name, types, kind)
            self.tokenizer.advance()            

            if self.tokenizer.currentToken == ',':
                # comma separator
                self.tokenizer.advance()

    def compileExpressionList(self):
        nExpressions = 0  # number of expressions

        expList = True
        while expList:
            if self.tokenizer.currentToken == ')':
                expList = False
                break
            
            self.compileExpression()
            nExpressions += 1

            if self.tokenizer.currentToken == ',':
                # comma separator
                self.tokenizer.advance()
        
        return nExpressions


if __name__ == "__main__":
    arg = sys.argv[1]
    eng = CompilationEngine(arg)
    eng.closeFile()
 
 
 