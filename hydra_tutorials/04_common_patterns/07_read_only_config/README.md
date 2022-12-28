## Read-only config

Here: https://hydra.cc/docs/patterns/write_protect_config_node/



### Problem

Sometimes you want to prevent a config node from being changed accidentally.



### Solution

Structured Configs can enable it by passing `frozen=True` in the dataclass definition. Using Structured Configs, you can annotate a dataclass as frozen.

This is *recursive and applies to all child nodes*.

This will prevent modifications via code, command line overrides and config composition.

`frozen.py:`
```python
@dataclass(frozen=True)  # NOTE.
class SerialPort:
    baud_rate: int = 19200
    data_bits: int = 8
    stop_bits: int = 1


cs = ConfigStore.instance()
cs.store(name="config", node=SerialPort)


@hydra.main(version_base=None, config_name="config")
def my_app(cfg: SerialPort) -> None:
    print(cfg)


if __name__ == "__main__":
    my_app()
```

Output:
```sh
$ python frozen.py data_bits=10
Error merging override data_bits=10
Cannot change read-only config container
    full_key: data_bits
    object_type=SerialPort
```

> NOTE: A crafty user can find many ways around this. This is just making it harder to change things accidentally.