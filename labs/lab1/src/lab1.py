# -*- coding: utf-8 -*-
import os.path
import pydot

epsilon = None

class Utils:
    @staticmethod
    def ensureDictHasKey(d, key, value):
        if not d.has_key(key):
            d[key] = value

class FA:
    def __init__(self):
        self.initialState = 0
        self.finalStates = set()
        self.transitions = {}   #ddl = {state : {symbol : [state, ...]}, ...}
        self.stateCount = 0
        self.epsilonIncedentStates = set()

    def __len__(self):
        return self.stateCount

    def copyStatesWithStep(self, fa, step):
        for state_1 in fa.transitions.keys():
            trans = fa.transitions[state_1]
            state_with_step = state_1 + step
            self.transitions[state_with_step] = {}
            for symbol in trans.keys():
                self.transitions[state_with_step][symbol] = [e + step for e in trans[symbol]]

        for s in fa.epsilonIncedentStates:
            self.epsilonIncedentStates.add(s + step)

#Конструктор Томпсона для построение NFA по регулярному выражению
class TomphsonCtor:
    #Регулярное выражение состоит из одного символа
    def CreateFaSymbol(self, symbol):
        fa = FA()
        fa.initialState = 0
        fa.finalStates.add(1)
        fa.transitions[0] = {symbol : [1]}
        fa.stateCount = 2
        return fa

    #Операция или (a|b)
    def CreateFaOr(self, fa_1, fa_2):
        fa = FA()
        f_1_step = 1
        fa.copyStatesWithStep(fa_1, f_1_step);
        f_2_step = len(fa_1) + 1
        fa.copyStatesWithStep(fa_2, f_2_step);
        fa.initialState = 0
        fa.transitions[0] = {epsilon : [1,  len(fa_1) + 1]}
        f2_first = len(fa_1) + 1
        final = len(fa_1) + len(fa_2) + 1
        fa.finalStates.add(final)
        for f in fa_1.finalStates:
            if not fa.transitions.has_key(f + f_1_step):
                fa.transitions[ f + f_1_step ] = {}
            if not fa.transitions[ f + f_1_step ].has_key(epsilon):
                fa.transitions[ f + f_1_step ][epsilon] = []
            fa.transitions[ f + f_1_step ][epsilon].append(final)

        for f in fa_2.finalStates:
            if not fa.transitions.has_key(f + f_2_step):
                fa.transitions[ f + f_2_step ] = {}
            if not fa.transitions[f + f_2_step].has_key(epsilon):
                fa.transitions[f + f_2_step][epsilon] = []
            fa.transitions[ f + f_2_step ][epsilon].append(final)
        fa.stateCount = final + 1
        fa.epsilonIncedentStates.add(1)
        fa.epsilonIncedentStates.add(f2_first)
        fa.epsilonIncedentStates.add(final)
        return fa

    def CreateFaConcat(self, fa_1, fa_2):
        fa = FA()
        f_1_step = 1
        fa.copyStatesWithStep(fa_1, f_1_step);
        f_2_step = len(fa_1) + 1
        fa.copyStatesWithStep(fa_2, f_2_step);
        fa.initialState = 0
        fa.transitions[0] = {epsilon : [1]}
        final = len(fa_1) + len(fa_2) + 1
        f2_first = len(fa_1) + 1
        fa.finalStates.add(final)
        for f in fa_1.finalStates:
            if not fa.transitions.has_key( f + f_1_step ):
                fa.transitions[ f + f_1_step ] = {}
            if not fa.transitions[ f + f_1_step ].has_key(epsilon):
                fa.transitions[ f + f_1_step ][epsilon] = []
            fa.transitions[ f + f_1_step ][epsilon].append(f2_first)

        for f in fa_2.finalStates:
            if not fa.transitions.has_key(f + f_2_step):
                fa.transitions[ f + f_2_step ] = {}
            if not fa.transitions[f + f_2_step].has_key(epsilon):
                fa.transitions[f + f_2_step][epsilon] = []
            fa.transitions[ f + f_2_step ][epsilon].append(final)

        fa.epsilonIncedentStates.add(1)
        fa.epsilonIncedentStates.add(f2_first)
        fa.epsilonIncedentStates.add(final)
        fa.stateCount = final + 1
        return fa

    def CreateFaIterPositive(self, fa_r):
        fa = FA()
        step = 1
        fa.copyStatesWithStep(fa_r, step)
        final = len(fa_r) + 1
        fa.transitions[0] = {epsilon : [1]}
        fa.finalStates = [final]
        for f in fa_r.finalStates:
            if not fa.transitions.has_key(f + step):
                fa.transitions[ f + step ] = {}
            if not fa.transitions[f + step].has_key(epsilon):
                fa.transitions[f + step][epsilon] = []
            fa.transitions[ f + step ][epsilon].append(1)
            fa.transitions[ f + step ][epsilon].append(final)
        fa.stateCount = len(fa_r) + 2
        fa.epsilonIncedentStates.add(1)
        fa.epsilonIncedentStates.add(final)
        return fa

    def CreateFaIter(self, fa_r):
        fa = self.CreateFaIterPositive(fa_r)
        fa.transitions[0][epsilon].append(len(fa) - 1)
        return fa

