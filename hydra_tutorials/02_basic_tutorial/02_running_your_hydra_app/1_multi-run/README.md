## Multi-run

Here: https://hydra.cc/docs/tutorials/basic/running_your_app/multi-run/

Sometimes you want to run the same application with multiple different configurations.
E.g. running a performance test on each of the databases with each of the schemas.

You can multirun a Hydra application via either commandline or configuration.

### Configure `hydra.mode` (*new in Hydra 1.2*)

You can configure `hydra.mode` in any supported way.

The legal values are `RUN` and `MULTIRUN`.

The following shows how to override from the command-line and *sweep* over all combinations of the `db`s and `schema`s.

(!) Setting `hydra.mode=MULTIRUN` in your input config would make your application multi-run by default.

```sh
$ python my_app.py hydra.mode=MULTIRUN db=mysql,postgresql schema=warehouse,support,school
[2021-01-20 17:25:03,317][HYDRA] Launching 6 jobs locally
[2021-01-20 17:25:03,318][HYDRA]        #0 : db=mysql schema=warehouse
[2021-01-20 17:25:03,458][HYDRA]        #1 : db=mysql schema=support
[2021-01-20 17:25:03,602][HYDRA]        #2 : db=mysql schema=school
[2021-01-20 17:25:03,755][HYDRA]        #3 : db=postgresql schema=warehouse
[2021-01-20 17:25:03,895][HYDRA]        #4 : db=postgresql schema=support
[2021-01-20 17:25:04,040][HYDRA]        #5 : db=postgresql schema=school
```
The printed configurations have been omitted for brevity.

### `--multirun (-m)` from the command-line

You can achieve the above from command-line as well:
```sh
python my_app.py --multirun db=mysql,postgresql schema=warehouse,support,school
```
or
```sh
python my_app.py -m db=mysql,postgresql schema=warehouse,support,school
```

You can access `hydra.mode` *at runtime* to determine whether the application is in `RUN` or `MULTIRUN` mode. Check [here](https://hydra.cc/docs/configure_hydra/intro/) on how to access Hydra config at run time.

(!) If conflicts arise (e.g., `hydra.mode=RUN` and the application was run with `--multirun`), Hydra will determine the value of `hydra.mode` at run time.

The following table shows what runtime hydra.mode value you'd get with different input configs and commandline combinations.

| | No multirun commandline flag | --multirun ( -m) |
| ---| --- | --- |
| hydra.mode=RUN | RunMode.RUN | RunMode.MULTIRUN (with UserWarning) |
| hydra.mode=MULTIRUN | RunMode.MULTIRUN | RunMode.MULTIRUN |
| hydra.mode=None (default) | RunMode.RUN | RunMode.MULTIRUN |

> ⚠️ Hydra composes configs lazily at job launching time. If you change code or configs after launching a job/sweep, the final composed configs might be impacted.

### Sweeping via `hydra.sweeper.params`

You can also define sweeping in the input configs by overriding `hydra.sweeper.params`. 

Using the above example, the same multirun could be achieved via the following config.

```yaml
hydra:
  sweeper:
    params:
      db: mysql,postgresql
      schema: warehouse,support,school
```

The syntax are consistent for both input configs and commandline overrides. 

If a sweep is specified *in both an input config and at the command line*, then the *commandline sweep will take precedence* over the sweep defined in the input config.

If we run the same application with the above input config and a new commandline override:
```
$ python my_app.py -m db=mysql
[2021-01-20 17:25:03,317][HYDRA] Launching 3 jobs locally
[2021-01-20 17:25:03,318][HYDRA]        #0 : db=mysql schema=warehouse
[2021-01-20 17:25:03,458][HYDRA]        #1 : db=mysql schema=support
[2021-01-20 17:25:03,602][HYDRA]        #2 : db=mysql schema=school
```

**NOTE**

The content of actual files in the example is slightly different.

See [./conf/config.yaml](./conf/config.yaml):
```yaml
defaults:
  - db: ???
  - _self_

hydra:
  sweeper:
    params:
      db: glob(*)
      db.timeout: 5,10
```

Run sweep with:
```sh
python my_app.py -m
```

> ℹ️ The above configuration methods only apply to Hydra's default `BasicSweeper` for now. For other sweepers, please check out the corresponding documentations.

### Additional sweep types

Hydra supports other kinds of sweeps, e.g.:

```sh
x=range(1,10)                  # 1-9
schema=glob(*)                 # warehouse,support,school
schema=glob(*,exclude=w*)      # support,school
```

### Sweeper
The default sweeping logic is built into Hydra. Additional sweepers are available as plugins. For example, the [Ax Sweeper](https://hydra.cc/docs/plugins/ax_sweeper/) can automatically find the best parameter combination!

### Launcher
By default, Hydra runs your multi-run jobs locally and serially.

Other **launchers** are available as plugins for launching in parallel and on different clusters.

For example, the [JobLib Launcher](https://hydra.cc/docs/plugins/joblib_launcher/) can execute the different parameter combinations in parallel on your local machine using multi-processing.

