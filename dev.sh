#!/usr/bin/env bash

export DJANGO_SETTINGS_MODULE=django_home_task.settings
bold="\x1b[1m"
ok="\x1b[32m"
warn="\x1b[33m"
grey="\x1b[2m"
c0="\x1b[0m"
# verbose execution
vex() {
  local description="\x1b[37;48;2;10;10;10m$*${c0}"
  echo "\nrunning $description...\n" >&2
  if eval "$@"; then
    echo "\n$description: ${ok}OK${c0}\n" >&2
    return 0
  else
    echo "\n$description: ${warn}FAIL${c0}\n" >&2
    return 1
  fi
}
function is_in_virenv() {
  local virenv_py_version
  local runtime_file_py_version
  local django_version

  # e.g. "3.8"
  virenv_py_version="$(python --version | cut -d ' ' -f 2 | cut -c -3)"
  runtime_file_py_version="$(cut -d '-' -f 2 ./runtime.txt | cut -c -3)"

  if [[ -z "$VIRTUAL_ENV" || "$virenv_py_version" != "$runtime_file_py_version" ]]; then
    echo "${warn}no virtual environment is currently active${c0}"
    if [[ -e ./env/bin/activate ]]; then
      if ! confirm "found file: './env/bin/activate'. activate?"; then
        return 1
      fi
      if source env/bin/activate; then
        echo "${ok}activated virtual environment"
        python --version
        echo -n "$c0"
      else
        echo "${warn}failed activating virtual environment${c0}"
        return 1
      fi
      # e.g. "3.1"
      django_version="$(python -m pip freeze | grep Django | cut -d '=' -f 3 | cut -c -3)"
      if [[ "$django_version" != 3.1 ]]; then
        echo "${warn}App requires django >= 3.1; Current Django version: $django_version${c0}"
        return 1
      else
        echo "${ok}django version >= 3.1 (good)${c0}"
        return 0
      fi
    else
      return 1
    fi
  else
    return 0
  fi
}
function input() {
  echo "${bold}$1${c0}"
  local answer
  read -r answer
  echo "$answer"
}
function confirm() {
  echo "${bold}$1 (y/n)${c0}"
  local answer
  read -r answer
  if [[ "$answer" == y ]]; then
    return 0
  else
    return 1
  fi
}
function pmp() {
  is_in_virenv || return 1
  python manage.py "$@"
  return $?
}

function killproc() {
  local all_killed=true
  local any_exist=false
  if [[ -n "$(pgrep -f "$1")" ]]; then
    any_exist=true
    echo "${bold}${warn}found proc(s) matching '$1'. killing...${c0}"
    for proc in $(pgrep -f "$1"); do
      kill -9 "$proc" || all_killed=false
    done
  fi
  if [[ "$all_killed" == true ]]; then
    if [[ "$any_exist" == true ]]; then
      echo "${ok}all '$1' processes killed${c0}"
    else
      echo "${ok}no processes existed in the first place for '$1'${c0}"
    fi
    return 0
  else
    echo "${warn}failed killing all '$1' processes${c0}"
    return 1
  fi
}

function deploy() {
  is_in_virenv || return 1
  if [[ -n "$(git status -s)" ]]; then
    git status -b
    if ! confirm "git add, commit and push?"; then
      return 1
    fi
    vex git add .
    echo -n "${bold}Commit message:${c0}\n>"
    local commitmsg
    read -r commitmsg
    vex git commit -m "'$commitmsg'" || return 1
    vex git push heroku main || return 1
  else
    echo "git status is empty; nothing to push"
  fi
  vex heroku run python manage.py makemigrations || return 1
  vex heroku run python manage.py migrate || return 1
}

function runlocal() {
  is_in_virenv || return 1

  local platform
  local should_collect_static=true
  local should_migrate=true
  local POSITIONAL=()
  while [[ "$#" -gt 0 ]]; do
    case "$1" in
    -h | --help)
      echo "$bold
runlocal <ENV> [OPTIONS]
$c0
Runs the app locally (either django or heroku), but first, takes care of:
- virtual environment and active python version
- pre-existing processes (if exist)
- runs makemigrations and migrate
- environment variables
$bold
Usage:
$c0
$ runlocal    ${grey}does migrations safely and verbosely${c0}
$ runlocal django [MANAGE.PY BUILT-IN OPTIONS] [--no-migrate] [--no-ipdb] [--no-pretty-trace] [--verbose]
$ runlocal heroku [HEROKU LOCAL BUILT-IN OPTIONS]
$bold
Example:
$c0
$ runlocal django --nothreading --nostatic --noreload --no-migrate
$bold
Environment Variables:
$c0
DJANGO_HOME_TASK_SECRET_KEY, DJANGO_HOME_TASK_DB_PASS and DJANGO_SETTINGS_MODULE are necessary for app to run
DJANGO_HOME_TASK_IPDB, DJANGO_HOME_TASK_PRETTY_TRACE, and DJANGO_HOME_TASK_VERBOSE are for debugging purposes,
and are toggled and exported by optional '--no-ipdb', '--no-pretty-trace' and '--verbose' args.
"
      return 0
      ;;
    heroku)
      killproc '.*heroku\-cli.*start' || return 1
      platform=heroku
      shift
      ;;
    django)
      killproc '.*manage\.py runserver' || return 1
      platform=django
      shift
      ;;
    --nostatic)
      should_collect_static=false
      POSITIONAL+=("$1")
      shift
      ;;
    --no-migrate)
      should_migrate=false
      shift
      ;;
    --no-ipdb)
      export DJANGO_HOME_TASK_IPDB=False
      POSITIONAL+=("$1")
      shift
      ;;
    --no-pretty-trace)
      export DJANGO_HOME_TASK_PRETTY_TRACE=False
      POSITIONAL+=("$1")
      shift
      ;;
    --verbose)
      export DJANGO_HOME_TASK_VERBOSE=True
      shift
      ;;
    *)
      POSITIONAL+=("$1")
      shift
      ;;

    esac
  done
  [[ "$DJANGO_HOME_TASK_IPDB" == False ]] || export DJANGO_HOME_TASK_IPDB=True
  [[ "$DJANGO_HOME_TASK_PRETTY_TRACE" == False ]] || export DJANGO_HOME_TASK_PRETTY_TRACE=True
  [[ "$DJANGO_HOME_TASK_VERBOSE" == True ]] || export DJANGO_HOME_TASK_VERBOSE=False
  if [[ "$should_migrate" == true ]]; then
    vex python manage.py makemigrations || return 1
    vex python manage.py migrate || return 1
  fi
  [[ $should_collect_static == true ]] && vex python manage.py collectstatic

  if [[ "$platform" == "heroku" ]]; then
    vex heroku local "${POSITIONAL[@]}"
    return $?
  elif [[ "$platform" == "django" ]]; then
    # See manage.py for extra custom cli args
    vex python manage.py runserver "${POSITIONAL[@]}"
    return $?
  fi
}
