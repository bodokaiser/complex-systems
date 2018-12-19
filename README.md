# Complex Systems

Interactive visualizations of (complex) system dynamics using [Dash][1].

![Screenshot](https://user-images.githubusercontent.com/1780466/49365618-90adfd00-f6e7-11e8-9592-34400a9ecfcd.png)

## Usage

Clone the repository:

```shell
git clone https://github.com/bodokaiser/complex-systems
```

Change into the directory of the repository:

```shell
cd complex-systems
```

Use [pipenv][2] to install the dependencies and setup a clean virtualenv:
```shell
pipenv install --dev -e .
```
The `--dev -e` flags install the `dynamics` directory as a package such that
we can easily import it from the `dashboards` and `notebooks` subdirectories.

### Dashboards

Run the dashboard web application:
```shell
pipenv run python dashboards/roessler.py
```

### Notebooks

In order to run notebooks we need to install [jupyter][3] and register the
environment as kernel. This can be done via:
```shell
pipenv run python -m ipykernel install --user --name=complex-systems
```

Then start a [jupyter][3] notebook server in the notebooks directory:
```shell
cd notebooks
pipenv run jupyter notebook
```

[1]: https://plot.ly/products/dash
[2]: https://docs.pipenv.org/
[3]: https://jupyter.org
