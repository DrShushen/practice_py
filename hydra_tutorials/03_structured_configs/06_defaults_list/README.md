## Defaults List

Here: https://hydra.cc/docs/tutorials/structured_config/defaults/

You can define a defaults list in your primary Structured Config just like you can in your primary `config.yaml` file.

The example below extends the previous example by adding a defaults list that will load `db=mysql` by default.

> **NOTE:** You can still place your defaults list in your primary (YAML) config file (Example in next page).

```python
from dataclasses import dataclass

import hydra
from hydra.core.config_store import ConfigStore
from omegaconf import MISSING, OmegaConf

@dataclass
class MySQLConfig:
    ...

@dataclass
class PostGreSQLConfig:
    ...

# NOTE.
defaults = [
    # Load the config "mysql" from the config group "db"
    {"db": "mysql"}
]

@dataclass
class Config:
    # this is unfortunately verbose due to @dataclass limitations
    defaults: List[Any] = field(default_factory=lambda: defaults)  # NOTE.

    # Hydra will populate this field based on the defaults list
    db: Any = MISSING

cs = ConfigStore.instance()
cs.store(group="db", name="mysql", node=MySQLConfig)
cs.store(group="db", name="postgresql", node=PostGreSQLConfig)
cs.store(name="config", node=Config)


@hydra.main(version_base=None, config_name="config")
def my_app(cfg: Config) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()
```

Running `my_app.py` loads the mysql config option by default:
```sh
$ python my_app.py
db:
  driver: mysql
  ...
```

You can override the default option via the command line:
```sh
$ python my_app.py db=postgresql
db:
  driver: postgresql
  ...
```



### [❗] A Note about *composition order*

The default composition order in Hydra is that values defined in a config are merged into values introduced from configs in the Defaults List - or in other words - overriding them. 

This behavior *can be unintuitive* when your primary config is a Structured Config, like in the example above.

For example, if the primary config is:
```python
@dataclass
class Config:
    defaults: List[Any] = field(default_factory=lambda:  [
        "debug/activate",
        # NOTE!
        # If you do not specify _self_, it will be appended *to the end* of the defaults list by default.
        "_self_"
    ])

    debug: bool = False
```
And `debug/activate.yaml` is overriding the `debug` flag to `True`, the composition order would be such that `debug` ends up being `False`!

To get `debug/activate.yaml` to override this config, explicitly specify `_self_` **before** `debug/activate.yaml`:
```python
@dataclass
class Config:
    defaults: List[Any] = field(default_factory=lambda:  [
        "_self_",  # NOTE.
        "debug/activate",
    ])

    debug: bool = False
```

See [Composition Order](https://hydra.cc/docs/advanced/defaults_list/#composition-order) for more information.



### Requiring users to specify a default list value

Set `db` as `MISSING` to *require the user to specify* a value on the command line.

`Defaults list with a missing db:`
```python
defaults = [
    {"db": MISSING}  # NOTE.
]
```

`Output:`
```sh
$ python my_app.py
You must specify 'db', e.g, db=<OPTION>
Available options:
        mysql
        postgresql
```
