def example(a, b, **kw):
    return a * b

print(type(example))
print(example.__code__.co_varnames)
print(example.__code__.co_argcount)
