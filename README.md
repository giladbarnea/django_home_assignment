# django_home_assignment

## Install

```bash
$ python3.8 -m virtualenv env
$ source env/bin/activate # or `env\Scripts\activate.cmd` on Windows
$ (env) pip install -r requirements.txt
```

## Use read / write / delete url endpoints

```bash
# activate virtual env and run each command to get examples:
$ (env) python dev/read.py --help
$ (env) python dev/write.py --help
$ (env) python dev/delete.py --help
```

## Run locally
#### Unix
```bash
$ source dev.sh     # loads two functions: runlocal, deploy
$ runlocal --help   # prints instructions about how runlocal does version, environment and process checks before running 'manage.py runserver'
```
#### Windows
Make sure python version is 3.8 and django is 3.1 (not 3.0).
A virtual env based on `requirements.txt` is failsafe.
See [Note on environment variables](#Note-on-environment-variables) 

## Deploy

```bash
$ source dev.sh
$ deploy
```

## Note on environment variables

If you're on Windows, `dev.sh` isn't very useful to you; it's a wrapper to manage.py that helps with the app's environment variables and cmd line args.

`DJANGO_HOME_TASK_SECRET_KEY`, `DJANGO_HOME_TASK_DB_PASS` and `DJANGO_SETTINGS_MODULE` are necessary for app
to run.

`DJANGO_HOME_TASK_IPDB`, `DJANGO_HOME_TASK_PRETTY_TRACE`, and `DJANGO_HOME_TASK_VERBOSE` are optional and are for debugging purposes.

`DJANGO_HOME_TASK_IPDB` and `DJANGO_HOME_TASK_VERBOSE` are `False` by default. `DJANGO_HOME_TASK_PRETTY_TRACE` is `True` by default.

Windows users can set env vars via e.g. `setx DJANGO_HOME_TASK_PRETTY_TRACE False`.