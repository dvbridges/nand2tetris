C_ARITHMETIC = 0
C_PUSH = 1
C_POP = 2
C_LABEL = 3
C_GOTO = 4
C_IF = 5
C_FUNCTION = 6
C_RETURN = 7
C_CALL = 8

commandLib = {}
# Artithmetic
commandLib['add'] = C_ARITHMETIC
commandLib['sub'] = C_ARITHMETIC
commandLib['neg'] = C_ARITHMETIC
commandLib['eq'] = C_ARITHMETIC
commandLib['gt'] = C_ARITHMETIC
commandLib['lt'] = C_ARITHMETIC
commandLib['and'] = C_ARITHMETIC
commandLib['or'] = C_ARITHMETIC
commandLib['not'] = C_ARITHMETIC
# Stack commands
commandLib['push'] = C_PUSH
commandLib['pop'] = C_POP

# stack commands
stackOp = {}
stackOp['local'] = 'LCL'
stackOp['argument'] = 'ARG'
stackOp['this'] = 'THIS'
stackOp['that'] = 'THAT'
stackOp['temp'] = 'TEMP'