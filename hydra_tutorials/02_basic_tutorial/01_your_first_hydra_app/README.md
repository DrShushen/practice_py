## A simple command-line application

Here: https://hydra.cc/docs/tutorials/basic/your_first_app/simple_cli/

```python
from omegaconf import DictConfig, OmegaConf
import hydra

@hydra.main(version_base=None)
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()
```

* In this example, Hydra creates an empty cfg object and passes it to the function annotated with `@hydra.main`.

* You can add config values via the command line. The `+` indicates that the field is new.
```sh
$ python my_app.py +db.driver=mysql +db.user=omry +db.password=secret
db:
  driver: mysql
  user: omry
  password: secret
```

ℹ️ See the [`version_base` page](https://hydra.cc/docs/upgrades/version_base/) for details on the `version_base` parameter.

ℹ️ See:
* [Hydra's command line flags](https://hydra.cc/docs/advanced/hydra-command-line-flags/) and
* [Basic Override Syntax](https://hydra.cc/docs/advanced/override_grammar/basic/)

for more information about the command line.



## Specifying a config file

It can get tedious to type all those command line arguments. You can solve it by creating a configuration file next to `my_app.py`.

Hydra configuration files are yaml files and should have the `.yaml` file extension.

```yaml
db: 
  driver: mysql
  user: omry
  password: secret
```

Specify the config name by passing a `config_name` parameter to the `@hydra.main()` decorator.
* Note that you should omit the `.yaml` extension.
* Hydra also needs to know *where* to find your config. Specify the *directory* containing it **relative to the application** by passing *config_path*.

```python
from omegaconf import DictConfig, OmegaConf
import hydra

@hydra.main(version_base=None, config_path=".", config_name="config")
def my_app(cfg):
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()
```

`config.yaml` is loaded automatically when you run your application.

```sh
$ python my_app.py
db:
  driver: mysql
  user: omry
  password: secret
```

You can override values in the loaded config from the command line.
Note **the lack of the `+` prefix**.

```sh
$ python my_app.py db.user=root db.password=1234
db:
  driver: mysql
  user: root
  password: 1234
```

[❗] Use `++` to *override a config value if it's already in the config, or add it otherwise*. e.g:
```sh
# Override an existing item
$ python my_app.py ++db.password=1234

# Add a new item
# NOTE: Will NOT modify the config.yaml itself - will only affect the config for this particular run!
$ python my_app.py ++db.timeout=5
```

You can enable [tab completion](https://hydra.cc/docs/tutorials/basic/running_your_app/tab_completion/)
for your Hydra applications.

## Using the config object

Here are some basic features of the **Hydra Configuration Object**:
```yaml
node:                         # Config is hierarchical
  loompa: 10                  # Simple value
  zippity: ${node.loompa}     # Value interpolation
  do: "oompa ${node.loompa}"  # String interpolation
  waldo: ???                  # Missing value, must be populated prior to access
```

Outputs:
```sh
$ python my_app.py 
Traceback (most recent call last):
  File "my_app.py", line 32, in my_app
    cfg.node.waldo
omegaconf.errors.MissingMandatoryValue: Missing mandatory value: node.waldo
    full_key: node.waldo
    object_type=dict
```

> ℹ️ Hydra's configuration object is an instance of **OmegaConf's `DictConfig`**. You can learn more about OmegaConf [here](https://omegaconf.readthedocs.io/en/latest/usage.html#access-and-manipulation).



## Grouping config files

Suppose you want to benchmark your application on each of PostgreSQL and MySQL. To do this, use *config groups*.

A **Config Group** is a *named group* with a *set of valid options*. Selecting a non-existent config option generates an error message with the valid options.

### Creating config groups

To create a config group, create a directory, e.g. db, to hold a file for each database configuration option. Since we are expecting to have multiple config groups, we will proactively move all the configuration files into a conf directory.

```
├─ conf
│  └─ db
│      ├─ mysql.yaml
│      └─ postgresql.yaml
└── my_app.py
```

### Using config groups

Since we moved all the configs into the `conf` directory, we need to tell Hydra where to find them using the `config_path` parameter. `config_path` is a directory *relative to `my_app.py`*.

```python
from omegaconf import DictConfig, OmegaConf
import hydra

@hydra.main(version_base=None, config_path="conf")  # NOTE.
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()
```

Running `my_app.py` without requesting a configuration will print an empty config.
```sh
$ python my_app.py
{}
```

Select an item from a config group **with `+GROUP=OPTION`**, e.g:
```sh
$ python my_app.py +db=postgresql
db:
  driver: postgresql
  pass: drowssap
  timeout: 10
  user: postgres_user
```

By default, the config group determines where the config content is placed inside the final config object.

In Hydra, the path to the config content is referred to as the *config `package`*. The package of `db/postgresql.yaml` is `db`.

Like before, you can still override individual values in the resulting config:
```sh
$ python my_app.py +db=postgresql db.timeout=20
db:
  driver: postgresql
  pass: drowssap
  timeout: 20
  user: postgres_user
```

### Advanced topics
* Config content can be relocated via package overrides. See [Reference Manual/Packages](https://hydra.cc/docs/advanced/overriding_packages/).
* Multiple options can be selected from the same Config Group by specifying them as a list. See [Common Patterns/Selecting multiple configs from a Config Group](https://hydra.cc/docs/patterns/select_multiple_configs_from_config_group/).



## Selecting default configs

After office politics, you decide that you want to use MySQL by default. You no longer want to type `+db=mysql` every time you run your application.

You can add a **Default List** to your config file. A Defaults List is a list telling Hydra how to compose the final config object.

> By convention, it is the first item in the config.

### Config group defaults

```yaml
defaults:
  - db: mysql
```

Remember to specify the `config_name`:
```python
from omegaconf import DictConfig, OmegaConf
import hydra

@hydra.main(version_base=None, config_path="conf", config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))

if __name__ == "__main__":
    my_app()
```

When you run the updated application, MySQL is loaded by default.
```sh
$ python my_app.py
db:
  driver: mysql
  pass: secret
  user: omry
```

You can have *multiple items in the defaults list*, e.g.
```yaml
defaults:
 - db: mysql
 - db/mysql/engine: innodb
```

The defaults are ordered:
* If multiple configs define the same value, the last one wins.
* If multiple configs contribute to the same dictionary, the result is the combined dictionary.

**Overriding a config group default**

You can still load PostgreSQL, and override individual values.

```sh
$ python my_app.py db=postgresql db.timeout=20
db:
  driver: postgresql
  pass: drowssap
  timeout: 20
  user: postgres_user
```

ℹ️ You can **remove a default entry from the defaults list by prefixing it with `~`**:
```sh
$ python my_app.py ~db
{}
```

### ⚠️ *Composition order* of primary config

Your primary config can contain **both config values and a Defaults List**. In such cases,
> you should add the `_self_` keyword to your defaults list

to **specify the composition order of the config file relative to the items in the defaults list**.

1. If you want your **primary config** to override the values of configs from the Defaults List, append `_self_` to **the end** of the Defaults List.
2. If you want the **configs from the Defaults List** to override the values in your primary config, insert `_self_` **as the first item** in your Defaults List.

Exemplified:

1. Case 1 above.

`config.yaml`
```yaml
defaults:
  - db: mysql
  - _self_  # NOTE.

db:  # NOTE. db ALSO here!
  user: root
```

`Result config: db.user from config.yaml`
```yaml
db:
  driver: mysql  # db/mysql.yaml
  pass: secret   # db/mysql.yaml 
  user: root     # config.yaml
```

2. Case 2 above.

`config.yaml`
```yaml
defaults:
  - _self_  # NOTE.
  - db: mysql

db:
  user: root
```

`Result config: db.user from config.yaml`
```yaml
db:
  driver: mysql # db/mysql.yaml
  pass: secret  # db/mysql.yaml
  user: omry    # db/mysql.yaml
```

See [Composition Order](https://hydra.cc/docs/advanced/defaults_list/#composition-order) for more information.

> NOTE: The default composition order changed between Hydra 1.0 and Hydra 1.1. See [info box](https://hydra.cc/docs/tutorials/basic/your_first_app/defaults/).

### Non-config group defaults

Sometimes a config file *does not belong in any config group*. You can still load it by default. Here is an example for `some_file.yaml`.

```yaml
defaults:
  - some_file
```

⚠️ Config files that are not part of a config group will always be loaded. They cannot be overridden. **Prefer using a config group.**

## Putting it all together

[./putting_all_together/](./putting_all_together/)

As software gets more complex, we resort to modularity and composition to keep it manageable. We can do the same with configs. Suppose we want our working example to support multiple databases, with multiple schemas per database, and different UIs. We wouldn't write a separate class for each permutation of db, schema and UI, so we shouldn't write separate configs either. We use the same solution in configuration as in writing the underlying software: **composition**.

To do this in Hydra, we first add a `schema` and a `ui` config group:
```
├── conf
│   ├── config.yaml
│   ├── db
│   │   ├── mysql.yaml
│   │   └── postgresql.yaml
│   ├── schema
│   │   ├── school.yaml
│   │   ├── support.yaml
│   │   └── warehouse.yaml
│   └── ui
│       ├── full.yaml
│       └── view.yaml
└── my_app.py
```

With these configs, we already have 12 possible combinations. Without composition, we would need 12 separate configs. A single change, such as renaming `db.user` to `db.username`, requires editing all 12 of them. This is a maintenance nightmare.

Composition can come to the rescue. Instead of creating 12 different config files, that fully specify each config, create a single config that specifies the different configuration dimensions, and the default for each.
```yaml
defaults:
  - db: mysql
  - ui: full
  - schema: school
```

The resulting configuration is a composition of the *mysql* database, the *full* ui, and the *school* schema (which we are seeing for the first time here):
```sh
$ python my_app.py
db:
  driver: mysql
  user: omry
  pass: secret
ui:
  windows:
    create_db: true
    view: true
schema:
  database: school
  tables:
  - name: students
    fields:
    - name: string
    - class: int
  - name: exams
    fields:
    - profession: string
    - time: data
    - class: int
```

Stay tuned to see how to run all of the combinations automatically ([Multi-run](https://hydra.cc/docs/tutorials/basic/running_your_app/multi-run/)).

**Summary**

* The addition of each new db, schema, or ui only requires a single file.
* Each config group can have a default specified in the Defaults List.
* Any combination can be composed by selecting the desired option from each config group in the Defaults List or the command line.
