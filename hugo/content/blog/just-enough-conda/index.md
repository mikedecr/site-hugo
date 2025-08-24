---
title: Just enough Conda advice
subtitle: Easy enough for beginners, good enough for seasoned users
summary: >-
  The best way to make things "just work" is for to design your workflow so that
  common mistakes are simply impossible.
author: Michael DeCrescenzo
date: 2025-04-05T00:00:00.000Z
---


Virtual environments seem to be a constant pain for researchers.
Academics in particular seem to not really understand them, which causes a lot of startup pain when they want try out the Python language.
The academics I used to roll with are heavy users of R, which has some environment management tools (`renv` in particular), but they are not heavily used.[^1]
Even in the industry world I see Python users complaining about environment pains.
Stuff like, "broke my conda environment again...".

This post will be a rapid-fire list of env-management practices that should ease a lot of these pains.

I will focus mostly on the `conda`, but you may have hard of `pip`, `uv`, `mamba` / `micromamba`, or `pixi`.[^2]
The principles discussed here generally apply to any major Python package manager.

This post may evolve as I evolve my thoughts about what good practices are.
But I have been using conda in a professional environment for 5 years now, and I think the information here is both:

-   good enough that experienced users can endorse it.
-   efficient enough that total newcomers can adopt 100% of these tips and feel like none of the effort was wasted.

If you are familiar with conda environments already, feel free to skip around and get what you want out of this.
If you are totally new, reading in order will help you get onboarded.

## Managing the environment is easy when you are consistent about it

