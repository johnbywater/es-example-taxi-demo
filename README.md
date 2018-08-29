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


## copying and license

This material is copyright (c) 2018 John Bywater and contributors.

It is licensed under the GNU Affero General Public License (AGPL) v3.0
whose full text may be found in the LICENSE file, and at:

http://www.fsf.org/licensing/licenses/agpl-3.0.html
