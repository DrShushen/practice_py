from omegaconf import DictConfig, OmegaConf
import hydra

# @hydra.main(version_base=None, config_path=".", config_name="config")
# def my_app(cfg: DictConfig) -> None:
#     print(OmegaConf.to_yaml(cfg))


# For tutorial: "Using the config object"
# @hydra.main(version_base=None, config_path=".", config_name="config")
# def my_app(cfg: DictConfig) -> None:
#     print(OmegaConf.to_yaml(cfg))

#     assert cfg.node.loompa == 10  # attribute style access
#     assert cfg["node"]["loompa"] == 10  # dictionary style access

#     assert cfg.node.zippity == 10  # Value interpolation
#     assert isinstance(cfg.node.zippity, int)  # Value interpolation type
#     assert cfg.node.do == "oompa 10"  # string interpolation

#     try:
#         cfg.node.waldo  # raises an exception
#     except Exception as e:  # pylint: disable=broad-except
#         print("Exception for cfg.node.waldo:")
#         print(e)


# For tutorial: "Grouping config files"
# @hydra.main(version_base=None, config_path="conf")
# def my_app(cfg: DictConfig) -> None:
#     print(OmegaConf.to_yaml(cfg))


# For tutorial: "Selecting default configs"
@hydra.main(version_base=None, config_path="conf", config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    my_app()  # pylint: disable=no-value-for-parameter
