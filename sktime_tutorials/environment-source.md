## Building latest `sktime` from source

1. Set up the environment `py38_playaround-sk_sktime` from `environment.yml`
2. Clone it: `conda create --name py38_playaround-sk_sktime-source --clone py38_playaround-sk_sktime`
3. Activate it: `conda activate py38_playaround-sk_sktime-source`
4. Disable OpenMP for compilation (as otherwise the installation is tricky): `export SKTIME_NO_OPENMP=1`
5. Clean, just in case: `make clean`
6. Build: ` pip install .`

More info: https://www.sktime.org/en/latest/installation.html#unix-like-os
