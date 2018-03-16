#!/usr/bin/env python3
import induce.refiner as refiner
import induce.miner as miner
import induce.grammar as g
import induce.config as config
import sys
import os
import pickle
from induce.bc import bc
import pudb; brk = pudb.set_trace

if os.getenv('SHOW_COMPARISONS') == 'true':
    config.Show_Comparisons = True

green = bc(bc.green)
blue = bc(bc.blue)
yellow = bc(bc.yellow)
red = bc(bc.red)

def nt_key_to_s(i):
    v = i.k
    return "[%s:%s]" % (v.func, v.var)

def process(lststr):
    i = 0
    last = None
    res = []
    plus = red('+')
    while i < len(lststr):
        v = lststr[i]
        i = i+1
        if len(res) == 0:
            res.append(v)
            continue
        if res[-1] == plus:
            if v == res[-2]:
                pass
            else:
                res.append(v)
        else:
            if v == res[-1]:
                res.append(plus)
            else:
                res.append(v)
    return ''.join(res)

if __name__ == "__main__":
    fin = sys.stdin.buffer if len(sys.argv) < 2 else open(sys.argv[1], 'rb')
    fout = sys.stdout if len(sys.argv) < 2 else open("%s.tmp" % sys.argv[1], 'w')
    grammar = pickle.load(fin)
    newg = {}
    for key in grammar.keys():
        rules = grammar[key]
        newk = green.o(nt_key_to_s(key))
        if newk not in newg:
            newg[newk] = set()
        newr = newg[newk]
        for r in rules:
            #assert r.comparisons
            my_str = []
            skip = False
            for i in r.rvalues():
                if type(i) == miner.NTKey:
                    str_var = blue.o(nt_key_to_s(i))
                    skip = True
                else:
                    pos = i.x()
                    str_var = str(i)
                my_str.append(str_var)
            if not skip and r.comparisons and config.Show_Comparisons:
                c = r.comparisons[pos]
                my_str.extend(["\t"] +
                        [
                         yellow('EQ_y:') + repr(''.join([str(i) for i in c['seq']]))     if c['seq'] else '',
                         yellow('NE_y:') + repr(''.join([str(i) for i in c['sne']]))     if c['sne'] else '',
                         yellow('IN_y:') + repr(''.join([''.join(i) for i in c['sin']])) if c['sin'] else '',
                         yellow('NI_y:') + repr(''.join([''.join(i) for i in c['sni']])) if c['sni'] else '',
                         yellow('EQ_X:') + repr(''.join([str(i) for i in c['feq']]))     if c['feq'] else '',
                         yellow('NE_x:') + repr(''.join([str(i) for i in c['fne']]))     if c['fne'] else '',
                         yellow('IN_x:') + repr(''.join([''.join(i) for i in c['fin']])) if c['fin'] else '',
                         yellow('NI_x:') + repr(''.join([''.join(i) for i in c['fni']])) if c['fni'] else '',
                         ])
            else:
                pass
                #my_str.extend([''])
            newr.add(process(my_str))
    x = g.Grammar(newg)
    if config.Compress_Grammar:
        x.compress()
    if len(sys.argv) > 1:
        print(str(x), file=sys.stderr)
    print(str(x), file=fout)
