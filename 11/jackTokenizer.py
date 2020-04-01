import sys
import copy

SYMBOLS = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~'] 
KEYWORDS = ['class', 'constructor', 'function', 'method', 'field', 
    'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 
    'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
OPERATORS = ['+', '-', '*', '/', '&', '|', '<', '>', '=', '~'] 
UN_OP = ['~', '-']

CONVERT_SYMBOL = {}
CONVERT_SYMBOL['<'] = '&lt;'
CONVERT_SYMBOL['>'] = '&gt;'
CONVERT_SYMBOL['&'] = '&amp;'

KEYWORD = 0
SYMBOL = 1
IDENTIFIER = 2
INT_CONST = 3
STRING_CONST = 4


class JackTokenizer (object):
    def __init__(self, fileName):
        self.currentToken = None
        self.codeStream = self.openFile(fileName)
        self.index = 0

    def openFile(self, fileName):
        """
        Open Jack file and return stream of chars as str
        """
        with open(fileName, 'r') as f:
            code = f.readlines()

        # Remove inline comments of //
        # Difficult to deal with as they have no end point
        code = [line.split("//")[0] for line in code]
        code = ''.join(code)

        # Remove all white space, tabs, and newlines
        return code

    @property
    def hasMoreTokens(self):
        return self.index < (len(self.codeStream)-1) 

    def lookAhead(self):
        """
        Look ahead n spaces
        """
        nextToken = self.codeStream[self.index]
        currentIndex = copy.copy(self.index)
        
        while nextToken in [' ', '', '/t', '/n']:
            currentIndex += 1
            nextToken = self.codeStream[currentIndex]
        return nextToken


    def advance(self):
        # Only inline and API comments need to be handled
        # These can be handled by checking for the closing comment symbols
        temp = ''
        runCode = True
        inString = False

        while runCode and self.hasMoreTokens:
            if self.codeStream[self.index] in [' ', '\t', '\n'] and len(temp) == 0:
                self.index += 1
                continue
            # Check for comments
            elif self.codeStream[self.index:self.index+2] == '/*':
                self.index += 2
                inComment = True
                while (inComment):
                    if inComment and self.codeStream[self.index-2:self.index] == '*/':
                        inComment = False
                    self.index += 1  # increment past final comment symbol
            else:
                # Check for symbol only
                char = self.codeStream[self.index]

                if char == '"' and inString:
                    inString = False
                elif char == '"' and not inString:
                    inString = True

                if inString:
                    temp += char
                    self.index += 1
                    continue
                elif char in SYMBOLS and len(temp) == 0:
                    temp = char
                    self.index += 1
                    runCode = False
                    break
                # Check for trailing symbol or space, after keywords, identifiers etc
                elif char in SYMBOLS or char in [' ', '\t', '\n'] and len(temp) > 0 and not inString:
                    runCode = False
                    break
                temp = temp + char
                self.index += 1
        
        self.currentToken = temp

    @property
    def tokenType(self):
        if self.currentToken in SYMBOLS:
            return SYMBOL
        elif self.currentToken in KEYWORDS:
            return KEYWORD
        elif self.currentToken.startswith('"'):
            return STRING_CONST
        elif self.currentToken.isdigit():
            return INT_CONST
        else:
            return IDENTIFIER

    @property
    def keyWord(self):
        if self.tokenType == KEYWORD:
            return self.currentToken

    @property
    def symbol(self):
        if self.tokenType == SYMBOL:
            if self.currentToken in CONVERT_SYMBOL:
                return CONVERT_SYMBOL[self.currentToken]
            return self.currentToken
    
    @property
    def identifier(self):
        if self.tokenType == IDENTIFIER:
            return self.currentToken

    @property
    def intVal(self):
        if self.tokenType == INT_CONST:
            return self.currentToken

    @property
    def stringVal(self):
        if self.tokenType == STRING_CONST:
            return self.currentToken.replace(';', '\;').replace('"', '')

if __name__ == "__main__":
    arg = sys.argv[1]
    tokenizer = JackTokenizer(arg)
    while(tokenizer.hasMoreTokens):
        tokenizer.advance()