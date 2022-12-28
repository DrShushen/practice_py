## Extending Configs

Here: https://hydra.cc/docs/patterns/extending_configs/

A common pattern is to extend an existing config, overriding and/or adding new config values to it. The extension is done by including the base configuration, and then overriding the chosen values in the current config.

**Extending a config from the same config group:**

`config.yaml:`
```yaml
defaults:
  - db: mysql 
```

This one **extends**:

`db/mysql_extending_from_this_group.yaml:`
```yaml
defaults:
  - base_mysql

user: omry
password: secret
port: 3307
encoding: utf8
```

This one **is base**:

`db/base_mysql.yaml:`
```yaml
host: localhost
port: 3306
user: ???
password: ???
```

Output:
```sh
$ python my_app.py
db:
  host: localhost   # from db/base_mysql
  port: 3307        # overridden by db/mysql_extending_from_this_group.yaml 
  user: omry        # populated by db/mysql_extending_from_this_group.yaml
  password: secret  # populated by db/mysql_extending_from_this_group.yaml
  encoding: utf8    # added by db/mysql_extending_from_this_group.yaml
```

**Extending a config *from another config group*:**

To extend a config from a different config group:
* include it using an absolute path (`/`),
* and override the package to `_here_`.

> `_here_` is described in [Packages](https://hydra.cc/docs/advanced/overriding_packages/#default-list-package-keywords).

Like so:

`db/mysql.yaml:`
```yaml
defaults:
  - /db_schema/base_mysql@_here_  # NOTE!!!
```

It is otherwise identical to extending a config within the same config group.
