## Configuring Plugins

Here: https://hydra.cc/docs/patterns/configuring_plugins/

*Hydra plugins* usually come with sensible defaults which work with minimal configuration. There are two primary ways to customize the configuration of a plugin:
* Overriding it directly in your primary config.
* Extending the config and using it from your primary config.

The first method is the simpler, but it makes it harder to switch to a different plugin configuration. The second method is a bit more complicated, but makes it easier to switch between different plugin configurations.

The following methods apply to all Hydra plugins.

In the following examples, we will configure an imaginary Launcher plugin `MoonLauncher`. The Launcher has two modes: `falcon9`, which actually launches the application to the Moon and `sim` which simulates a launch.

The config *schema* for MoonLauncher looks like:
```python
@dataclass
class Falcon9Conf:
  ton_fuel:  int = 10
```

```python
@dataclass
class Simulation:
  ton_fuel:  int = 10
  window_size:
    width: 1024
    height: 768
```



### Overriding in primary config

We can directly override Launcher config in primary config.

`config.yaml`
```yaml
a: 1

hydra:
  launcher:
    ton_fuel: 2
```

* command-line override: `hydra/launcher=falcon9`. Resulting launcher config:
```
hydra:
  launcher:
    ton_fuel: 2
```

* command-line override: `hydra/launcher=sim`. Resulting launcher config:
```
hydra:
  launcher:
    ton_fuel: 2
    window_size:
      width: 1024
      height: 768
```

This approach makes the assumption that the Launcher used has all the fields we are overriding. If we wanted to override a field that exists in the Simulation Launcher but not in the Falcon9 Launcher, like `window_size.width`, we would no longer be able to use the Falcon9 Launcher!

The next section solves this problem.



### Extending plugin default config

Extending plugin default config has several advantages:
* Separate configuration concerns, keep primary config clean.
* Easier to switch between different plugin configurations.
* Provides flexibility when a Plugin has different modes that requires different schema.

**❓ This example makes no sense to me. Did they mean `launcher` instead of `sweeper` in the second `yaml`?..**

Say that we want to override certain values for different Launcher mode:

`hydra/launcher/my_falcon9.yaml`
```yaml
defaults:
  - falcon9

ton_fuel: 2
```

`hydra/sweeper/my_sim.yaml`
```yaml
defaults:
  - sim

window_size:
  width: 768
```

We can easily user command-line overrides to get the configuration needed:

* command-line override: `hydra/launcher=my_falcon9`. Resulting launcher config:
```
hydra:
  launcher:
    ton_fuel: 2
```

* command-line override: `hydra/launcher=my_sim`. Resulting launcher config:
```
hydra:
  launcher:
    ton_fuel: 2
    window_size:
      width: 1024
      height: 768
```
