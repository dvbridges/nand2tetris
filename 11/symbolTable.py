from collections import defaultdict
STATIC = 'static'
FIELD = 'field'


class SymbolTable(object):
    def __init__(self):
        self.symbolTable = {}
        self.defaultKeys = ['name', 'type', 'kind', 'index']
        self.startSubroutine()

    def startSubroutine(self, table=None):
        self.symbolTable = {}
        for key in self.defaultKeys:
            self.symbolTable.setdefault(key, [])

    def define(self, name, types, kind):

        if name in self.symbolTable['name']:
            return

        varCount = self.varCount(kind)
        self.symbolTable['name'].append(name)
        self.symbolTable['type'].append(types)
        self.symbolTable['kind'].append(kind)
        self.symbolTable['index'].append(varCount)

    def varCount(self, kind):
        return self.symbolTable['kind'].count(kind)

    def kindOf(self, name):
        idx = self.symbolTable['name'].index(name)
        return self.symbolTable['kind'][idx]

    def typeOf(self, name):
        idx = self.symbolTable['name'].index(name)
        return self.symbolTable['type'][idx]

    def indexOf(self, name):
        idx = self.symbolTable['name'].index(name)
        return self.symbolTable['index'][idx]


if __name__ == "__main__":
    b = SymbolTable()
    for i in range(3):
        b.define('x', 'static', STATIC)
    
    b.define('y', 'int', FIELD)
    b.define('z', 'char', FIELD)
    print(b.kindOf('x'))
    print(b.typeOf('y'))
    print(b.indexOf('z'))
    print(b.symbolTable)



    