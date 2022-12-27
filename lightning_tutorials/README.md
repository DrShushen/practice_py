## Synopsis
Following [official documentation](https://pytorch-lightning.readthedocs.io/en/stable) as of 2022-12.

Using Python 3.8.

Using the following PyTorch & associated libraries:
```bash
conda install pytorch=1.13.1 torchvision=0.13.1 pytorch-cuda=11.7 -c pytorch -c nvidia
```

### Useful Lightning-adjacent resources/libraries

* `TorchMetrics`: https://torchmetrics.readthedocs.io/en/stable/pages/lightning.html
* `lightning-hydra-template`: https://github.com/ashleve/lightning-hydra-template
* `Lightning Bolts`: https://lightning-bolts.readthedocs.io/en/stable/index.html
    * A bunch of more specific Lightning components to go on top of Lightning, like model components, losses, datasets...
* `Lightning Flash`: https://lightning-flash.readthedocs.io/en/stable/quickstart.html
(and https://github.com/Lightning-AI/lightning-flash)
    * A whole bunch more pre-implemented ML tasks and tools for Lightning, like:
    image classification, text classification, ...
* ...
