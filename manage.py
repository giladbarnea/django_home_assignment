#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
print(__file__)
import os
import sys

# #### Parse custom command line args (mostly debug purposes) ####
# # This needs to run before main() so execute_from_command_line() doesn't raise an 'Unknown command'
# for arg in sys.argv:
#     if arg == '--no-pretty-trace':
#         os.environ.setdefault('DJANGO_HOME_TASK_PRETTY_TRACE', 'False')
#         sys.argv.remove(arg)
#     if arg == '--no-ipdb':
#         # Controls whether sys.breakpointhook is set to ipdb.set_trace or left as-is (in django_home_task/urls.py)
#         os.environ.setdefault('DJANGO_HOME_TASK_IPDB', 'False')
#         sys.argv.remove(arg)
# print('sys.argv: ', *sys.argv)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_home_task.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
                ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
