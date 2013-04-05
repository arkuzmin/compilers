# -*- coding: utf-8 -*-
from sys import stdout
from xml.dom.minidom import Document, parseString, parse
import codecs

class CFGrammar:
    def __init__(self):
        self.nonTerminals = set()
        self.terminals = set()
        self.startSymbol = None
        self.rules = dict()
        #self.rules = {'A' : list(list('BcA', 'B', 'd'),  list(), ...)}

    def AddRule(self, nonTerm, product):
        if not self.rules.has_key(nonTerm):
            self.rules[nonTerm] = []
        self.rules[nonTerm].append(product) #product = []

    def AddRuleSet(self, nonTerm, produceList):
        for p in produceList:
            self.AddRule(nonTerm, p)

    xml_keyword_grammar = 'grammar'
    xml_keyword_terminals = 'terminals'
    xml_keyword_terminal = 'terminal'
    xml_keyword_nonterminals = 'nonterminals'
    xml_keyword_nonterminal = 'nonterminal'
    xml_keyword_startSymbol = 'startSymbol'
    xml_keyword_rules = 'rules'
    xml_keyword_rule = 'rule'
    xml_keyword_product = 'product'
    xml_keyword_symbol = 'symbol'
    xml_keyword_value_attr = 'value'
    
    def PrintToConsole(self, name):
        print('******************************************')
        print(name)
        print('******************************************')
        stdout.write('NON TERMINALS:')
        for n in self.nonTerminals:
            print(n)
        print('')
        print('TERMINALS:')
        for t in self.terminals: 
            print(t)
        print('')
        print('START SYMBOL:')
        print(self.startSymbol)
        for rleft in self.rules.keys():
            rright = self.rules[rleft]
            first = True
            for product in rright: 
                if first: 
                    stdout.write('\n'+ str(rleft) + ' --> ' + unicode(product))
                    first = False
                else:
                    stdout.write('|' + unicode(product))
        stdout.write('\n\n')
        

    def SaveToXml(self, fileName):
        doc = Document()
        grammar = doc.createElement(CFGrammar.xml_keyword_grammar)
        doc.appendChild(grammar)
        terminals = doc.createElement(CFGrammar.xml_keyword_terminals)
        grammar.appendChild(terminals)
        for t in self.terminals:
            tdoc = doc.createElement(CFGrammar.xml_keyword_terminal)
            tdoc.setAttribute(CFGrammar.xml_keyword_value_attr, t)
            terminals.appendChild(tdoc)
        nonterminals = doc.createElement(CFGrammar.xml_keyword_nonterminals)
        grammar.appendChild(nonterminals)
        for n in self.nonTerminals:
            nontdoc = doc.createElement(CFGrammar.xml_keyword_nonterminal)
            nontdoc.setAttribute(CFGrammar.xml_keyword_value_attr, n)
            nonterminals.appendChild(nontdoc)
        startSymbol = doc.createElement(CFGrammar.xml_keyword_startSymbol)
        startSymbol.setAttribute(CFGrammar.xml_keyword_value_attr, self.startSymbol)
        grammar.appendChild(startSymbol)
        rules = doc.createElement(CFGrammar.xml_keyword_rules)
        grammar.appendChild(rules)
        for rleft in self.rules.keys():
            rright = self.rules[rleft]
            rule = doc.createElement(CFGrammar.xml_keyword_rule)
            rule.setAttribute(CFGrammar.xml_keyword_value_attr, rleft)
            rules.appendChild(rule)
            for product in rright:
                productdoc = doc.createElement(CFGrammar.xml_keyword_product)
                rule.appendChild(productdoc)
                for symbol in product:
                    docsymbol = doc.createElement(CFGrammar.xml_keyword_symbol)
                    docsymbol.setAttribute(CFGrammar.xml_keyword_value_attr, symbol)
                    productdoc.appendChild(docsymbol)


        with codecs.open(fileName, "w", "utf-8") as out:
            doc.writexml(out)

    @staticmethod
    def CreateFromXml(fileName):
        f = codecs.open( fileName, "r", "utf-8" )
        content = codecs.encode(f.read(), "utf-8")
        doc = parseString(content)
        f.close()
        g = CFGrammar()
        grammar = doc.childNodes[0]
        terms = grammar.childNodes[0]
        for t in terms.childNodes:
            g.terminals.add(t.getAttribute(CFGrammar.xml_keyword_value_attr))
        nonterms = grammar.childNodes[1]
        for n in nonterms.childNodes:
            g.nonTerminals.add(n.getAttribute(CFGrammar.xml_keyword_value_attr))
        g.startSymbol = grammar.childNodes[2].getAttribute(CFGrammar.xml_keyword_value_attr)
        rules = grammar.childNodes[3]
        for r in rules.childNodes:
            rleft = r.getAttribute(CFGrammar.xml_keyword_value_attr)
            products = r.childNodes
            for p in products:
                rright = []
                for symbol in p.childNodes:
                    rright.append(symbol.getAttribute(CFGrammar.xml_keyword_value_attr))
                g.AddRule(rleft, rright)

        return g

