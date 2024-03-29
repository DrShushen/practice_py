# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved
import os

from omegaconf import DictConfig

import hydra
from hydra.utils import get_original_cwd, to_absolute_path


@hydra.main(version_base=None)
def my_app(_cfg: DictConfig) -> None:
    print(f"Current working directory : {os.getcwd()}")
    print(f"Orig working directory    : {get_original_cwd()}")
    print(f"to_absolute_path('foo')   : {to_absolute_path('foo')}")
    print(f"to_absolute_path('/foo')  : {to_absolute_path('/foo')}")


if __name__ == "__main__":
    my_app()  # pylint: disable=no-value-for-parameter
