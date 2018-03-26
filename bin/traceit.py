#!/usr/bin/env python3
import sys
sys.path.append('.')
import resource
resource.setrlimit(resource.RLIMIT_STACK, [0x10000000, resource.RLIM_INFINITY])
sys.setrecursionlimit(0x100000)

import taintedstr
import sys
import os.path
import pygmalion.ftrace as tracer
import pickle
import imp
from contextlib import contextmanager

@contextmanager
def opened_file(f):
    if not f:
        yield sys.stdout.buffer
    else:
        with open(f, 'wb') as f:
            yield f

if __name__ == "__main__":
    m_file = sys.argv[1]
    mod_obj = imp.new_module('example')
    mod_obj.__file__ = m_file
    code = compile(open(m_file).read(), os.path.basename(m_file), 'exec')
    exec(code, mod_obj.__dict__)
    if len(sys.argv) > 2:
        fn = sys.argv[2]
    else:
        fn = None
    with opened_file(fn) as trace_file:
        # Infer grammar
        for j,_i in enumerate(sys.stdin):
            assert _i[-1] == "\n"
            i = taintedstr.tstr(_i[0:-1]) # strip '\n'
            print("trace:",j, repr(i), file=sys.stderr)
            with tracer.Tracer(i, trace_file) as t:
                t._my_files = ['%s' % os.path.basename(m_file)]
                t._skip_classes = mod_obj.skip_classes() if hasattr(mod_obj, 'skip_classes') else []
                o = mod_obj.main(i)
