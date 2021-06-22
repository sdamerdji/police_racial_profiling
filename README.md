# Police Racial Profiling

## Motivation

Cities across California will be implementing new data collection to monitor racial profiling in police stops, in accordance with AB 953: The Racial and Identity Profiling Act of 2015.

Now that cities will start collecting this data, the question is how to make the best use of it. This repository compares several proxies for racial profiling against state-of-the-arts tests: the veil of darkness test and the threshold test. Our aim is to provide actionable insights for local electeds who care about racial equity.

## Setup

We rely on [`poetry`](https://python-poetry.org/) to maintain the virtualenv for this repository. 

To install poetry in linux or osx, execute:
```sh
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
source $HOME/.poetry/env
```

After installing poetry, run:
```sh
poetry install
poetry shell
poetry run jupyter lab
```
to spin up a Jupyter lab shell with all of the dependencies.
