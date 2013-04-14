from recursive_descent import RecursiveDescent

expr = 'true&~~false!~true&false'
print expr
print RecursiveDescent(expr).parse()