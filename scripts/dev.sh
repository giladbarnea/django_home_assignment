#!/usr/bin/env bash

export DJANGO_SETTINGS_MODULE=django_home_task.settings

vex() {
  local description="\x1b[37;48;2;10;10;10m$*\x1b[0m"
  echo "\nrunning $description...\n" >&2
  if eval "$@"; then
    echo "\n$description: \x1b[32mOK\x1b[0m\n" >&2
    return 0
  else
    echo "\n$description: \x1b[33mFAIL\x1b[0m\n" >&2
    return 1
  fi
}
function _is_in_virenv() {
  local virenv_py_version
  local runtime_file_py_version

  # e.g. "3.8"
  virenv_py_version="$(python --version | cut -d ' ' -f 2 | cut -c -3)"
  runtime_file_py_version="$(cut -d '-' -f 2 ./runtime.txt | cut -c -3)"
  if [[ -z "$VIRTUAL_ENV" || "$virenv_py_version" != "$runtime_file_py_version" ]]; then
    echo "ERROR: no virtual environment is currently active"
    if [[ -e ./env/bin/activate ]]; then
      local should_activate
      echo "found file: './env/bin/activate'. activate? y/n"
      read -r should_activate
      if [[ "$should_activate" == y ]]; then
        source ./env/bin/activate
        return $?
      else
        return 1
      fi
    fi

    return 1
  fi
}
function pmp(){
  _is_in_virenv || return 1
  python manage.py "$@"
  return $?
}


function deploy() {
  _is_in_virenv || return 1
  if [[ -n "$(git status -s)" ]]; then
    vex git add .
    local commitmsg
    echo -n "Commit message:\n>"
    read -r commitmsg
    git commit -m "$commitmsg" && vex git push heroku main
  else
    echo "git status is empty; nothing to push"
  fi
  vex heroku run python manage.py migrate
}
function killproc() {
  local all_killed=true
  local any_exist=false
  if [[ -n "$(pgrep -f "$1")" ]]; then
    any_exist=true
    echo "\x1b[1;33mfound proc(s) matching '$1'. killing...\x1b[0m"
    for proc in $(pgrep -f "$1"); do
      kill -9 "$proc" || all_killed=false
    done
  fi
  if [[ "$all_killed" == true ]]; then
    if [[ "$any_exist" == true ]]; then
      echo "\x1b[32mall '$1' processes killed\x1b[0m"
    else
      echo "\x1b[32mno processes existed in the first place for '$1'\x1b[0m"
    fi
    return 0
  else
    echo "\x1b[33mfailed killing all '$1' processes\x1b[0m"
    return 1
  fi
}
# runlocal <django|heroku>
function runlocal() {
  _is_in_virenv || return 1
  if [[ -z "$1" ]]; then
    echo "FATAL: runlocal expects 1 param: 'django' or 'heroku'"
    return 1
  fi
  local platform="$1"
  if [[ "$platform" == "heroku" ]]; then
    killproc '.*heroku\-cli.*start' || return 1
  elif [[ "$platform" == "django" ]]; then
    killproc '.*manage\.py runserver' || return 1
  fi

  local should_collect_static=true
  local should_migrate=true
  for i in {1..10}; do
    if [[ "${*[$i]}" == "--nostatic" ]]; then
      should_collect_static=false
    fi
    if [[ "${*[$i]}" == "--no-migrate" ]]; then
      should_migrate=false
    fi
  done
  if [[ "$should_migrate" == true ]]; then
    vex python manage.py makemigrations || return 1
    vex python manage.py migrate || return 1
  fi
  [[ $should_collect_static == true ]] && vex python manage.py collectstatic

  if [[ "$platform" == "heroku" ]]; then
    vex heroku local "${@:2}"
    return $?
  elif [[ "$platform" == "django" ]]; then
    # See manage.py for extra custom cli args
    vex python manage.py runserver "${@:2}"
    return $?
  fi
}
[[ -s ./scripts/dev.sh ]] && cat ./scripts/dev.sh | python3 -c 'import sys; [print(x, end="") if x.startswith("alias") else None for x in sys.stdin.readlines()]'
