# imfpy

A client for interacting with the [IMF's JSON RESTful API](https://datahelp.imf.org/knowledgebase/articles/667681-using-json-restful-web-service) with Python!! In particular, a tool for understanding, retrieving and exploring Direction of Trade Statistics (DoTS) data. 

This API client is intended to be useful for economic policymakers, researchers, government officials and more. Moving forward, I will add more functionality to each module, so that users may retrieve and analyse data from other IMF databases.

## Installation

```python
!pip install imfpy
```

Depends on:

- python 3.7 and above
- pandas 1.1.3 and above
- requests 2.19.0 and above
- matplotlib 3.2.2. and above

## Usage

The package contains three modules:  

* [`searches`](https://imfpy.readthedocs.io/en/latest/autoapi/imfpy/searches/index.html)
* [`retrievals`](https://imfpy.readthedocs.io/en/latest/autoapi/imfpy/retrievals/index.html)
* [`tools`](https://imfpy.readthedocs.io/en/latest/autoapi/imfpy/tools/index.html)

`searches` contains many helper functions that assist the user in searching through available IMF databases, dimensions, metadata and variables. 

`retrievals` contains functions that retrieve data from important databases. 

For example, `retrievals.dots` pulls data from the DoTS database including imports, exports, two-way trade and trade balances for IMF countries and country-groups. The function handles flexible queries and formats the returned data to the user's specifications. 

```python
#Example: retrieve Greece annual trade data
>>> from imfpy.retrievals import dots
>>> dots("GR", ["US", "AU", "DE"], 2000, 2005)
```

`tools` contains functions that conduct rudimentary analysis and visualization on the data returned by `retrievals` functions. For example, the `dotsplot` function transforms the result of `dots()` into time series plots.

```python
#Example: plot Australia trade data
>>> from imfpy.tools import dotsplot
>>> d = dots('AU',['US','CN'], 2000, 2020, freq='A', form="long")
>>> dotsplot(d, subset=['Trade Balance', 'Twoway Trade'])
```



## Links

**Documentation**

* [User Guide/Vignette](https://imfpy.readthedocs.io/en/latest/example.html#user-guide)

* [Full documentation](https://imfpy.readthedocs.io/en/latest/)

* [API Reference](https://imfpy.readthedocs.io/en/latest/autoapi/index.html)

**Distribution**

* [Github Repo](https://github.com/ltk2118/imfpy)

* PyPI package

**Tests**

* [Pytests](https://github.com/ltk2118/imfpy/blob/main/tests/test_imfpy.py)

**Extras**

* [IMF DoTS](https://data.imf.org/?sk=9D6028D4-F14A-464C-A2F2-59B2CD424B85)
* [My website](https://ltk2118.github.io/home/)

## Contributing

Interested in contributing? Want to use this package?  Please get in touch! Check out the contributing guidelines. 

Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`imfpy` was created by Liam Tay Kearney. It is licensed under the terms of the MIT license.

## Credits

`imfpy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
