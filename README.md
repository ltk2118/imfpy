# imfpy

A client for interacting with the [IMF's JSON RESTful API](https://datahelp.imf.org/knowledgebase/articles/667681-using-json-restful-web-service) with Python!! In particular, a tool for understanding, retrieving and exploring Direction of Trade Statistics (DoTS) data. 

This API client is intended to be useful for economic policymakers, researchers, government officials and more. Moving forward, I will add more functionality to each module, so that users may retrieve and analyse data from other IMF databases.

## Installation

```bash
$ pip install imfpy
```

## Usage

The package contains three modules:  `searches`, `retrievals`, `tools`.

`searches` contains many helper functions that assist the user in searching through available IMF databases, dimensions, metadata and variables. 

`retrievals` contains functions that retrieve data from important databases. For now, `retrievals` contains only `retrievals.dots()`, a function that pulls data from the DoTS database including imports, exports, two-way trade and trade balances for IMF countries and country-groups. The function handles flexible queries and formats the returned data to the user's specifications. 

```python
>>> from imfpy.retrievals import dots
>>> dots("GR", ["US", "AU", "DE"], 2000, 2005)
```

![usage3](https://github.com/ltk2118/imfpy/blob/main/img/usage3.png)

`tools` contains functions that conduct rudimentary analysis and visualization on the data returned by `retrievals` functions. For example, the `dotsplot` function transforms the result of `dots()` into time series plots.

```python
>>> from imfpy.tools import dotsplot
>>> d = dots('AU',['US','CN'], 2000, 2020, freq='A', form="long")
>>> dotsplot(d, subset=['Trade Balance', 'Twoway Trade'])
```

<img src="C:\Users\liamt\Documents\GitHub\imfpy\img\usage.png" alt="usage" style="zoom:50%;" />

<img src="C:\Users\liamt\Documents\GitHub\imfpy\img\usage2.png" alt="usage2" style="zoom:50%;" />

## Links

Full documentation

Vignettes

PyPI package

Github Repo

Tests

## Contributing

Interested in contributing?  Please get in touch! Check out the contributing guidelines. 

Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`imfpy` was created by Liam Tay Kearney. It is licensed under the terms of the MIT license.

## Credits

`imfpy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
