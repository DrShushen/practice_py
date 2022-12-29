## OmegaConf

Following this: https://omegaconf.readthedocs.io/

Using the same environment as the Hydra tutorials one directory level up.


### Summary

OmegaConf is a **YAML** based **hierarchical** configuration system, with support for:
* merging configurations from multiple sources (files, CLI argument, environment variables)
* providing a consistent API regardless of how the configuration was created.

OmegaConf also offers **runtime type safety** via **Structured Configs**.



### Covered

* Usage: [01_usage.ipynb](./01_usage.ipynb)
* Resolvers - skipped, see: https://omegaconf.readthedocs.io/en/latest/custom_resolvers.html
    * Useful things there include env var resolver etc.
* Structured Configs: [03_structured_configs.ipynb](./03_structured_configs.ipynb)
* The OmegaConf grammar - skipped, see for reference: https://omegaconf.readthedocs.io/en/latest/grammar.html
    * Basically an overview of the grammar of *Resolvers*, e.g. `${some_deep_dict[key1][subkey2].subsubkey3}` etc.
* How-To Guides - skipped, not very useful.
