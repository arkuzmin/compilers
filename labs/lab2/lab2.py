# -*- coding: utf-8 -*-

from cfgrammar import CFGrammar

#epsilon = unichr(949)
epsilon = u'e'

class CFGrammarTransformator:
    def RemoveUselessSymbols(self, g):  #2.9
        g_n = CFGrammar()
        g_n.terminals = g.terminals.copy()
        g_n.startSymbol = g.startSymbol
        reachableSet = self.GetReachableNonterminalsSet(g)
        g_n.nonTerminals = reachableSet.intersection(g.nonTerminals)
        validSymbolsSet = reachableSet.union(g_n.terminals)
        for rleft in g.rules.keys():
            if (rleft not in validSymbolsSet):
                continue
            rright = g.rules[rleft]
            for product in rright:
                isIn = True
                for s in product:
                    if s not in validSymbolsSet:
                        isIn = False
                        break
                if (isIn):
                    g_n.AddRule(rleft, product)

        #Устранение недостижимых символов
        g_n = self.RemoveUnreachableSymbols(g_n)
        return g_n
    
    '''
    Возвращает достижимое мно-во нетерминалов
    2.7
    '''
    def GetReachableNonterminalsSet(self, g):
        reachableSet = set()
        prevStepSize = 1
        while (len(reachableSet) != prevStepSize):
            reachableSet_n = set()
            for rleft in g.rules.keys():
                if rleft in reachableSet:
                    continue
                rright = g.rules[rleft]
                for product in rright:
                    isIn = True
                    for symbol in product:
                        if (symbol not in g.terminals and symbol not in reachableSet):
                            isIn = False
                            break
                    if isIn:
                        reachableSet_n.add(rleft)
            prevStepSize = len(reachableSet)
            reachableSet.update(reachableSet_n)
        return reachableSet

    '''2.8
    '''
    def RemoveUnreachableSymbols(self, g):
        g_n = CFGrammar()

        reachableSet = set([g.startSymbol])
        prevStepSize = 0
        while (len(reachableSet) != prevStepSize):
            reachableSet_n = set()
            for rleft in reachableSet:
                if rleft not in g.rules.keys():
                    continue
                rright = g.rules[rleft]
                for product in rright:
                    for symbol in product:
                        reachableSet_n.add(symbol)
            prevStepSize = len(reachableSet)
            reachableSet.update(reachableSet_n)


        g_n.startSymbol = g.startSymbol
        g_n.nonTerminals = reachableSet.intersection(g.nonTerminals)
        g_n.terminals = reachableSet.intersection(g.terminals)
        for rleft in g.rules.keys():
            if (rleft not in reachableSet):
                continue
            rright = g.rules[rleft]
            for product in rright:
                isIn = True
                for s in product:
                    if s not in reachableSet:
                        isIn = False
                        break
                if (isIn):
                    g_n.AddRule(rleft, product)
        return g_n

    '''2.10
    '''
    def RemoveEpsilonRules(self, g):
        g_n = CFGrammar()
        g_n.terminals = g.terminals.copy()
        g_n.nonTerminals = g.nonTerminals.copy()

        epsilonProducers = self.GetNonterminalsProducingEpsilons(g)

        for rleft in g.rules.keys():
            rright = g.rules[rleft]
            for product in rright:
                if product == [epsilon]:
                    continue
                epsProducersIndex = []
                for index in xrange(len(product)):
                    if product[index] in epsilonProducers:
                        epsProducersIndex.append(index)
                if len(epsProducersIndex) == 0 or epsProducersIndex == range(len(product)):
                    g_n.AddRule(rleft, product)
                    continue
                for i in xrange(0, 2**len(epsProducersIndex)):
                    pos = bin(i)[2:]
                    pos = '0' * (len(epsProducersIndex) - len(pos)) + pos
                    product_new = product[:]
                    backStep = 0
                    for j in xrange(len(pos)):
                        p = pos[j]
                        if p == '0':
                            del product_new[epsProducersIndex[j] - backStep]
                            backStep += 1
                    g_n.AddRule(rleft, product_new)

                #if product != epsilon:
                 #   g_n.AddRule(rleft, product)

        if g.startSymbol in epsilonProducers:
            nextSymbol = unichr(ord(max(g.terminals.union(g.nonTerminals))) + 1)
            g_n.startSymbol = nextSymbol
            g_n.nonTerminals.add(nextSymbol)
            g_n.AddRuleSet(nextSymbol, [[epsilon], [g.startSymbol]])
        else:
            g_n.startSymbol = g.startSymbol

        return g_n

    def GetNonterminalsProducingEpsilons(self, g):
        epsilonProducers = set()
        prevStepSize = 1
        for rleft in g.rules.keys():
            rright = g.rules[rleft]
            for product in rright:
                if product == [epsilon]:
                    epsilonProducers.add(rleft)
        prevStepSize = len(epsilonProducers) + 1
                        
        while (len(epsilonProducers) != prevStepSize):
            epsilonProducers_n = set()
            for rleft in g.rules.keys():
                rright = g.rules[rleft]
                isIn = True
                for product in rright:
                    for symbol in product:
                        if symbol not in epsilonProducers:
                            isIn = False
                            break
                    if isIn:
                        epsilonProducers_n.add(rleft)
                        break
            prevStepSize = len(epsilonProducers)
            epsilonProducers.update(epsilonProducers_n)
        return epsilonProducers

    def RemoveChainRules(self, g):
        g_n = CFGrammar()
        g_n.terminals = g.terminals.copy()
        g_n.nonTerminals = g.nonTerminals.copy()
        g_n.startSymbol = g.startSymbol

        N = {}              # нетерминал : множество выводимых из него
        for rleft in g.rules.keys():
            N[rleft] = set([rleft])
            reachableSet = N[rleft]
            prevStepSize = 0
            while (len(reachableSet) != prevStepSize):
                reachableSet_n = set()
                for rleft in reachableSet:
                    if rleft not in g.rules.keys():
                        continue
                    rright = g.rules[rleft]
                    for product in rright:
                        if len(product) == 1 and product[0] in g.nonTerminals:
                            reachableSet_n.add(product[0])
                prevStepSize = len(reachableSet)
                reachableSet.update(reachableSet_n)

        '''
        reverseN = {}       # нетерминал : множество нетерминалов, из которых он выводится
        for rleft in g.rules.keys():
            reverseN[rleft] = set()
        for rleft in g.rules.keys():
            reachableSet = reverseN[rleft]
            prevStepSize = 0
            while (len(reachableSet) != prevStepSize):
                reachableSet_n = set()
                for rleft in reachableSet:
                    rright = g.rules[rleft]
                    for product in rright:
                        if len(product) == 1 and product in g.nonTerminals:
                            reverseN[product].add(rleft)
                prevStepSize = len(reachableSet)
                reachableSet.update(reachableSet_n)
                '''

        for rleft in g.rules.keys():
            rright = g.rules[rleft]
            for product in rright:
                if len(product) == 1 and product[0] in g.nonTerminals:
                    continue
                for parent in N.keys():
                    if rleft in N[parent]:
                        g_n.AddRule(parent, product)

        return g_n


