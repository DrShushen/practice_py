# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
from omegaconf import DictConfig

import hydra


@hydra.main(version_base=None, config_path="conf", config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(f"driver={cfg.db.driver}, timeout={cfg.db.timeout}")


if __name__ == "__main__":
    my_app()  # pylint: disable=no-value-for-parameter