# | . * + ( )
class RPN:
    def __init__(self):
        self.opers = ('|' , '.', '*', '+')

    def Transform2ReversePolishNotation(self, seq):
        stack = []
        priors = {'(' : 0, '|' : 2 , '.' : 3, '*' : 4, '+' : 4}
        opers = priors.keys()
        out = ''
        for s in seq:
            if s == '(':
                stack.append(s)
            elif s == ')':
                s = ''
                while (s != '(' and len(stack) != 0):
                    s = stack.pop()
                    out += s
                if (s != '('):
                    return None
                out = out[:-1]
            elif s in opers:
                if (len(stack) != 0):
                    if (priors[s] >= priors[stack[len(stack) - 1]]):
                        stack.append(s)
                    else:
                        while ( (len(stack) != 0 ) and (priors[s] < priors[stack[len(stack) - 1]])):
                            out += stack.pop()
                        stack.append(s)
                else:
                    stack.append(s)
            else:
                out += s
        while(len(stack) != 0):
            out += stack.pop()
        return out

    def HandleRPN(self, rpn_str):
        t = TomphsonCtor()
        stack = []
        index = 0
        for s in rpn_str:
            if s in self.opers:
                if s in ('|', '.') :
                    if s == '|':
                        f = t.CreateFaOr
                    else:
                        f = t.CreateFaConcat
                    fa_2 = stack.pop()
                    fa_1 = stack.pop()
                    stack.append(f(fa_1, fa_2))
                elif s == '*':
                    stack.append(t.CreateFaIter(stack.pop()))
                elif s == '+':
                    stack.append(t.CreateFaIterPositive(stack.pop()))
            else:
                stack.append(t.CreateFaSymbol(s))
        if (len(stack) != 1):
            return None
        fa = stack.pop()
        return fa

    def BuildFa(self, regexp):
        return self.HandleRPN(self.Transform2ReversePolishNotation(regexp))

class Determinisator:
    def Determine(self, fa):
        if len(fa.epsilonIncedentStates) != 0:
            faNoEps = self.RemoveEpsilonTransitions(fa)
        else:
            faNoEps = fa
        detFa = self.GetDetFa(faNoEps)
        return detFa

    def RemoveEpsilonTransitions(self, fa):
        detFa = FA()
        # В эти состояния есть не epsilon переходы
        detStates = [x for x in range(0, len(fa) - 1) if x not in fa.epsilonIncedentStates]
        detTransitions = {}
        detFinalStates = set()
        for state in detStates:
            reachSet = self.DefineReachSet(fa, state)
            if (state in fa.finalStates) or (fa.finalStates & reachSet):
                detFinalStates.add(state)
            for r in reachSet:
                if fa.transitions.has_key(r):
                    for symbol in fa.transitions[r].keys():
                        if symbol != epsilon:
                            Utils.ensureDictHasKey(detTransitions, state, {})
                            Utils.ensureDictHasKey(detTransitions[state], symbol, [])
                            detTransitions[state][symbol].extend(fa.transitions[r][symbol])
        stateMapping = dict(zip(detStates, range(len(detStates))))
        detFa.stateCount = len(detStates)
        detFa.finalStates = [stateMapping[f] for f in detFinalStates]
        for s1 in detTransitions:
            s1_n = stateMapping[s1]
            Utils.ensureDictHasKey(detFa.transitions, s1_n, {})
            for symbol in detTransitions[s1]:
                detFa.transitions[s1_n][symbol] = [stateMapping[s2] for s2 in detTransitions[s1][symbol]]
        return detFa

    def DefineReachSet(self, fa, state):
        reachSet = set()
        currReachSet = set([state])
        prevStepReachSetSize = 1
        while (len(reachSet) != prevStepReachSetSize):
            prevStepReachSetSize = len(reachSet)
            nextReachSet = set()
            for s1 in currReachSet:
                if fa.transitions.has_key(s1) and fa.transitions[s1].has_key(epsilon):
                    for s2 in fa.transitions[s1][epsilon]:
                        if s2 not in reachSet:
                            reachSet.add(s2)
                            nextReachSet.add(s2)
            currReachSet = nextReachSet
        return reachSet

    def GetDetFa(self, faWithoutEpsilon):
        fa = faWithoutEpsilon
        detFa = FA()
        detFa.initialState = 0
        initialSet = (0,)
        stateMapping = {initialSet : 0}
        leftStates = [initialSet]
        while len(leftStates) != 0:
            leftStates_new = []
            for state_set in leftStates:
                s1_n = stateMapping[tuple(state_set)]
                for s in state_set:
                    if s in fa.finalStates:
                        detFa.finalStates.add(s1_n)
                        break
                Utils.ensureDictHasKey(detFa.transitions, s1_n, {})

                state_set_symbols = set()
                for s in state_set:
                    if fa.transitions.has_key(s):
                        state_set_symbols.update(fa.transitions[s].keys())
                for symbol in state_set_symbols:
                    newState = set()
                    for s1 in state_set:
                        if fa.transitions.has_key(s1) and symbol in fa.transitions[s1].keys():
                            newState.update(fa.transitions[s1][symbol])
                    if len(newState) != 0:
                        state_tup = tuple(newState)
                        if stateMapping.has_key(state_tup): #Либо берем только что добавленное состояние, либо то которое уже было
                            s2_n = stateMapping[state_tup]
                        else:
                            leftStates_new.append(newState)
                            s2_n = len(stateMapping)
                            stateMapping[state_tup] = len(stateMapping)
                        Utils.ensureDictHasKey(detFa.transitions[s1_n], symbol, s2_n)
            leftStates = leftStates_new
        detFa.stateCount = len(detFa.transitions.keys())
        return detFa

