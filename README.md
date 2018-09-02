# Taxi-Demo


## Install pipenv on osx

```bash
brew install pipenv
```

Other platforms - 
https://pipenv.readthedocs.io/en/latest/



## Install dependencies

In the project root:
```bash
pipenv install
```


## To run BDD tests of the model 

In the project root:

```bash
behave tests/bdd
```

The pipenv also includes dependencies to run the model tests from pycharm. 
To make use of this, in the UI, set the python interpreter to the one created
by pipenv, highlight taxi.feature, and Run.



## To run the prototype-api tests under pytest

```bash
pytest
```


## To exercise the prototype-api using curl


### start the REST server in a terminal...

```bash
python api.py
```

### run the tests in another terminal

```bash
./shell_test_api.bash
```




## copying and license

This material is copyright (c) 2018 John Bywater and contributors. It
is licensed under the GNU Affero General Public License (AGPL) v3.0
whose full text may be found in the LICENSE file, and at: 
http://www.fsf.org/licensing/licenses/agpl-3.0.html
