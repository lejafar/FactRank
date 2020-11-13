import yaml
import argparse
import pathlib
from dataclasses import dataclass, replace
import logging
import os
import click
import shutil


@dataclass(eq=False, frozen=True)
class Options:

    """ hyperparameters """
    # learning settings
    batch_size: int = 512
    max_epochs: int = 1000
    # network configuration
    dropout: float = 0.6
    static: bool = True
    embed_dim: int = 320
    kernel_num: int = 100
    n_layers: int = 1
    # optimization
    weight_decay: float = 0.00001
    lr: float = 0.001
    lr_decay_step: float = 100
    lr_decay: float = 0.5

    """ transformer settings """
    pretrained_model_shortcut: str = "wietsedv/bert-base-dutch-cased"
    max_seq_length: int = 70
    adam_epsilon: float = 1e-8
    warmup_steps: int = 50

    """ data settings """
    gpu_id: int = 0
    run: str = "factnet"
    _run_path: str = None
    prefix: str = "factnet"
    statements_train_path: str = "data/training/statements_train_with_positive_feedback_21_03_2020.csv"
    statements_test_path: str = "data/training/statements_test.csv"
    min_freq: int = 1
    word_embeddings_path: str = "data/word_embeddings/cow-big-slim.txt"
    word_embeddings_noise: float = 1e-3
    split_ratio: float = 0.8
    stratified: bool = True
    log_metrics_step: int = 10
    log_level: str = 'INFO'

    LOG_BASE = 'log'

    @property
    def run_path(self):
        return self._run_path or self.get_run_path(self.run)

    @classmethod
    def get_run_path(cls, run):
        return pathlib.Path(cls.LOG_BASE) / run

    @classmethod
    def load(cls, options_path):
        with open(options_path, 'r') as f:
            options = cls(**yaml.load(f, Loader=yaml.FullLoader))
            options = replace(options, _run_path=options_path.parent)
            return options

    def dump(self, options_path):
        with open(options_path, 'w') as f:
            yaml.dump(self.__dict__, f, default_flow_style=False)

    @classmethod
    def parse(cls):
        # add all annotated attributes as parser arguments
        parser = argparse.ArgumentParser()
        parser.add_argument('--rerun', type=str)
        for name, field_type in cls.__annotations__.items():
            if field_type.__name__ in {'str', 'int', 'float', 'bool', 'tuple'}:
                parser.add_argument(f'--{name}', type=field_type)
        args, _ = parser.parse_known_args()

        if args.rerun:
            # this run already exist let's warn the user and reuse the options from that run
            logger.warning("Re-using the options from \033[1m%s\033[0m, " \
                    "other arguments will be ignored! 🔥", args.rerun)
            return cls.load(cls.get_run_path(args.rerun) / 'options.yml')

        # overwrite default options using all not None parser argument
        options = cls(**{k:v for k, v in args.__dict__.items() if v is not None})

        if options.run_path.exists():
            if click.confirm(f"Are you sure you want to overwrite run \033[1m{options.run}\033[0m?", default=True):
                shutil.rmtree(str(options.run_path), ignore_errors=True)
            else:
                exit(0)

        # store run options
        options.run_path.mkdir(parents=True, exist_ok=True)
        options.dump(options.run_path / f"{options.prefix}.options.yml")

        return options

