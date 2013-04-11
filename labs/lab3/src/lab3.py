from grammar import Grammar, Rule, Nonterminal, Terminal, EmptySymbol, Symbol
from topdown_parser import Configuration, TopDownParser

grammar = Grammar()
'''terminals'''

tEq = Terminal('=')
tNeq = Terminal('<>')
tLt = Terminal('<')
tLe = Terminal('<=')
tGt = Terminal('>')
tGe = Terminal('>=')
tPl = Terminal('+')
tMi = Terminal('-')
tOr = Terminal('or')
tMu = Terminal('*')
tDi = Terminal('/')
tDiv = Terminal('div')
tMod = Terminal('mod')
tAnd = Terminal('and')
tNot = Terminal('not')
tOpenBr = Terminal('(')
tCloseBr = Terminal(')')
tIdentifier = Terminal('<identifier>')
tConst = Terminal('<const>')

grammar.terminals.update([tEq, tNeq, tLt, tLe, tGt, tGe, tPl, tMi, tOr, tMu, tDi, tDiv, tMod, tAnd, tNot, tOpenBr, tCloseBr, tIdentifier, tConst])

'''nonterminals'''
S = Nonterminal('S')
B = Nonterminal('B')
A = Nonterminal('A')
T = Nonterminal('T')
Z = Nonterminal('Z')
P = Nonterminal('P')
F = Nonterminal('F')
M = Nonterminal('M')

grammar.nonterminals.update([S, A, B, T, Z, P, F])
grammar.axiom = S

'''rules'''
grammar.rules.append(Rule([S], [A]))
grammar.rules.append(Rule([S], [A, B, A]))
grammar.rules.append(Rule([A], [T]))
grammar.rules.append(Rule([A], [Z, T]))
grammar.rules.append(Rule([A], [A, P, T]))
grammar.rules.append(Rule([T], [F]))
grammar.rules.append(Rule([T], [T, M, F]))
grammar.rules.append(Rule([F], [tIdentifier]))
grammar.rules.append(Rule([F], [tConst]))
grammar.rules.append(Rule([F], [tOpenBr, A, tCloseBr]))
grammar.rules.append(Rule([F], [tNot, F]))
grammar.rules.append(Rule([B], [tEq]))
grammar.rules.append(Rule([B], [tNeq]))
grammar.rules.append(Rule([B], [tLt]))
grammar.rules.append(Rule([B], [tLe]))
grammar.rules.append(Rule([B], [tGt]))
grammar.rules.append(Rule([B], [tGe]))
grammar.rules.append(Rule([Z], [tPl]))
grammar.rules.append(Rule([Z], [tMi]))
grammar.rules.append(Rule([P], [tPl]))
grammar.rules.append(Rule([P], [tMi]))
grammar.rules.append(Rule([P], [tOr]))
grammar.rules.append(Rule([M], [tMu]))
grammar.rules.append(Rule([M], [tDi]))
grammar.rules.append(Rule([M], [tDiv]))
grammar.rules.append(Rule([M], [tMod]))
grammar.rules.append(Rule([M], [tAnd]))

print "grammar:\n", grammar

grammar.removeLeftRecursion()

print "left recursions removed: \n", grammar


expr = [tOpenBr, tIdentifier, tMi, tConst, tCloseBr, tMu, tOpenBr, tIdentifier, tPl, tIdentifier, tCloseBr]
print "expr: %s\n" % ''.join([str(symbol) for symbol in expr])

parser = TopDownParser(grammar)
parser.parse(expr)
