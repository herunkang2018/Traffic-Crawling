from contextlib import contextmanager

@contextmanager
def tag(name):
    print("<%s>" % name)
    a = 1
    yield a
    print("</%s>" % name)

with tag("h1") as q:
    print("hello")
    print("world")
    print(q)