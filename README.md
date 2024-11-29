# Hugo site

Personal website, [`quarto`](https://quarto.org/) compiled to Markdown, site generated with [Hugo](https://gohugo.io/).

Build status at [mikedecr.netlify.app](https://mikedecr.netlify.app/): [![Netlify Status](https://api.netlify.com/api/v1/badges/fbc483b6-8147-45ad-9e78-f11e6e5d1e53/deploy-status)](https://app.netlify.com/sites/mikedecr/deploys)


## Setup

Requires: 

- [`uv`](https://docs.astral.sh/uv/pip/packages/)
- for historical reasons, [micromamba](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html)

```sh
git clone git@github.com:mikedecr/site-hugo.git mikedecr-site
cd mikedecr-site
git submodule update --init --recursuve
uv sync
uv run mkd build
```
