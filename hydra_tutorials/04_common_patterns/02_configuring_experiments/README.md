## Configuring Experiments

Here: https://hydra.cc/docs/patterns/configuring_experiments/



### Problem

A common problem is *maintaining multiple configurations of an application*.

This can get especially tedious when the *configuration differences span multiple dimensions*.

This pattern shows how to *cleanly support multiple configurations*, with each configuration file *only specifying the changes to the master (default) configuration*.



### Solution

Create a config file specifying the overrides to the default configuration, and then call it via the command line. e.g. `$ python my_app.py +experiment=fast_mode`.

To avoid clutter, we place the experiment config files in dedicated config group called `experiment`.


### Example

In this example, we will create configurations for each of the server and database pairings that we want to benchmark.

The default configuration is:

*Main config:*
`config.yaml:`
```yaml
defaults:
  - db: mysql
  - server: apache
```

*Databases:*
`db/mysql.yaml:`
```yaml
name: mysql
```

`db/sqlite.yaml:`
```yaml
name: sqlite
```

*Servers:*
`server/apache.yaml:`
```yaml
name: apache
port: 80
```

`server/nginx.yaml:`
```yaml
name: nginx
port: 80
```

*Directory structure:*
```
├── config.yaml
├── db
│   ├── mysql.yaml
│   └── sqlite.yaml
└── server
    ├── apache.yaml
    └── nginx.yaml
```

*Run app...*
```sh
$ python my_app.py
db:
  name: mysql
server:
  name: apache
  port: 80
```

**/!\ The benchmark config files (`experiment/`) specify the deltas from the default configuration:**

`experiment/aplite.yaml:`
```yaml
# @package _global_
defaults:
  - override /db: sqlite
  
  
server:
  port: 8080
```

*Run...*
```sh
$ python my_app.py +experiment=aplite
db:
  name: sqlite
server:
  name: apache
  port: 8080
```

`experiment/nglite.yaml:`
```yaml
# @package _global_
defaults:
  - override /db: sqlite
  - override /server: nginx
  
server:
  port: 8080
```

*Run...*
```sh
$ python my_app.py +experiment=nglite
db:
  name: sqlite
server:
  name: nginx
  port: 8080
```

⚠️ Key concepts:
* `# @package _global_`:
    * Changes specified in this config should be interpreted as relative to the `_global_` package.
    * We could instead place `nglite.yaml` and `aplite.yaml` next to `config.yaml` and omit this line.
* The `override`s of `/db` and `/server` are **absolute paths**.
    * This is necessary because they are outside of the experiment directory. 

> Running the experiments from the command line requires prefixing the experiment choice with a `+`. The experiment config group *is an addition, not an override*.



### Sweeping over experiments

This approach also enables sweeping *over those experiments* to easily compare their results:
```sh
$ python my_app.py --multirun +experiment=aplite,nglite
[HYDRA] Launching 2 jobs locally
[HYDRA]        #0 : +experiment=aplite
db:
  name: sqlite
server:
  name: apache
  port: 8080

[HYDRA]        #1 : +experiment=nglite
db:
  name: sqlite
server:
  name: nginx
  port: 8080
```

To run all the experiments, use the [glob](https://hydra.cc/docs/advanced/override_grammar/extended/#glob-choice-sweep) syntax:
```
$ python my_app.py --multirun '+experiment=glob(*)'
[HYDRA]        #0 : +experiment=aplite
...
[HYDRA]        #1 : +experiment=nglite
...
```