class Minimisator:
    def Minimize(self, fa):
        st2cl = {}
        initialiClass0 = set()
        initialiClass1 = set()
        for f in xrange(len(fa)):   #0 - разбиение
            if f in fa.finalStates:
                st2cl[f] = 0
                initialiClass0.add(f)
            else:
                st2cl[f] = 1
                initialiClass1.add(f)
        hasNew = True
        classes = [tuple(initialiClass0), tuple(initialiClass1)]
        while (hasNew):
            classes_size = len(classes)
            new_classes = []
            for c in classes:
                new_classes.extend(self.SplitClass(fa, c, st2cl))
            #пересчитываем st2cl
            st2cl = self.RecalcState2ClassMapping(new_classes)
            hasNew = classes_size != len(new_classes)
            classes = new_classes

        if (len(fa) == len(classes)):
            return fa

        minFa = FA()
        cl2st = {}
        i = 0
        for c in classes:
            cl2st[c] = i
            i += 1

        foundInitState = False
        minFa.stateCount = len(classes)
        for c in classes:
            oldState = c[0]
            newState = cl2st[c]

            if (not foundInitState) and (fa.initialState in c):
                minFa.initialState = newState
                foundInitState = True

            if not fa.finalStates.isdisjoint(c):
                minFa.finalStates.add(newState)

            Utils.ensureDictHasKey(minFa.transitions, newState, {})
            for symbol in fa.transitions[oldState].keys():
                minFa.transitions[newState][symbol] = st2cl[fa.transitions[oldState][symbol]]

        #return self.changeStatesNames(minFa)
        return minFa

    def changeStatesNames(self, fa):
        correctedFa = FA()
        for startState in fa.transitions.keys():
            correctedFa.transitions[len(fa) - startState - 1] = {}
            trans = fa.transitions[startState]
            for symbol in trans.keys():
                e = trans[symbol]
                correctedFa.transitions[len(fa) - startState - 1][symbol] = len(fa) - 1 - e

        correctedFa.initialState = len(fa)-1-fa.initialState
        correctedFa.finalStates = [len(fa) - 1 - e for e in fa.finalStates]
        correctedFa.stateCount = fa.stateCount
        return correctedFa

    def SplitClass(self, fa, _class, st2cl):
        if len(_class) == 1:
            return [_class]
        new_classes = []
        trans2st = {}
        for s1 in _class:
            t = fa.transitions[s1]
            transDefinition = []
            for symbol in t.keys():
                transDefinition.append((symbol, st2cl[t[symbol]]))
            transDefinition = tuple(transDefinition)
            if trans2st.has_key(transDefinition):
                trans2st[transDefinition].append(s1)
            else:
                trans2st[transDefinition] = [s1]

        return [tuple(x) for x in trans2st.values()]

    def RecalcState2ClassMapping(self, classes):
        st2cl = {}
        class_index = 0
        for c in classes:
            for s in c:
                st2cl[s] = class_index
            class_index += 1
        return st2cl

