
def iteration( co):
    steps = 0
    u = co.n
    while 1:
        if u % 2 == 1:
            u = (3*u+1)//2
        else:
            u = u//2
        steps += 1
        if u == co.n:
            print(f"Found loop.")
            break
        if u < co.n:
            break
    assert co.n_w == u and co.steps == steps
    print( f"Checking: {hex(co.n)} {hex(u)} steps={steps}")

class CollatzObject:
    def __repr__(self):
        return f"{(hex(self.stride),hex(self.n))} {(hex(self.stride_w),hex(self.n_w))} steps={self.steps}"

    def __init__(self, stride, n, stride_w=None, n_w=None, steps=0):
        self.steps = steps
        self.stride = stride
        self.n = n
        if stride_w is not None:
            self.stride_w = stride_w
            self.n_w = n_w
        else:
            self.stride_w = self.stride
            self.n_w = self.n
            self.step()

    def protected_step(self):
        if self.eq():
            raise Exception("Found loop")
        elif self.le():
            print( f"Stopping {self}")
            iteration(self)
            return []
        else:
            return self.step()

    def step(self):
        if self.stride_w % 2 == 1:
            k = 1
            kk = 1<<k
            result = []
            for i in range( kk):
                result.append( CollatzObject( self.stride*kk, self.n+i*self.stride,
                                         self.stride_w*kk, self.n_w+i*self.stride_w,
                                         self.steps))
            print( f"Spliting {self} into {result}")
            return [ y for x in result for y in x.step()]
        else:
            self.steps += 1
            if self.n_w % 2 == 1:
                self.stride_w, self.n_w = 3*self.stride_w//2, (3*self.n_w+1)//2
            else:
                self.stride_w, self.n_w = self.stride_w//2, self.n_w//2
            return [self]

    def le(self):
        return self.stride_w <= self.stride and self.n_w <= self.n

    def eq(self):
        return self.stride_w == self.stride and self.n_w == self.n


from collections import deque


def depth_first():    
    q = deque()

    q.append(CollatzObject(6,1))
    q.append(CollatzObject(6,3))

    iter = 0

    while len(q) > 0 and iter < 1000:
        co = q.pop()
        print( f"Iter: {iter} Count: {len(q)} Popping {co}")
        for x in co.protected_step():
            q.append(x)
            print( f"\tPushing {x}")
        iter += 1
        
    for x in q:
        print(f"\tPending {x}")
    print( f"Items pending: {len(q)}")


def breadth_first():    
    q = deque()

    q.append(CollatzObject(6,1))
    q.append(CollatzObject(6,3))

    iter = 0

    while len(q) > 0 and iter < 10000000:
        iter += 1
        co = q.popleft()
        print( f"Iter: {iter} Count: {len(q)} Dequeuing {co}")
        lst = co.protected_step()
        for x in lst:
            q.append(x)
            print( f"\tEnqueuing {x}")
        
    for x in q:
        print(f"\tPending {x}")
    print( f"Items pending: {len(q)}")

import random

def mixed_first():
    
    rnd = random.Random()

    q = deque()

    q.append(CollatzObject(6,1))
    q.append(CollatzObject(6,3))

    iter = 0

    while len(q) > 0 and iter < 10000000:
        coin = rnd.randrange(100)

        if coin > 0:
            co = q.pop()
            tag = "Popping"
        else:
            co = q.popleft()
            tag = "Dequeuing"
        print( f"Iter: {iter} Count: {len(q)} {tag} {co}")
        for x in co.protected_step():
            q.append(x)
            print( f"\tPushing {x}")
        iter += 1
        
def test_A():
    breadth_first()

def test_B():
    depth_first()

def test_C():
    mixed_first()
    
