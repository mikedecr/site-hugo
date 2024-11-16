eval "$($HOME/.local/bin/micromamba shell hook --shell=zsh)"
micromamba env create -f conda/hugosite.yml -p build/conda_envs/hugosite