In his Statistical Rethinking lectures, Richard McElreath says that statistical machinery helps us solve problems [not because we are clever, but because we are rigorous](https://www.youtube.com/watch?v=lTFAB6QmwHM&) in the application of statistical fundamentals.

Analogously, environments help you solve problems when they are applied rigorously.

Many people first learn about environments and want to minimize their interactions with the environment.
They want things to "just work", but they think they can achieve this by hiding the environment.
They want the environment to be an invisible background consideration, an inconvenience whose existence should be minimized.

Sorry, but I think this is all wrong!
The environment is saving you from a ton of pain, and you should embrace it.
The best way to make things "just work" is for to design your workflow so that common mistakes are simply impossible.

This means you must learn.

## What is an environment?

An environment is like a "scope" that defines which computational resources are available and how programs can find those resources, without interfering with the global setup of the machine where it lives.

Your computer contains many software tools on it, and those tools "live" in certain places in the computer.
When you run a piece of software, and it needs to reach out to some other thing you have installed on your computer (like a math library), how does the software know where to find that other program?
And are these programs compatible with each other?

Environments are one way to manage which dependencies are available to your program.

It is helpful to see this working in the terminal with an example.

This current blog post is written in Quarto, and I use the Quarto CLI to render the post.
If I open a terminal and ask if the `quarto` tool exists, the terminal shows me where it is finding that tool.

``` sh
which quarto
# /usr/local/bin/quarto

quarto --version
# 1.6.40
```

This is saying that I have a `quarto` version 1.6.40 executable in the `/usr/local/bin` directory.

That's nice.

But when I build this blog post, I don't use this instance of `quarto`.
Instead, I have a virtual environment for this post, managed by `pixi`.

Let's learn about the version of `quarto` that I use to build this blog post:

``` sh
pixi run which quarto
# /Users/md/projects/site-hugo/submodules/blog-monorepo/just-enough-conda/.pixi/envs/default/bin/quarto

pixi run quarto --version
# 1.7.33
```

(Every time I say `pixi run xyz` I am running the command `xyz` in the pixi environment.)

This environment contains its own installation of `quarto` that I pin to a specific version.
So if I ever change the global installation of `quarto` on my computer, I won't break the version of `quarto` that I use to build this blog post.

This is what the environment is all about.
A project knows its own dependencies, and the environment isolates those dependencies from the rest of the computer.

## Why use environments

Environments let you control many separate projects on your computer that have different computational requirements.

-   Different projects need different versions of R or Python, or whatever other software.
-   One project needs some package, but another project doesn't need it at all.
-   You want to prevent software upgrades from breaking your code, so you want to specify *which* version of a package you need for a project.
-   You want to test your project on another computer, and you need a way to quickly install the required dependencies on that other computer.
-   You move your project to a different location on *your own* machine, and you need to make sure all of the dependencies are in the right place.

Environments save you from all of this, if you use them intentionally.

## Start in the terminal

Environments can be invoked by various GUI applications like VSCode or RStudio, but there is no substitute for learning the fundamentals in the shell.
The shell is where envrionments are laid bare, and if it doesn't make sense in the shell, it is unlikely to make sense in the GUI.

This doesn't mean you only have to use terminal-based applications like Vim to do your work.
Instead, I recommend launching GUI applications *from the correct environment* in order to inherit your environment's behaviors.

Re-using the `quarto` example above.
If I open VSCode from the terminal (with the terminal command `code`) using my `pixi` environment...

``` sh
# opens VScode in pixi env
pixi run code .
```

...the terminal *inside of VScode* will have inherited the environment configuations.

``` sh
which quarto
# /Users/md/projects/site-hugo/submodules/blog-monorepo/just-enough-conda/.pixi/envs/default/bin/quarto
```

So it is possible to both (a) get comfortable managing environments in the terminal, and (b) use the same GUI apps to edit your code as before.

## Projects should never share environments

Many people start using environments by building a single conda environment that they can activate from anywhere.
This is a recipe for disaster, because different projects want competing dependencies.

This is one reason why you see "broke my conda environment again..." tweets.
They may have been using the same environment for too many things.

You should have (at least) one environment per project.
Some projects require multiple environments.

But you should never mix multiple projects into one environment.

## Build environments into a local path

When you create a conda environment, keep it inside the project directory.
You can do this with

``` sh
conda create -p path/to/env <list packages here>
```

or if your environment is defined in a `yml` file (more on that later):

``` sh
conda env create -f path/to/file.yml -p path/to/env
```

In both examples, the `-p path/to/env` argument says the installed dependences (binaries, packages, etc) for that environment will live at that path.

By keeping the environment inside your project directory, you never lose track of which environment goes with which project.
And you can install multiple environments into separate paths under the same project directory.

## You can run commands in the environment without "activating" the environment

With all package managers listed so far, you can run commands in an environment without "activating" the environment.
For example, opening Python:

-   `uv run python`
-   `pixi run python`
-   `conda run -p path/to/env python`
-   `micromamba run -p path/to/env python`

This is in contrast to "activating" the environment, which means to initialize your terminal shell with paths and environment variables that the environment defines.

-   `conda activate -p path/to/env`
-   `micromamba activate -p path/to/env`
-   `pixi shell`
-   I don't think `uv` has a command for this ([yet?](https://github.com/astral-sh/uv/issues/1910))

This is most useful in scenarios where you have multiple environments in play.
For example, you need to compile some program in environment A and then run the program in environment B.

I encounter this with my website build process.

-   I have an environment that builds my website.
-   My website also contains many blog posts with their own computing dependencies.
-   *The website env does not / should not care* what is in each blog post env, and vice versa, so it makes sense for these envs to be separate!
-   I render each blog post its own environment, and then build the website with the website environment.

Managing multiple environments sounds tedious, but this is what computers are for.
As long as you are rigorous in the configuation of your project, nothing ever goes wrong because every step of your workflow is associated with the correct dependencies.

## Never use a global `.condarc` file

In conda, your [`~/.condarc`](https://docs.conda.io/projects/conda/en/latest/user-guide/configuration/use-condarc.html) defines some "common" behavior for all conda/mamba operations on your machine.
For example, you can list "default" channels to install packages from, or other default configurations.

Do not use this file.
It controls *your machine only*.
If someone else wants to use your software but doesn't have your exact global `.condarc` configs, your project may not actually be reproducible.
Keep your environment configurations local to the project source code so that other people who use your project can reproduce your environment.

## Build your conda environment from a `.yml`. Never install things as you go

Another major footgun is to install things into your environment on an ad-hoc basis, for example `conda install pandas`.
Package managers are nice because they can find a version of a package that can be installed into your present environment.
But things go wrong.
Sometimes they install a package into your environment while uninstalling or changing the versions of other dependencies, so it can break your code.

Instead: define a `yml` file that lists the channels and packages to install, and build the environment from that file.
Non-conda package managers use `requirements.txt` or `pyproject.toml` or `pixi.toml` instead of conda's `yml` format, but the idea is the same.
Use these files pin the package versions you need, which gives your environment can be built and re-built in the exact same way.

Here is an [example from a blog post that sets up an R computing envrionment](https://github.com/mikedecr/post_nonflat-priors/blob/1b070b664257fef4cbbc3c9786ed7ccb00357f77/conda/nonflat.yml).

## Pin your dependencies

If you have read this far, it should not be a huge surprise that you should pin your dependencies to the versions that you expect to consume in your project.
If you know that you need some minimum version of a package to pick up a new feature, specify that in your environment recipe.

This can be done to pin the maximum version of a package as well, in case new versions broke a feature that you needed to work.

If you see someone complaining that they updated a package and now their code doesn't work, they didn't do this part right.

## Other quick tips:

This stuff is more optional, but can improve your UX.

-   [**Direnv**](https://direnv.net/). In the simple case where you want to activate an environment when you are in a project directory, you can use Direnv.
    Your `.envrc` can contain a command like `conda activate -p path/to/env`, so you automatically activate the environment when you `cd` into the project directory.
-   **R environments**.
    You can manage R projects with Conda/Mamba/Micromamba just fine.
    You can ask for packages prefixed with `r-` from the `r` conda channel.
    Example from my own blog posts [here](https://github.com/mikedecr/post_memo_scum/blob/c9af2771a61ef483d7335c3f41a5a309cf832e6b/conda/env.yml).
    I think this is way easier and more predictable than `renv`, which has never worked the way I want it to.
-   **Makefiles and friends**: If you have other setup scripts that need to run that cannot be entirely managed by your environment / package manager, systematizing how those commands should be run is also very helpful.
    Makefiles are one way to do it.
    I prefer [Just](https://github.com/casey/just), which I find far easier to write.
    You can install `just` with conda or pip.
-   **UV, Pixi, etc**.
    People realy like [uv](https://docs.astral.sh/uv/), a Python package manager written in Rust.
    I love `uv` when it can support my projects, but because `uv` focuses on the Python Package Index, it isn't a good choice for projects that need e.g. C/C++ dependencies, or R projects.
    So that's why we talked about Conda and friends here.
    If you like the speed and feel of `uv`, but you need a more cross-language package index, [`Pixi`](https://pixi.sh/latest/) has been fun to use.

[^1]: Most R users survive on a combination of CRAN's blessings and hope, which is another way of saying, complete avoidance of env tooling and workflow.

[^2]: Mentally I divide these tools into two groups: Python-only or multi-language.
    I could `pip` and `uv` as Python-only because they work with the Python Package Index (PyPI).
    But `conda` has its own system of channels for distributing packages across several languages.
    `micromamba` is basically `conda` but smaller and faster.
    The `pixi` user experience is a lot like `uv` but for conda-like environments.
    Usually I prefer the `conda` family of tools because I often have to specify dependencies across languages.
    You can manage R environments with Conda (and I do).
