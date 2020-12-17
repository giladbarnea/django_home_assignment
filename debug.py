print(__file__)
import os
import sys

from rich import inspect
from rich.console import Console


def patch_breakpointhook():
    import logger
    log = logger.getlogger()
    log.debug('patching breakpointhook...')
    
    def set_trace():
        import builtins
        import rich
        whatis = lambda *args, **kwargs: inspect(*args, **kwargs, methods=True, help=True)
        from IPython import get_ipython
        ipy = get_ipython()
        nonlocal pi
        from rich.pretty import pprint
        pp = pprint
        con = Console()
        if sys.exc_info()[0]:  # If any exception occurred:
            con.print_exception(show_locals=True)
        mm = lambda topic: os.system(f'bash -c "/usr/bin/python3.8 -m mytool.myman {topic}"')
        builtins.mm = mm
        builtins.rich = rich
        builtins.whatis = whatis
        builtins.ipy = ipy
        builtins.pi = pi
        builtins.pp = pp
        builtins.con = con
        try:
            pi.ok('available debug tools:', f'rich, whatis, ipy, pi, pp, con, mm')
        except Exception as e:
            pp(dict(rich=rich, whatis=whatis, ipy=ipy, pi=pi, pp=pp, con=con, mm=mm))
        _set_trace()
    
    try:
        # In production, this raises ModuleNotFoundError, because
        # pyinspect and ipdb are not installed
        import pyinspect as pi
        from ipdb import set_trace as _set_trace
    
    except ModuleNotFoundError as mnfe:
        log.warning((f'\n\n{mnfe.__class__.__qualname__}:',
                     'failed patching sys.breakpointhook with ipdb (this is expected in production)',
                     mnfe.args, '\n\n'))
        
        from pdb import set_trace as _set_trace  # vanilla python pdb
    
    sys.breakpointhook = set_trace


def printattr(obj, attr: str, default=None):
    try:
        import pyinspect as pi
        pi.what(getattr(obj, attr, default), title=f'{obj}.{attr}')
    except ModuleNotFoundError:
        inspect(getattr(obj, attr, default), docs=False, title=f'{obj}.{attr}')
