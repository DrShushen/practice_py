## Quick start guide

### Introduction

Hydra is an open-source Python framework that simplifies the development of research and other complex applications.

The key feature is the ability to dynamically create a hierarchical configuration by composition and override it through config files and the command line.

The name Hydra comes from its ability to run multiple similar jobs - much like a Hydra with multiple heads.

Key features:
* Hierarchical configuration composable from multiple sources
* Configuration can be specified or overridden from the command line
* Dynamic command line tab completion
* Run your application locally or launch it to run remotely
* Run multiple jobs with different arguments with a single command

### NOTE

This guide will show you some of the most important features you get by writing your application as a Hydra app.

If you only want to use Hydra for *config composition*, check out Hydra's [compose API](https://hydra.cc/docs/advanced/compose_api/) for an alternative.

Please also read the full [tutorial](https://hydra.cc/docs/tutorials/basic/your_first_app/simple_cli/) to gain a deeper understanding.

### Basic example

[./basic_example/](./basic_example/)

> You can learn more about OmegaConf [here](https://omegaconf.readthedocs.io/en/latest/usage.html#access-and-manipulation) later.

`config.yaml` is loaded automatically when you run your application:
```sh
$ python my_app.py
db:
  driver: mysql
  pass: secret
  user: omry
```

You can override values in the loaded config from the command line:
```
$ python my_app.py db.user=root db.pass=1234
db:
  driver: mysql
  user: root
  pass: 1234
```

### Composition example

[./composition_example/](./composition_example/)

You may want to alternate between two different databases.

To support this create a `config group` named `db`, and place one config file for each alternative inside.

The directory structure of our application now looks like:
```text
├── conf
│   ├── config.yaml
│   ├── db
│   │   ├── mysql.yaml
│   │   └── postgresql.yaml
│   └── __init__.py
└── my_app.py
```

`defaults` is a special directive telling Hydra to use `db/mysql.yaml` when composing the configuration object.

The resulting `cfg` object is a **composition of configs from defaults** with configs specified in your `config.yaml`.

```sh
$ python my_app.py db=postgresql db.timeout=20
db:
  driver: postgresql
  pass: drowssap
  timeout: 20
  user: postgres_user
```

### Multirun

Continued with [./composition_example/](./composition_example/).

You can run your function multiple times with different configuration easily with the `--multirun|-m` flag.

```
$ python my_app.py --multirun db=mysql,postgresql
[HYDRA] Sweep output dir : multirun/2020-01-09/01-16-29
[HYDRA] Launching 2 jobs locally
[HYDRA]        #0 : db=mysql
db:
  driver: mysql
  pass: secret
  user: omry

[HYDRA]        #1 : db=postgresql
db:
  driver: postgresql
  pass: drowssap
  timeout: 10
  user: postgres_user
```