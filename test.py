from collections import Counter, namedtuple, defaultdict, OrderedDict
from functools import reduce  # forward compatibility for Python 3
import operator

class BaseTree :
    def __init__(self):
        self._data = {}
        self._subtotal = 0
        self._count=None
        self._path=None
        
    def leaf(self):
        return len(self._data.keys())==0
    
    def path(self, path):
        self._path=path
        
    def contains(self, k):
        return k in self._data
        
    def subtotal(self,v):
        self._subtotal=self._subtotal+v

    def __setitem__(self, k, v):
        self._data[k] =v 

    def __getitem__(self, k):
        return self._data[k]

    def count(self, v):
        if self._count is None:
            self._count=0
        
        self._count=self._count+v
        
    def debug_print(self, indent=''):
        print indent + str({
            'path': self._path,
            'count': self._count,
            'subtotal' : self._subtotal })

    def visit(self):
        tree = self        
        for k in sorted(self._data.keys()):
            v = tree[k]
            for x in v.visit():
                yield x
                
        if self.leaf():
            yield self
                
    def items(self, afilter):
        
        for x in self.visit():
            match = True
            
            for k in afilter :
                d = x._path
                if k in d :
                    v1 = d[k]
                    v2 = afilter[k]
                    if v1 != v2 :
                        match = False
                else:
                    match = False
                if match :
                    yield x
                    
    
class ValTree(BaseTree) :
    def __init__(self):
        BaseTree.__init__(self)

    def pprint(self, indent=''):
        tree = self
        print indent,"st:",self._subtotal
        
        for k in sorted(self._data.keys()):
            v = tree[k]
            print indent,"K",k
                
            v.pprint(indent=indent+'\t')
        if self.leaf():
            self.debug_print(indent=indent+'\t')

class KeyTree(BaseTree) :
    def __init__(self, name):
        self.name = name

        BaseTree.__init__(self)
        
    def pprint(self, indent=''):
        tree = self
        print indent,"st:",self._subtotal
        for k in sorted(self._data.keys()):
            v = tree[k]
            print indent,"V",k
            v.pprint(indent=indent+'\t')
    
class Tree(BaseTree) :
    def __init__(self, fields):
        BaseTree.__init__(self)
        self._fields = fields        
    
    def keytree(self, tree, k):
        if not tree.contains(k) :
            tree[k]=KeyTree(k)
        return tree[k]

    def valtree(self, tree, k):
        if not tree.contains(k) :
            tree[k]=ValTree()
        return tree[k]
        
    def insert(self, x, count):
        tree = self
        tree.subtotal(count)
        path = {}        
        for k in self._fields:
            v = x[k]
            path[k]=None        
            ktree = self.keytree(tree,k)
            ktree.path(path)
            ktree.subtotal(count)
            path[k]=v
            vtree = self.valtree(ktree,v)
            vtree.path(path)
            vtree.subtotal(count)            
            tree = vtree


        tree.count(count)
        tree.debug_print("DEBUG")
        
    def pprint(self, indent=''):
        tree = self        
        for k in sorted(self._data.keys()):            
            v = tree[k]
            print indent,"Tree",k,tree._subtotal
            v.pprint(indent=indent+'\t')


        
test = [
    {  'data' : {'foo' :1,'bar':2,'baz':3},     'count' : 20    },
    {  'data' : {'foo' :1,'bar':2,'baz':3},     'count' : 1   },
    {  'data' : {'foo' :3,'bar':2,'baz':3},     'count' : 1   },
    {  'data' : {'foo' :1,'bar':2,'baz':2},     'count' : 1   },
    {  'data' : {'foo' :2,'bar':2,'baz':2},     'count' : 1   },
]

t = Tree(['foo','bar','baz'])

for x in test :
    d= x['data']
    c= x['count']
    t.insert(d,c)

t.pprint()

c = 0
for x in t.items({'baz':3}):
    c = c + x._count
print "Baz:3",c
