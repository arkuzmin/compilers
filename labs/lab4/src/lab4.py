from recursive_descent import RecursiveDescent

expr = 'truetruetrue'
print expr
print RecursiveDescent(expr).parse()