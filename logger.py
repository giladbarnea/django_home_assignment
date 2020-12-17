print(__file__)
import logging
from rich.logging import RichHandler

from django_home_task import settings
from pathlib import Path
from rich import inspect

old_factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
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
    logging.setLogRecordFactory(record_factory)
    logging.basicConfig(
            level="DEBUG",
            # format="%(message)s",
            # format='%(asctime)s[%(levelname)s]%(filename)s.%(funcName)s():%(lineno)d | %(message)s',
            # format='%(pathname)s.%(funcName)s():%(lineno)d | %(message)s',
            format='%(relpath)s.%(funcName)s():%(lineno)d | %(message)s',
            datefmt="[%X]",
            handlers=[RichHandler(rich_tracebacks=True,
                                  tracebacks_show_locals=True)]
            )
    logging.setLoggerClass(Logger)
    log = getlogger()
    log.debug('logger initiated and now exists globally across app')
