# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import logging
import sys

from omegaconf import DictConfig, OmegaConf

import hydra

log = logging.getLogger(__name__)


@hydra.main(version_base=None, config_path="conf", config_name="config")
def experiment(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))


if __name__ == "__main__":
    sys.exit(experiment())  # pylint: disable=no-value-for-parameter
