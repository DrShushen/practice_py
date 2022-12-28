## Introduction to Structured Configs

Here: https://hydra.cc/docs/tutorials/structured_config/intro/

> This is an advanced tutorial that assumes that you are comfortable with the concepts introduced in the [Basic Tutorial](https://hydra.cc/docs/tutorials/basic/your_first_app/simple_cli/
> 
> The examples in this tutorial are available [here](https://github.com/facebookresearch/hydra/blob/main/examples/tutorials/structured_configs).

*Structured Configs* use Python [**dataclasses**](https://docs.python.org/3.7/library/dataclasses.html) to describe your configuration structure and types.

They enable:
* **Runtime type checking** as you compose or mutate your config
* **Static type checking** when using static type checkers (`mypy`, PyCharm, etc.)

#### Structured Configs supports:
* Primitive types (`int`, `bool`, `float`, `str`, `Enum`a, `byte`s, `pathlib.Path`)
* *Nesting* of Structured Configs
* Containers (`List` and `Dict`) containing primitives, Structured Configs, or other lists/dicts
* Optional fields

#### ⚠️ Structured Configs Limitations:
* `Union` types are only partially supported (see [OmegaConf docs on unions](https://omegaconf.readthedocs.io/en/latest/structured_config.html#union-types))
* *User methods* are **not** supported

> See the [OmegaConf docs on Structured Configs](https://omegaconf.readthedocs.io/en/latest/structured_config.html) for more details.

#### There are two primary patterns for using Structured configs with Hydra
1. As a [config](https://hydra.cc/docs/tutorials/structured_config/minimal_example/), **in place of configuration files** (often a starting place)
1. As a [config schema](https://hydra.cc/docs/tutorials/structured_config/schema/) **validating configuration files** (ℹ️ better for complex use cases)

With both patterns, you still get everything Hydra has to offer (config composition, Command line overrides etc).

This tutorial covers both. *Read it in order*.

Hydra supports **OmegaConf's Structured Configs** via the `ConfigStore` API. This tutorial does not assume any knowledge of them.

> It is recommended that you visit the [OmegaConf Structured Configs](https://omegaconf.readthedocs.io/en/latest/structured_config.html) page to learn more later.
