import os
# [Procedure calls]
# Why should we not track params to a function? because
# the input string may get progressively eaten rather than
# split recursively. So the input string variable actually
# causes more noise than signal.
Track_Params = True

Track_Vars = True

# Why we do not care about return values?
# * We expect the input value to be partitioned by each
#   procedure. Hence, the variables inside the procedures
#   are important. However, the return value of a given
#   procedure may not include the correct result. Even if
#   it did, it is probably already assigned an internal
#   variable (i.e: return my_val) in which case, we dont care
#   If not, (i.e: return i+j), the result may not represent
#   a sequence of input string.
Track_Return = False

# []

# Lambdas typicaly are unimportant, and contribute to noise.
Ignore_Lambda = True

# What should we do if we have a variable that eclipses already
# replaced variables?
# e.g
# x = peek()
# if x == '[': parseSqBr()
# def parseSqBr:
#    v = eatUntilEnd(']')
# now, x contains '[' but if x is processed, v will be ignored
# because any rule that contains x will be ineligible for v.
# similarly,
# strval = ''
# while hasNext:
#    char = peek()
#    if char in digits:
#       strval += char
# here, the char gets tainted first, and will not be a part of
# strval eventhough it obviously is. This is an interplay between
# input and output formats.

Swap_Eclipsing_Keys = (os.getenv('SWAP_PEEK') or 'true') in {'true', '1'}

# should we discard the peeking variables that got eclipsed?
Strip_Peek = (os.getenv('STRIP_PEEK') or 'true') in {'true', '1'}

# [Verbosity]

Show_Colors = True

Show_Comparisons = True

Refine_Tactics = (os.getenv('REFINE_TACTICS') or ','.join([
        'single_repeat',
        'remove_single_alternatives',
        'compress_keys'])).split(',')

# True: only replace things at a lower height with something
# at higher height. This is useful mainly when we decide whether
# to split inner method values after the inner method returns.
Prevent_Deep_Stack_Modification = False

Use_Character_Classes = True

Python_Specific = (os.getenv('PYTHON_OPT') or 'false') in {'true', '1'}

StdErr_DevNull=(os.getenv('NO_LOG') or 'false') in {'true', '1'}

if StdErr_DevNull:
    import sys
    f = open(os.devnull, 'w')
    sys.stderr = f

With_Char_Class =  (os.getenv('WITH_CHAR_CLASS') or 'true') in {'true', '1'}

Skip_Refine =  (os.getenv('SKIP_REFINE') or 'false') in {'true', '1'}

Infer = (os.getenv('INFER') or 'UNSOUND')
Simple_Class = (os.getenv('CCLASS') or 'false') in {'true', '1'}
