import pegpy
#from pegpy.tpeg import ParseTree
peg = pegpy.grammar('chibi.tpeg')
parser = pegpy.generate(peg)
'''
tree = parser('1+2*3')
print(repr(tree))
tree = parser('1@2*3')
print(repr(tree))
'''

class Expr(object):
    @classmethod
    def new(cls, v):
        if isinstance(v, Expr):
            return v
        return Val(v)
class Val(Expr):
    __slots__ = ['value']
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f'Val({self.value})'
    def eval(self, env: dict):
        return self.value
e = Val(0)
assert e.eval({}) == 0
class Binary(Expr):
    __slots__ = ['left', 'right']
    def __init__(self, left, right):
        self.left = Expr.new(left)
        self.right = Expr.new(right)
    def __repr__(self):
        classname = self.__class__.__name__
        return f'{classname}({self.left},{self.right})'
class Add(Binary):
    __slots__ = ['left', 'right']
    def eval(self, env: dict):
        return self.left.eval(env) + self.right.eval(env)
class Sub(Binary):
    __slots__ = ['left', 'right']
    def eval(self, env: dict):
        return self.left.eval(env) - self.right.eval(env)
class Mul(Binary):
    __slots__ = ['left', 'right']
    def eval(self, env: dict):
        return self.left.eval(env) * self.right.eval(env)
class Div(Binary):
    __slots__ = ['left', 'right']
    def eval(self, env: dict):
        return self.left.eval(env) // self.right.eval(env)
class Mod(Binary):
    __slots__ = ['left', 'right']
    def eval(self, env: dict):
        return self.left.eval(env) % self.right.eval(env)

class Var(Expr):
    __slots__ = ['name']
    def __init__(self, name):
        self.name = name
    def eval(self,env: dict):
        if self.name in env:
            return env[self.name]
        raise NameError(self.name)

class Assign(Expr):
    __slots__ = []
    def __init__(self,name,e):
        self.name = name
        self.e = Expr.new(e)

    def eval(self, env):
        env[self.name] = self.e.eval(env)
        return env[self.name]

print('少しテスト')

env = {}
e = Assign('x', Val(1)) # x =1
print(e.eval(env)) #1
e = Assign('x', Add(Var('x'), Val(2))) #x=x+2
print(e.eval(env)) #e

print('テスト終わり')


def conv(tree):
    if tree == 'Block':
        return conv(tree[0])
    if tree == 'Val' or tree == 'Int':
        return Val(int(str(tree)))
    if tree == 'Add':
        return Add(conv(tree[0]), conv(tree[1]))
    if tree == 'Div':
        return Div(conv(tree[0]), conv(tree[1]))
    if tree == 'Mod':
        return Mod(conv(tree[0], conv(tree[1])))
    if tree == 'Var':
        return Var(str(tree))
    if tree == 'LetDecl':
        return Assign(conv(tree[0]), conv(tree[1]))
    print('@TODO', tree.tag,repr(tree))
    return Val(str(tree))
    
def run(src: str):
    tree = parser(src)
    if tree.isError():
        print(repr(tree))
    else:
        e = conv(tree)
        print('env', env)
        print(e.eval(env))

def main():
    try:
        env = {}
        while True:
            s = input('>>> ')
            if s == '':
                break
            run(s, env)
    except EOFError:
        return
if __name__ == '__main__':
    main()
'''
Chibi Konoha
by Kimio Kuramitsu

example Program 
fib(n) = if n < 3 then 1 else fib(n-1)+fib(n-2)
print(fib(10))
'''
Program = {
Statement*
  #Block
}

EOF
EOF = !.
Statement = FuncDecl / LetDecl / Expression
_ = [ \t\r\n]*
FuncDecl = {
  Name '(' _ Name ')' _ '=' _ Expression
  #FuncDecl
} _
LetDecl = {
  Name '=' _ Expression
  #LetDecl
} _
example Expression if a == 1 then print(a) else 0
example Expression f(a+1)
example Expression 1+2*3
example Expression 1*2+3
example Expression 1-2-3
example Expression 1+2-3
Expression = IfExpr / Cmpr
IfExpr = {
  'if' _ Expression 
  'then' _ Expression 
  'else' _ Expression
  #If
}
Cmpr = { Sum '==' _ Sum #Eq}
  / { Sum '!=' _ Sum #Ne}
  / { Sum '<' _ Sum #Lt}
  / { Sum '>' _ Sum #Gt}
  / { Sum '<=' _ Sum #Lte}
  / { Sum '>=' _ Sum #Gte}
  / Sum
/*
Sum = { Prod ('+' _ Prod)+ #Add}
  / { Prod ('-' _ Prod)+ #Sub}
  / Prod
*/
/*
Prod = { Term ('*' _ Term)+ #Mul}
  / { Term ('/' _ Term)+ #Div}
  / Term
*/
Sum = Prod ( ^{ '+' Prod #Add } / ^ { '-' _ Prod #Sub} )*
Prod = Term ( ^{ '*' Term #Mul } / ^{ '/' _ Term #Div} )*
Term = FuncApp / Name / Value / '(' _ Expression ')' _
FuncApp = {
  Name '(' _ Expression ')' _
  #FuncApp
}
example Name x
example Name x2
Name = {
  [A-Za-z] [A-Za-z0-9]* 
  #Var
} _
example Value 0
example Value 10
Value = {
  [0-9]+ 
  #Int
} _
