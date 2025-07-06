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
The academics I used to roll with are heavy users of R, which has some environment management solutions (`renv` in particular), but they are not heavily used.
Even in the industry world I see Python users complaining about environment pains.
Stuff like, "broke my conda environment again...".

This post will be a rapid-fire list of env-management practices that should ease a lot of these pains.
I will focus on `conda` primarily because it is more versatile than `pip` and `uv`, which are focused primarily on installing Python packages from the [Python Package Index](https://pypi.org/).
(For example, you can manage R environments with Conda. More detail on that below.)
I use [micromamba](https://mamba.readthedocs.io/en/latest/user_guide/micromamba.html), which behaves basically like conda but is smaller and faster.
Many of the principles will still apply to the use of these other tools.

This post may evolve as I evolve my thoughts about what good practices are.
But I have been using conda in a professional environment for 5 years now, and I think the information below is both:

-   good enough for experienced users
-   efficient enough for total newcomers to adopt 100% of the advice here and feel like none of the effort is wasted

If you are familiar with conda environments already you can skip around and get what you want out of this.
If you are totally new, reading in order will help you get onboarded.

## Managing the environment is easy when you are consistent about it

In his Statistical Rethinking lectures, Richard McElreath says that statistical machinery helps us solve problems [not because we are clever, but because we are rigorous](https://www.youtube.com/watch?v=lTFAB6QmwHM&) in the application of statistical fundamentals.

Similarly, environments help you solve problems when they are applied rigorously.

Many people first learn about environments and want to minimize their interactions with the environment.
They want things to "just work", which is understandable, but they think they can achieve this by hiding the environment.
They want the environment to be an invisible background consideration, an inconvenience whose existence should be minimized.

Sorry, but this is all wrong.
The environment is saving you from a ton of pain, and you should embrace it.
The best way to make things "just work" is for to design your workflow so that common mistakes are simply impossible.

This means you have to learn.

## What is an environment?

An environment is sort of like a "scope" that defines which computational resources are available and where they come from.
Your computer can contain many software tools on it, and those tools "live" in certain places in the computer.
When you run some piece of software, and it needs to reach out to some other thing you have installed on your computer (such as a matrix multiplication library), how does the software know where to find that other program?
When you install software, and it needs something on your computer, how does the software know where to find it?

Environments are one way to manage which resources are available to certain processes at certain times.

Let's demonstrate in the terminal.

If I go into the terminal and I run the `R` command...

``` sh
R
```

...the R interpreter program will open in the terminal.
I would see something like this:

    R version 4.3.3 (2024-02-29) -- "Angel Food Cake"
    Copyright (C) 2024 The R Foundation for Statistical Computing
    Platform: aarch64-apple-darwin20 (64-bit)

    R is free software and comes with ABSOLUTELY NO WARRANTY.
    You are welcome to redistribute it under certain conditions.
    Type 'license()' or 'licence()' for distribution details.

      Natural language support but running in an English locale

    R is a collaborative project with many contributors.
    Type 'contributors()' for more information and
    'citation()' on how to cite R or R packages in publications.

    Type 'demo()' for some demos, 'help()' for on-line help, or
    'help.start()' for an HTML browser interface to help.
    Type 'q()' to quit R.

    R > 

So this program must be installed on my computer somehow.

I can ask *where* the program is installed.

``` sh
which R

# /usr/local/bin/R
```

This says the `R` command is actually going to execute the command `/usr/local/bin/R`, which is a application installed in my computer in that path.
I can `ls` the directory and see that R is indeed installed there.

``` sh
# asks for only results containing "R" in the name
ls /usr/local/bin | grep R

# R
# Rscript
```

However, *I have other computational environments on my computer.*
I can ask where R is installed in those environments.
For example, if I `cd` to my website repo, I have a few environments that manage how I build some blog posts.
I can ask where R is installed in those environments.

``` sh
cd ~/projects/site-hugo && micromamba run -p build/conda_envs/qmd/blog/scrape-memoize-scum-data which R     
# /Users/michaeldecrescenzo/projects/site-hugo/build/conda_envs/qmd/blog/scrape-memoize-scum-data/bin/R
```

This command says, "go to this directory, and then run the `which R` command in the environment defined at this path".
And because that environment is its own isolated thing, the R interpreter in that environment is not the one in my computer's "global" scope.
So the path that is printed to the console is R interpreter in that specific environment.

## Why you should use environments

The benefit of this is you can control many separate projects on your computer that have different computational requirements.

-   Your projects need different versions of R or Python, depending on the project.
-   One project needs some package, but another project doesn't need it.
-   You want to prevent software upgrades from breaking your code, so you want to specify *which* version of a package you need for this project.
-   You want to test your project on another computer, and you need a way to quickly install the required dependencies on that other computer.
-   You move your project to a different location on *your own* machine, and you need to make sure all of the dependencies are in the right place.

Environments save you from all of this.

But you *must* use them intentionally to reap these benefits.

## Use the terminal

Although environments can be invoked by various GUI applications like VSCode or RStudio, I think there is no substitute for learning the fundamentals in the shell.
The terminal is where you learn what environments actually are, and if it doesn't make sense in the terminal, it is unlikely to make sense in the GUI.
GUIs can obscure what is really going on, they can set *their own* environment variables that interfere with the behaviors that you think you should be getting out of the environment.
It can be a huge mess, and if you don't know what *should* be happening (wisdom that you gain in the terminal), then you will have a hard time diagnosing how the GUI application is messing with you.

This doesn't mean you only have to use terminal-based applications like vim to do your work.
Instead, I recommend launching GUI applications *from the correct environment* in order to inherit your environment's behaviors.

For example, if I just open my terminal emulator in my computer (no special environment active), I can open VScode from the terminal like this:

``` sh
# open VSCode focusing on the current folder '.'
code .
```

...And VSCode is opened subject to the environment variables in that shell.
If I open VSCode's terminal and ask what `python` program is available, I get whatever I would have gotten in the shell that launched VSCode.
As it happens, I don't have a Python install available from that context.

``` sh
which python
# python not found
```

But if I go to my website repo's environment (which is managed by `uv`) and then launch VSCode from *that* environment...

``` sh
cd projects/site-hugo

# run "code ." in the local uv environment
uv run code .
```

then VSCode inherits that environment's background behaviors.
Which means that the VSCode terminal is aware of the Python binary that I use to managing my website.

``` sh
which python
# /Users/michaeldecrescenzo/projects/site-hugo/.venv/bin/python
```

So it is possible to both (a) get comfortable managing environments in the terminal, and (b) use the same GUI apps to edit your code as before.

## Projects should never share environments

Many people start using environments by building a single conda environment that they can activate from anywhere.
This is a recipe for disaster, because different projects may want competing dependencies.

This is one reason why you see "broke my conda environment again..." tweets.
They may have been using the same environment for too many things.

You should have one environment per project.
Or more!
Some projects require multiple environments.

But you should never mix projects in one environment.

## Build environments into a local path

When you create a conda environment, keep it inside the project directory.
You can do this with

``` sh
conda create -p path/to/env <list packages here>
```

or if your environment is defined in a `yml` file (more on that later):

``` sh
conda env create -f path/to/file.yml -p path/to/env`
```

In both examples, the `-p path/to/env` argument says to build and store the environment at that path, instead of in some global "default" path that conda/mambda/micromamba sets up for you.

What will actually live at that path is a bunch of folders and files containing binaries, packages, and so on that your project will use.
Quite literally, you will install Python/R/whatever you need into that folder.

The upside to this practice is that it's always easy to associate your project with its correct environment.
When you have environments floating around in the default global path, it is easy to forget which environment goes with which project.
It is needless mental burden.

You may find it helpful to mark these env paths as "private" directories however you wish (and add them to `.gitignore`).
Some people like to put these environmenets in `.venv` (the `.` at the front of the name hides the directory) or in directories whose names are prefixed with an underscore.
I often do `_build/envs/env-name`:

-   `_build` contains many things that I might build, which includes environments but also other things like generated data or output of some other kind
-   `envs` contains any environments, obviously
-   `env-name` is the specific name of the environment, but the project might need another environment to handle a separate, specific thing.
    This can happen if you need to compile something in one environment but use it in another environment.
    Situations like this are pretty common!

## You can run commands in the environment without "activating" the environment

"Activating" the environment means to initialize your terminal shell with paths and environment variables that the environment defines.
When the env is "active" then all commands will be run in that environment, without you specifying anything extra.
So `which python` would give me a different answer after I activate an environment that contains a Python installation.

But you don't have to activate the environment in order to run commands inside the environment.
With conda/mamba/micromamba for example you can do `micromamba run -p path/to/env <insert cmd here>` in order to run the command in the environment defined at `path/to/env`.
This is helpful when writing scripts: you can explicitly invoke an environment for specific commands without relying on any background context.
We saw examples of this above already.

This can be especially useful in complex scenarios where you might have multiple environments in play.
For example, when I build my website, my blog posts might have different computating environments (some use R code, some use Python code, some use none...).
When I render my blog posts, I need to do a series of `micromamba run -p path/to/blog-specific-env quarto render path/to/specific-blog-post.qmd` to render each post in its matching environment.
This may sound tedious, but:

-   It is necessary to prevent the dependencies of multiple blog posts from clashing with one another.
-   it is actually "easy", because the blog posts and their environments are associated to each other in a config file.
    So all the difficulty of the coordinated environments can be handled programmatically.

This is why it pays to be rigorous!
When your system follows good rules, you can leverage the computer to do the correct thing, easily, even in complex situations.

## Never use a global `.condarc` file

A [`.condarc`](https://docs.conda.io/projects/conda/en/latest/user-guide/configuration/use-condarc.html) defines some "common" behavior for all conda/mamba operations on your machine.
You can define some "default" channels that you want to search for packages to install and configure some options for how the dependency resolver algorithm works.

You should not use this file, because it controls *your machine* only.
This undermines reproducibility by injecting hidden configuration that is not checked into your project's source code control.
It is a big mistake that creates tons of reproducibility problems once you start sharing code with other people.
*Do not ever use this file*, and you should encourage your coworkers to stop using it also.

The way to get around `.condarc` is to be explicit when creating/modifying environments about which "channels" you are requesting packages from *at the level of the project*.

This sounds tedious, but it won't be if you also *define your environment in a `.yml` file*.

## Build your conda environment from a `.yml`. Never install things as you go

Another major footgun is to install things into your environment on an ad-hoc basis, for example `conda install polars`.[^1]
Package managers are nice because they can find a version of a package that can be installed into your present environment.
But things go wrong.
Sometimes they install a package into your environment while uninstalling or changing the versions of other dependencies, so it can break your code.
There are also sometimes situations where the package versions you get with one single environment "solve" are different from the versions you get with post-hoc package installations.
This means your enviornment is no longer reproducible.

Instead: define a `yml` file that lists the channels and packages to install, and build the environment from that file.
You can pin the package versions you need, which gives you more control over how your environment will be created in the future.
Here is an [example yml file from my website repo](https://github.com/mikedecr/site-hugo/blob/main/conda/hugosite.yml):

``` yml
name: hugosite
channels:
  - conda-forge
  - r
  - nodefaults

dependencies:
  # website core dependencies
  - hugo == 0.138.0
  - quarto == 1.5.57
  # scripting
  - python >= 3.10
  - ipython
  - typer
  - setuptools
```

And you would create this environent (according to all above instrucions) like this:

``` sh
micromamba create -f path/to/env-recipe.yml -p path/to/built-env
```

...which says "build the environment defined in this file, and put it at this path".

If you don't use conda, other package managers have other ways of encoding dependencies into a file for reproducibility, such as `requirements.txt` or `pyproject.toml`.
Regardless of your choice of tool, you should do something like this.

## Other quick tips:

This stuff is more optional, but can improve your UX.

-   [**Direnv**](https://direnv.net/). In the simple case where you want to activate an environment when you are in a project directory, you can use Direnv.
    This creates the effect where you `cd` to the directory, and your environment is automatically activated.
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

[^1]: Didn't you hear? Pandas is deprecated.
