#!/usr/bin/env bash
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
alias mm='/usr/bin/python3.8 -m mytool.myman'
alias gig='/usr/bin/python3.8 -m igit.exec.ignore'
alias tree='tree -Ia "*env|__pycache__|.git|.idea|.vscode|staticfiles|.ipynb_checkpoints|__pycache__"'
alias pmp='python manage.py'
function _is_in_virenv() {
  local virenv_py_version
  local runtime_file_py_version

  # e.g. "3.8"
  virenv_py_version="$(python --version | cut -d ' ' -f 2 | cut -c -3)"
  runtime_file_py_version="$(cut -d '-' -f 2 ./runtime.txt | cut -c -3)"
  if [[ -z "$VIRTUAL_ENV" || "$virenv_py_version" != "$runtime_file_py_version" ]]; then
    echo "FATAL: no virtual environment is currently active"
    return 1
  fi
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
# runlocal <django|heroku>
function runlocal() {
  _is_in_virenv || return 1
  if [[ -z "$1" ]]; then
    echo "FATAL: runlocal expects 1 param: 'django' or 'heroku'"
    return 1
  fi
  local platform="$1"
  if [[ "$platform" == "heroku" ]]; then
    if [[ -n "$(pgrep -f '.*heroku-cli.*start')" ]]; then
      kill -9 "$(pgrep -f '.*heroku-cli.*start')" 2>/dev/null
    fi
  elif [[ "$platform" == "django" ]]; then
    if [[ -n "$(pgrep -f '.*env.*manage\.py runserver')" ]]; then
      kill -9 "$(pgrep -f '.*env.*manage\.py runserver')" 2>/dev/null
    fi
  fi
  if [[ -n "$(pgrep -f '.*django_home_task')" ]]; then
    kill -9 "$(pgrep -f '.*django_home_task')" 2>/dev/null
  fi

  vex python manage.py migrate || return 1
  python manage.py collectstatic
  if [[ "$platform" == "heroku" ]]; then
    vex heroku local
    return $?
  elif [[ "$platform" == "django" ]]; then
    vex python manage.py runserver
    return $?
  fi
}
#[ -s ./scripts/dev.sh ] && cat ./scripts/dev.sh | python3 -c 'x if x.startswith("alias") else None'
[ -s ./scripts/dev.sh ] && cat ./scripts/dev.sh | python3 -c 'import sys; [print(x, end="") if x.startswith("alias") else None for x in sys.stdin.readlines()]'
