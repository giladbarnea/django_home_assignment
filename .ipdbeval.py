"""This file is evalulated just before ipdb.set_trace() is called (ipdb fork)"""
print('in .ipdbeval.py')
import builtins
import sys
import rich
from rich import inspect
import os
from rich.pretty import pprint as ppr

import pyinspect as pi

from rich.console import Console

con = Console()
if sys.exc_info()[0]:
    print('.ipdbeval.py: building fancy trace...')
    con.print_exception(show_locals=True)


def mm(topic):
    os.system(f'bash -c "/usr/bin/python3.8 -m mytool.myman {topic}"')


def what(*args, **kwargs):
    inspect(*args, **kwargs, methods=True, help=True)


def what_(*args, **kwargs):
    inspect(*args, **kwargs, methods=True, help=True, private=True)


def what__(*args, **kwargs):
    inspect(*args, **kwargs, methods=True, help=True, private=True, dunder=True)


builtins.sys = sys
builtins.rich = rich
builtins.mm = mm
builtins.what = what
builtins.inspect = inspect
# builtins.ipy = ipy
builtins.pi = pi
builtins.ppr = ppr
builtins.con = con
pi.ok('available debug tools:', f'rich, inspect, what (inspect with methods), pi, ppr, con, mm')