g = CFGrammar()
g.terminals = set([u'a',u'b',u'c', epsilon])
g.nonTerminals = set([u'A',u'B',u'C',u'D',u'E',u'S'])
g.startSymbol = u'S'
g.AddRuleSet(u'S', [[u'A'], [u'B']])
g.AddRuleSet(u'A', [[u'C'], [u'D']])
g.AddRuleSet(u'B', [[u'D'], [u'E']])
g.AddRuleSet(u'C', [[u'S'], [u'a'], [epsilon]])
g.AddRuleSet(u'D', [[u'S'], [u'b']])
g.AddRuleSet(u'E', [[u'S'], [u'c'], [epsilon]])

g.SaveToXml('0_inputGrammar.xml')

t = CFGrammarTransformator()
g.PrintToConsole('Initial grammar')
g1 = t.RemoveUselessSymbols(g)
g1.PrintToConsole('Useless symbols removed')
g1.SaveToXml('1_removed_UselessSymbols.xml')
g2 = t.RemoveEpsilonRules(g1)
g2.PrintToConsole('Epsilon rules removed')
g2.SaveToXml('2_removed_EpsilonRules.xml')
g3 = t.RemoveChainRules(g2)
g3.PrintToConsole('Cycles removed')
g3.SaveToXml('3_removed_Cycles.xml');
pass