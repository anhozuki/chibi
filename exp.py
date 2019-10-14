class Val(object):
   __slots__=['value']
   def __init__(self, v = 0):
       self.value = v
   def __repr__(self):
       return f'Val({self.value})'
   def eval(self):
       return self.value
v = Val(1)
print(v)
assert v.eval() == 1
class Add(object):
   __slots__ = ['left', 'right']
   def __init__(self, a, b):
       self.left = a
       self.right = b
   def eval(self):
       return self.left.eval() + self.right.eval()
e = Add(Val(1), Val(2))
print(e.eval())
assert e.eval() == 3
e = Add(Val(1), Add(Val(2), Val(3)))
print(e.eval())
assert e.eval() == 6
class Mul(object):
   __slots__ = ['left', 'right']
   def __init__(self, a, b):
       self.left = a
       self.right = b
   def eval(self):
       return self.left.eval() * self.right.eval()
e = Mul(Val(1), Val(2))
print(e.eval())
assert e.eval() == 2
class Sub(object):
   __slots__ = ['left', 'right']
   def __init__(self, a, b):
       self.left = a
       self.right = b
   def eval(self):
       return self.left.eval() - self.right.eval()
e = Sub(Val(1), Val(2))
print(e.eval())
assert e.eval() == -1
class Div(object):
   __slots__ = ['left', 'right']
   def __init__(self, a, b):
       self.left = a
       self.right = b
   def eval(self):
       return self.left.eval() / self.right.eval()
e = Div(Val(7), Val(2))
print(e.eval())
assert e.eval() == 3.5
class Expr(object):
   pass
class Val(Expr):
   __slots__=['value']
   def __init__(self, v = 0):
       self.value = v
   def __repr__(self):
       return f'Val({self.value})'
   def eval(self):
       return self.value
v = Val(1)
print(v)
assert v.eval() == 1
class Add(Expr):
   __slots__ = ['left', 'right']
   def __init__(self, a, b):
       self.left = a
       self.right = b
   def eval(self):
       return self.left.eval() + self.right.eval()
e = Add(Val(1),Val(2))
print(e.eval())
assert e.eval() == 3
assert isinstance(v, Expr)
assert isinstance(v, Val)
assert  not isinstance(v, int)
def toExpr(a):
   if not isinstance(a, Expr):
       a = Val(a)
   return a
class Add(Expr):
   __slots__ = ['left', 'right']
   def __init__(self, a, b):
       self.left = toExpr(a)
       self.right = toExpr(b)
   def eval(self):
       return self.left.eval() + self.right.eval()
e = Add(1,Add(1, 2))
print(e.eval())
assert e.eval() == 4
print()
print()


