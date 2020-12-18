print(__file__)
import logging
from rich.logging import RichHandler

from django_home_task import settings
from pathlib import Path
from rich import inspect

old_factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
    """Custom %(relpath)s field in format string.
    Paths of files in this project are displayed relatively, not absolutely.
    """
    record = old_factory(*args, **kwargs)
    try:
        record.relpath = Path(record.pathname).relative_to(settings.BASE_DIR)
    except ValueError:
        record.relpath = record.pathname
    return record


class Logger(logging.Logger):
    name = "main"
    
    def __init__(self, name: str, level=logging.NOTSET):
        super().__init__(name, level)
    
    def logattr(self, obj, name: str, default=None):
        inspect(getattr(obj, name, default), docs=False, title=f'{obj}.{name}')


def getlogger(name: str = "main") -> Logger:
    log = logging.getLogger(name)
    return log


def init():
    """Sets up main Logger config, and hooks any exceptions to use RichHandler"""
    logging.setLogRecordFactory(record_factory)
    logging.basicConfig(
            level="DEBUG",
            # format="%(message)s",
            # format='%(asctime)s[%(levelname)s]%(filename)s.%(funcName)s():%(lineno)d | %(message)s',
            # format='%(pathname)s.%(funcName)s():%(lineno)d | %(message)s',
            format='%(relpath)s.%(funcName)s():%(lineno)d | %(message)s',
            datefmt="[%X]",
            handlers=[RichHandler(rich_tracebacks=True,
                                  tracebacks_show_locals=True,
                                  locals_max_length=100,
                                  locals_max_string=160)]
            )
    logging.setLoggerClass(Logger)
    log = getlogger()
    log.debug('logger initiated')
