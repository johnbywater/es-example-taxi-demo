# Taxi-Demo


## install pipenv on osx

```bash
brew install pipenv
```

Other platforms - 
https://pipenv.readthedocs.io/en/latest/



## install deps

In the project root:
```bash
pipenv install

```


## run tests

In the project root:

```bash
behave tests/bdd
```

The pipenv includes dependencies to run the tests from pycharm. 

In the UI, set the python interpreter to the one created
by pipenv, highlight taxi.feature, and Run.

