# django_home_assignment

## Run

```bash
source dev.sh     # loads two functions: runlocal, deploy
runlocal --help   # prints instructions
```

## Use

```bash
source dev.sh
runlocal --nostatic
# in a different shell, run each for examples:
python dev/read.py --help
python dev/write.py --help
python dev/delete.py --help
```