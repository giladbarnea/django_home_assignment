print(__file__)
import logging

from django_home_task import settings
from pathlib import Path

import os
from logging import getLogger

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


class Logger(logging.RootLogger):
    name = "root"
    
    def __init__(self, name: str = "root", level=logging.DEBUG):
        super().__init__(level)
        self._verbose = eval(os.environ.get('DJANGO_HOME_TASK_VERBOSE', 'False'))
        self.debug(f'VERBOSE = {self._verbose}')
    
    def verbose(self, msg, *args, **kwargs):
        if self._verbose:
            super().debug(msg, *args, **kwargs)


def getlogger(name: str = "root") -> Logger:
    log = Logger()
    # print(type(log), log.__class__, log.name)
    assert hasattr(log, 'verbose')
    return log


def init():
    """Sets up root Logger config, and hooks any exceptions to use RichHandler"""
    logging.setLogRecordFactory(record_factory)
    log_config_args = dict(level="DEBUG",
                           format='%(relpath)s.%(funcName)s():%(lineno)d | %(message)s',
                           datefmt="[%X]", )
    import os
    PRETTY_TRACE = eval(os.environ.get('DJANGO_HOME_TASK_PRETTY_TRACE', 'True'))
    if PRETTY_TRACE:
        from rich.logging import RichHandler
        logging.basicConfig(**log_config_args,
                            handlers=[RichHandler(rich_tracebacks=True,
                                                  tracebacks_show_locals=True,
                                                  locals_max_length=100,
                                                  locals_max_string=160)]
                            )
    else:
        logging.basicConfig(**log_config_args)
    # logging.setLoggerClass(Logger)
    
    log = logging.getLogger()
    log.debug(f'logger initiated with {PRETTY_TRACE = }')
