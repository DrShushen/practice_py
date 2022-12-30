## `pandera` tutorials

* GitHub: https://github.com/unionai-oss/pandera
* Docs: https://pandera.readthedocs.io/en/stable/index.html



### Note multiple additional functionality items:
```sh
pip install pandera[hypotheses]  # hypothesis checks
pip install pandera[io]          # yaml/script schema io utilities
pip install pandera[strategies]  # data synthesis strategies
pip install pandera[mypy]        # enable static type-linting of pandas
pip install pandera[fastapi]     # fastapi integration
pip install pandera[dask]        # validate dask dataframes
pip install pandera[pyspark]     # validate pyspark dataframes
pip install pandera[modin]       # validate modin dataframes
pip install pandera[modin-ray]   # validate modin dataframes with ray
pip install pandera[modin-dask]  # validate modin dataframes with dask
pip install pandera[geopandas]   # validate geopandas geodataframes
```

In particular `[mypy]` and maybe `[io]` seem useful.



### Tutorials run info
* Using Python 3.8.
* As of 2022-12.
* Used extensions: `io`, `mypy`, `strategies`.