class FaSimulator:
    def Simulate(self, fa, seq):
        state = fa.initialState
        path = [state]
        for c in seq:
            if fa.transitions[state].has_key(c):
                state = fa.transitions[state][c]
                path.append(state)
            else:
                return (False, path)
        if state in fa.finalStates:
            return (True, path)
        else:
            return (False, path)

class FaGraphVizExporter:
    def convert(self, fa, list):
        g = pydot.Dot(graph_type='digraph')
        map = {}
        for c in xrange(fa.stateCount):
            if fa.initialState == c:
                map[c] = pydot.Node('%d' % (c,), shape='doublecircle')
                g.add_node(map[c])
            if c in fa.finalStates:
                map[c] = pydot.Node('%d' % (c,), shape='doublecircle')
                g.add_node(map[c])
            map[c] = pydot.Node('%d' % (c,))
            g.add_node(map[c])
        for s1 in fa.transitions.keys():
            t = fa.transitions[s1]
            for symbol in t.keys():
                if list:
                    toList = t[symbol]
                    for toPnt in toList:
                        g.add_edge(pydot.Edge(map[s1], map[toPnt], label=symbol))
                else:
                    g.add_edge(pydot.Edge(map[s1], map[t[symbol]], label=symbol))
        return g

    def export(self, fa, path, list=False):
        g = self.convert(fa, list)
        if os.path.exists(path):
            os.remove(path)
        g.write_png(path)


class GraphConsoleExporter:
    
    def append(self, fa, name): 
        output = self.formOutput(fa, name)
        self.consoleExport(output)
        self.fileExport(output, '.\out\out.txt', "a")
    
    def export(self, fa, name):
        output = self.formOutput(fa, name)
        self.consoleExport(output)
        self.fileExport(output, '.\out\out.txt', "w")
    
    def fileExport(self, output, filename, param):
        try:
            f = open(filename, param)
            try:
                for str in output: 
                    f.write(str + '\n')
            finally:
                f.close()
        except IOError:
            pass

    def consoleExport(self, output):
        for str in output: 
            print(str)
        
    def formOutput(self, fa, name):
        initialstates = []
        finalstates = []
        states = []
        output = []
        for c in xrange(fa.stateCount):
            if fa.initialState == c:
                initialstates.append(c)
            if c in fa.finalStates:
                finalstates.append(c)
            states.append(c)
        output.append('initialstates: ' + str(initialstates))
        output.append('finalstates:   ' + str(finalstates))
        output.append('states:        ' + str(states))
        
        output.append('-----------------    ' + name + '     ---------------------')
        for s1 in fa.transitions.keys():
            t = fa.transitions[s1]
            for symbol in t.keys():
                strsym = str(symbol)
                if strsym == 'None':
                   strsym = 'N'
                output.append(str(s1) + ' --(' + strsym + ')--> ' + str(t[symbol]))
        output.append('-------------------------------------------------')
        output.append('')
        output.append('')
        
        return output

class App:
    def __init__(self):
        self.rpn = RPN()
        self.det = Determinisator()
        self.min = Minimisator()
        self.sim = FaSimulator()
        self.exp = GraphConsoleExporter()
        self.graph = FaGraphVizExporter()

    def main(self):
        #try:
        """


        """
        regexp = raw_input('Put your regular expression:')
        print('Parsing with Reverse Polish Notation, building automate...\n')
        fa = self.rpn.BuildFa(regexp)
        self.exp.export(fa, 'INITIAL FA')
        #self.graph.export(fa, '.\out\initial.png', True)
        print('Determining automate...\n')
        detFa = self.det.Determine(fa)
        self.exp.append(detFa, 'DETERMINED FA')
        self.graph.export(detFa, '.\out\determined.png')
        print('Minimizing automate...\n')
        minFa = self.min.Minimize(detFa)
        self.exp.append(minFa, 'MINIMIZED FA')
        self.graph.export(minFa, '.\out\minimized.png')
        print('The automate is successfully built. Input chain to parse or an empty chain to finish work:\n')
        seq = raw_input('Chain:')
        while (seq != ''):
            result = self.sim.Simulate(minFa, seq)
            if (result[0]):
                print('Parsed! The parsing trac: %s\n' % (result[1], ))
            else:
                print('Error char sequence! The parsing trac: %s\n' % (result[1], ))
            seq = raw_input('Chain:')

        #except Exception as ex:
         #   print(u'Ошибка', ex)

'''
(a|b)*.(c.d)+
(a|b|c|d|e|f|g).(4|5|6|7|8|9)*
'''
App().main()
