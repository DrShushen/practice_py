## Structured Config schema

Here: https://hydra.cc/docs/tutorials/structured_config/schema/

We have seen how to use *Structured Configs* as **configuration**, but they can also be used as a **schema** (i.e. *validating configuration files*).

To achieve this, we will follow the common pattern of [Extending Configs](https://hydra.cc/docs/patterns/extending_configs/) - but instead of extending another config file, *we will extend a Structured Config*.



### Validating against a schema in the **same** config group

⚠️ This is all quite ugly and convoluted...

Given the config directory structure:
```
conf/
├── config.yaml
└── db
    ├── mysql.yaml
    └── postgresql.yaml
```

We will add Structured Config schema for each of the config files above and store in the Config Store as `base_config`, `db/base_mysql` and `db/base_postgresql`.

Then, we will use the Defaults List in each config to specify its base config as follows:

`config.yaml:`
```yaml
defaults:
  - base_config  # NOTE!
  - db: mysql
  # See composition order note
  - _self_

debug: true
```

`db/mysql.yaml:`
```yaml
defaults:
  - base_mysql  # NOTE!

user: omry
password: secret
```

`db/postgresql.yaml:`
```yaml
defaults:
  - base_postgresql  # NOTE!

user: postgres_user
password: drowssap
```

One difference in the source code is that we have **removed the Defaults List from the Config dataclass**. The primary Defaults List will come from `config.yaml`.

```python
from dataclasses import dataclass

import hydra
from hydra.core.config_store import ConfigStore

@dataclass
class DBConfig:
    driver: str = MISSING
    host: str = "localhost"
    port: int = MISSING

@dataclass
class MySQLConfig(DBConfig):
    driver: str = "mysql"
    port: int = 3306
    user: str = MISSING
    password: str = MISSING

@dataclass
class PostGreSQLConfig(DBConfig):
    driver: str = "postgresql"
    user: str = MISSING
    port: int = 5432
    password: str = MISSING
    timeout: int = 10

@dataclass
class Config:
    db: DBConfig = MISSING
    debug: bool = False

# NOTE: No defaults list!

cs = ConfigStore.instance()
cs.store(name="base_config", node=Config)
cs.store(group="db", name="base_mysql", node=MySQLConfig)  # NOTE.
cs.store(group="db", name="base_postgresql", node=PostGreSQLConfig)  # NOTE.

@hydra.main(version_base=None, config_path="conf", config_name="config")
def my_app(cfg: Config) -> None:
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()
```

When Hydra composes the final config object it will use the config schemas as specified in the Default Lists.

Like before, Hydra will catch user errors in the command line:
```sh
$ python my_app.py db.port=fail
Error merging override db.port=fail
Value 'fail' could not be converted to Integer
        full_key: db.port
        object_type=MySQLConfig
```

> ℹ️ Use `--info` commands to see how a config was composed
```sh
$ python my_app.py --info defaults-tree

Defaults Tree
*************
<root>:
  hydra/config:
    hydra/output: default
    hydra/launcher: basic
    hydra/sweeper: basic
    hydra/help: default
    hydra/hydra_help: default
    hydra/hydra_logging: default
    hydra/job_logging: default
    _self_
  config:
    base_config
    db: mysql:
      db/base_mysql
      _self_
    _self_

$ python my_app.py --info defaults

Defaults List
*************
| Config path                 | Package             | _self_ | Parent       | 
------------------------------------------------------------------------------
| hydra/output/default        | hydra               | False  | hydra/config |
| hydra/launcher/basic        | hydra.launcher      | False  | hydra/config |
| hydra/sweeper/basic         | hydra.sweeper       | False  | hydra/config |
| hydra/help/default          | hydra.help          | False  | hydra/config |
| hydra/hydra_help/default    | hydra.hydra_help    | False  | hydra/config |
| hydra/hydra_logging/default | hydra.hydra_logging | False  | hydra/config |
| hydra/job_logging/default   | hydra.job_logging   | False  | hydra/config |
| hydra/config                | hydra               | True   | <root>       |
| base_config                 |                     | False  | config       |
| db/base_mysql               | db                  | False  | db/mysql     |
| db/mysql                    | db                  | True   | config       |
| config                      |                     | True   | <root>       |
------------------------------------------------------------------------------
```


### Validating against a schema from a **different** config group

In the above example, the schema we used was stored in the same config group. This is not always the case, for example - A library might provide schemas in its own config group.

Here is a modified version of the example above, where a mock `database_lib` is providing the schemas we want to validate against.

`my_app.py`
```python
from dataclasses import dataclass

import hydra
from hydra.core.config_store import ConfigStore

import database_lib  # NOTE.


@dataclass
class Config:
    db: database_lib.DBConfig = MISSING  # NOTE.
    debug: bool = False

cs = ConfigStore.instance()
cs.store(name="base_config", node=Config)  # NOTE.

# database_lib registers its configs
# in database_lib/db
database_lib.register_configs()  # NOTE.


@hydra.main(
    version_base=None,
    config_path="conf",
    config_name="config",
)
def my_app(cfg: Config) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()
```

`database_lib.py:`
```python
from dataclasses import dataclass

from hydra.core.config_store import ConfigStore

@dataclass
class DBConfig:
  ...

@dataclass
class MySQLConfig(DBConfig):
  ...

@dataclass
class PostGreSQLConfig(DBConfig):
  ...


def register_configs() -> None:  # NOTE.
    cs = ConfigStore.instance()
    cs.store(
        group="database_lib/db",
        name="mysql",
        node=MySQLConfig,
    )
    cs.store(
        group="database_lib/db",
        name="postgresql",
        node=PostGreSQLConfig,
    )
```

The *Defaults List* entry for the base config is **slightly different**:
`db/mysql.yaml:`
```yaml
defaults:
  - /database_lib/db/mysql@_here_  # NOTE!

user: omry
password: secret
```

`db/postgresql.yaml:`
```yaml
defaults:
  - /database_lib/db/postgresql@_here_  # NOTE!
  # See composition order note  
  - _self_

user: postgres_user
password: drowssap
```

* We refer to the config **with an absolute path** because it is outside the subtree of the `db` config group.
* We override the package to `_here_` to ensure that the package of the schema is the same as the package of the config it's validating. **\[❓ I don't get this.\]**
> To understand `_here` see the [Extending Configs (pattern) tutorial](https://hydra.cc/docs/patterns/extending_configs/).


### A Note about composition order
By default, Hydra 1.1 appends `_self_` to the end of the Defaults List.

This behavior is new in Hydra 1.1 and different from previous Hydra versions.

As such Hydra 1.1 issues a warning if `_self_` is not specified in the **primary config**, asking you to add `_self_` and thus indicate the desired composition order.

To address the warning while maintaining the new behavior, append `_self_` to the end of the Defaults List.

Note that in some cases it may instead be desirable to add `_self_` *directly after the schema and before other Defaults List elements*.

See [Composition Order](https://hydra.cc/docs/advanced/defaults_list/#composition-order) for more information.
