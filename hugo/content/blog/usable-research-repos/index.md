---
author: Michael DeCrescenzo
categories:
  - code
title: Replication code should be more usable.
date: '2022-05-15'
draft: false
image: featured.png
---


## Why do so many research projects' replication archives hurt?

My mind has been on **replication archives** lately.
I often go digging in other peoples' projects for data to practice some new statistical skill or another.
And I have been digging in *my own* projects lately to refactor some code for a dormant academic project.
In both of these situations I am interfacing with some else's code (me today ≠ me in the past), and in both situations I am having a bad time.

The academic community has been increasingly interested in replication archives since they realized that a lot of public research is, err, systematically untrustworthy.
Formal requirements (from journals) and informal pressures (from other researchers) in academia are increasingly requiring authors to prepare these repositories for new projects, which seems good on the whole.
But if you ever go digging in these republication archives, you quickly realize that just because authors provide data and code doesn't mean that the experience is all that helpful.
But why?
You can see the data, maybe the code runs without errors...What's the problem?

My main argument is that the code was not really designed to be understood or manipulated by other people.
If it were, the code would not look the way it does.

Now, I'm not an academic anymore, so don't have much stake in this.
But I do write quantitative research code in a collaborative environment at work all the time, with the intention that my code will be consumed and repurposed by others.
As it turns out, writing code under these conditions changes how you write that code, improves the reliability of your work, and has positive effects on the community in which your code is deliberated and consumed.
This blog post will attempt to distill some of the things I have learned into discrete, attainable lessons for writing academic research code.

Before I get too concrete though, I make a normative argument for caring about this at all.
Changing the way code is written takes effort, and I want to argue why that effort would be justified.

## Getting oriented

### This isn't about "good" code vs. "bad" code.

Like you, I don't have a defensible theory about what makes code Good for any enduring understanding of Good.
"Good" code seems like a contested and highly contextual idea.
Code may have "good properties", but certain features of code design also present important trade-offs, so goodness is understood relative to our goals.
So maybe we should start by talking about what we want academic code to do for us.

### What is the point of the code repository for academic projects?

I will discuss two broad models for code repositories, an *archive* model and a *product* model.
I am making these up as I go, but you will get the idea.

**The archive model.**
This is what most academic repositories are doing right now, I would guess.
We call these code repositories "replication archives" because that's what we think we want them to do: replicate and archive.
The model is focused on the "validity" of the code---does it correctly reproduce the results in the writing, tables, and figures (replication) in a robust and enduring way (archiving).

These are important goals, but focusing exclusively on them has some predictable side-effects.
The repositories end up serving as an audit trail for the paper, so the code is designed around the *rhetoric of the paper* instead of around the operations that the code performs.
We see files named things like `01_setup`, `02_clean-data`, `03_model`, `04_tables-figs`, `05_robustness` and so on.
Even supposing that all of the code runs just fine, all we can really do with the code is rebuild the paper exactly as it is.
If you could draw a web of all the interlocking pieces of this project, it would be a long, single strand from start to finish, highly dependent from one script to the next (perhaps intended to be run in the same R/Python session), with no feasible way to swap out any components for other components or modify them in isolation.
And crucially, if we wanted to use the data or some of the code from this project for some other purpose, we would have to mangle the project in order to extract the components we wanted.

**The product model.**
The product model organizes its code as if to offer it as a product for someone else to use.
The code is a key part of the research package, and researchers care that it is a good experience, just as they care about the quality of their writing.
An important assertion here is that there is value in the code even if the paper did not exist.
If a project proposes a method to measure or estimate a key variable, those methods are valuable outside of the context of the written paper, so part of the *product* of the project is to make these tools available and usable for other researchers to benefit from.
Projects that propose a new model make this model available for others to use with a practical interface.
Indeed, there may be a notion of *interface* as distinct from *infrastructure*; the code that drives the project at a high level is uniform and understandable, and the ugly code that does heavy lifting might be encapsulated away from the interface.
And better yet, the important infrastructure pieces are modularly designed: they may combine at the locus of the project, but the components can exist without reference to one another and could be exchanged for other components that perform similar functions.

### Increasing the amount of shared / re-used code would be good for research credibility and knowledge accumulation

Posting code online is not the same as making it usable.
I suspect many social scientists put code online without really wanting others to dig into it.
But there are real services that academics could provide for each other more regularly if they were more generous with the way their code is designed.
Political scientists in particular use a lot of the same data sources and do a lot of similar transformations on it, but why all the wasted effort?
I quite admire Steven V. Miller's [`peacesciencer`](http://svmiller.com/peacesciencer/ms.pdf) package for R, a set of tools whose rationale seems to be that there's no sense in having everybody duplicate each other's work to shape the data into common formats for analysis in political science.
I gotta say, I agree.

But it doesn't stop at broad-based datasets or data-shaping tools.
Think about every paper you have ever read that proposes a new way to measure something.
Did those authors provide a code module to do the appropriate calculations on new data of appropriate shape?
Did those authors provide an interface for validating these measures against alternatives?
I suspect that in most cases the answer is no.
The authors may put their code online, but it isn't online so that you can use it.
Not really.

I don't want to point fingers, so I will use some examples from my own academic work to show that I, too, wasn't thinking enough about this.
In my dissertation, I built a group-level measurement model to estimate latent political ideology in partisan groups at subnational units of aggregation, and I wrote a series of Stan files to iterate on a few approaches to it.
Other projects I have seen before and after I finished my thesis have built similar models.
Did I package my models into a tool that they could use?
No, I did not.
I also implemented a reweighting method for aggregated survey data that I first saw in a paper from nearly a decade ago.
This is probably a pretty broadly applicable correction for similar data, but did I provide a little module for others to apply the same calculations on data that wasn't exactly my own?
Nah.
I designed a Bayesian implementation of the [Acharya, Blackwell, and Sen formulation of sequential-*g* estimator](https://www.cambridge.org/core/journals/american-political-science-review/article/abs/explaining-causal-findings-without-bias-detecting-and-assessing-direct-effects/D11BEB8666E913A0DCD7D0B9872F5D11) that addresses some of the things that Bayesians would care about in situations like that, and I would even say I was pretty proud of it.
But I wasn't proud enough to share a generic version that others could use and adapt for their purposes.

You get the idea.

It just makes me worry that when we advertise our work as tools that others could use, we do not really mean it.
I worry that phrases like "We propose a method...", or "we provide an approach..." are only things we were trained to say to make it *sound* like we are contributing tools for the community.
But we are not doing the work that would make those tools available for others.
The code that goes into the paper repository is for ourselves, because the goal is getting our paper over the finish line.
The code is just another part of the game.

There recently was a [post on the Gelman blog](https://statmodeling.stat.columbia.edu/2022/03/04/biology-as-a-cumulative-science-and-the-relevance-of-this-idea-to-replication/) that stuck out to me about cumulative science and re-using each other's work.
Here is an excerpt that gives you the idea:

> How could a famous study sit there for 20 years with nobody trying to replicate it?
> \[...\]
> Pamela said this doesn't happen as often in biology.
> Why?
> Because in biology, when one research team publishes something useful, then other labs want to use it too.
> Important work in biology gets replicated all the time---not because people want to prove it's right, not because people want to shoot it down, not as part of a "replication study," but just because they want to use the method.
> So if there's something that everybody's talking about, and it doesn't replicate, word will get out.
>
> The way she put it is that biology is a cumulative science.

Thinking about how this applies to our code, it is clear that there is more than a vague moral value to posting usable code for others.
There is scientific value.
And it is interesting to me that after all the commotion about replication and [running code without errors](https://www.nature.com/articles/s41597-022-01143-6), there is comparatively little discussion about the scientific value of the code outside of the narrow, narrow context of the paper it is written for.

## What can be done?

Now that I am done complaining, we can talk about recommendations.
I will focus mainly on two concepts, interface and modularity, from a couple different angles.
Interface refers to the way other people use your tools.
Modularity describes how those tools are combined for easier development (for your own benefit) and exporting (for others' benefit).

### Interfaces for living projects, not memorials to dead projects

Whenever I want to download a project's data and code, I *only* want to get it from a version control platform like Github.
I want to fork the project, see the history, get the intended file structure, and maybe even contribute to the project by opening issues or pull requests.
I [never](https://twitter.com/rmkubinec/status/1514142461949583361) want to go to Harvard Dataverse.
I'm sure Dataverse was a great idea when it first hit the scene, but by today's standards, it feels like it is chasing yesterday's problems, like the problem of "pure replication".
But I think the credibility problems in social science warrant more than old-world-style replication.
We should be looking for platforms that accommodate and encourage sharing, re-use, mutual contribution, and stress-testing by others.

### Interface vs. Infrastructure

This is a pretty common distinction you hear about in software communities.
It isn't much discussed in academic research circles.

I will explain by way of example:
Think about the `tidyverse` packages in R, or just the `dplyr` and `tidyr` packages.
These packages provide an interface to useful data manipulations on data frames.
These are operations on *abstractions* of your data---an abstraction in the sense that the functions **do not have to know or care what is in those data frames** in order to operate on them.
The packages provide a *uniform* interface; they take a data frame as an input and return a data frame as an output, and the semantics are similar across functions.
This makes the operations *composable*, which is jargon for "the operations can be reordered and combined to achieve powerful functionality".
The same basic principles are true for other tools in the tidyverse like `stringr`, `forcats`, `purrr`, and so on.
They employ different abstractions for data organized at different levels (strings, factors, and lists respectively), but the emphasis on uniformity and composability is always there.

So that's the "interface" layer.
Now, what about the "infrastructure" or the implementation of these functions?
Do you know *anything* about how these functions are actually written?
And would it really matter if you did?
The infrastructure isn't what you, the user, care about.
What matters is that the tools provide a simple way to perform key tasks with your code without bogging you down in the implementation details.

Compare this to the way we write research code.
There is usually no distinction between interface and infrastructure whatsoever.
A lot of the time, we keep all of our nasty and idiosyncratic data-cleaning code right next to our analysis and visualization.
On a good day, we may smuggle the data-cleaning code into a different file, but that doesn't make a huge difference because the flow of the project is still mostly linear from raw data to analysis.
The user cannot really avoid spending time in the darkest corners of the code.

To be fair, it isn't necessary that an academic project's code base should produce an end result as concptually gorgeous as tidyverse tools are.
But there are probably some intertwined components in the research project that could be separated into interface and infrastructure layers somehow, and readers who really want to investigate the infrastructure are free to do so.[^1]

Thinking again about a paper that proposes a new way to measure a key variable, or a new method to analyze some data:
could those methods not be divided into an interface to access the method and an infrastructure that does the heavy lifting somewhere else?
Wouldn't you be more likely to use and re-use a tool like that?
Wouldn't it be more likely that if the method has a problem, we would have an easier time discovering and fixing it?
Wouldn't that look more like the iterative, communal scientific process that we wish we had?

### Little functions, good and bad

Should you make an interface by writing more functions?
Annoyingly, it depends.
One way to make an interface more legible to users is package annoying routines into functions that describe what you're accomplishing.
This is nominally easy to implement, but it isn't always easy to design well.
And the design considerations present plenty of trade-offs with [no obvious guiding theory](https://twitter.com/mikedecr/status/1524899107135016967).

Take a halfway concrete example.
You have a dataset of administrative data on many individuals, and the dataset has a field for individuals' names.
Your task is to clean these names in some way.

You choose to use some combination of regular expressions and `stringr` to do this.
But how do you implement this operation in the code?
One way is to create a new variable like...

``` r
new_df <- mutate(
    df, 
    name = 
        str_replace(...[manipulation 1 here]...) |>
        str_replace(...[manipulation 2 here]...) |>
        [...]
        str_replace(...[final manipulation here]...)
)
```

...and this works fine.
But if you wanted to change the way this name-cleaning is done, not only do you have to do surgery directly on a data pipeline, but you can't test your new implementation without re-running this mutate step over and over (which may be only one step of an expensive, multi-function pipe chain, but that is a separate, solvable issue).

Consider instead the possibility of writing a function called `format_names` that implements your routine.
Now your data pipeline looks like this...

``` r
new_df <- mutate(df, name = format_names(name))
```

Well, should you do that?
The routine is now encapsulated, so if you need to do it more places, you can call the function without rewriting the steps.[^2]
This makes your routine unit-testable: does it clean the patterns you want it to clean (and you are, of course, limited by the patterns you can anticipate).
It also makes it a little easier to change your implementation in one location and achieve effects in many places without doing surgery to your data pipeline.
Maybe it also makes it easy to move this step in your data pipeline around, which is good.

And what are the drawbacks?
Well, you no longer know what the function is doing without hunting down the implementation, and it's possible that the implementation is idiosyncratic to your project instead of being broadly rules-based.
In general, encapsulating code into a function makes it easier to "drive" code, but it doesn't inherently have any effect on whether your code is operating at a useful level of abstraction.
Nor does it have any obvious effect on whether the interface you design for one function is at all related to the interface you create for other functions---uniformity makes your functions easier to use and combine for powerful results.
If you aren't careful, you might write ten different functions that don't share a uniform abstraction or interface, so now it takes more effort for you to remember how your functions work than it does to write it out using stringr.
After all, stringr is already built on familiar abstractions: stringr don't know what your string is, and it does not care.
All it knows is that it has functions with similar semantics for doing operations on strings.

So, you have to think about what you want to accomplish if you want to have an effective design.

### More modules, fewer pipelines

So far I have been a little incredulous toward the idea that your code should be a "pipeline" for your data.
This is because pipelines are often in conflict with modularity: the principle of keeping things separate, independent, and interchangeable.
A lot of academic projects are lacking in it.

It is difficult at first to realize the drawbacks of non-modular pipeline organization because, especially with tidyverse tools, chaining many things together to do big things is the primary benefit.
When `dplyr` and `tidyr` first start clicking for you, you immediately begin chaining tons of operations together to go from A to B without a ton of code.
But as you iterate on the analysis, which requires breaking and changing things in your code, it can suddenly be very cumbersome to find and fix broken parts.
This is because you have twisted all of the important steps together!
You wrote the code in such a way that steps that do not depend on one another in principal now have to be organized and executed in a strict order.
And now the fix for one breakage leads you to break something else because the steps in your pipeline are not abstracted.
It is just nice to avoid problems like this.

To be clear, this is not the tidyverse's fault.
The tidyverse is an exemplar of modular design.
The problem is that you tried to string too much together without thinking about how to keep things smartly separated.
We should be asking ourselves questions like,

-   What *operation* (read: function) do I need to do here, regardless of what my particular *data* look like?
    That is, think more about functionality and less about *state*.
-   What can be separated?
    For instance, do I need the analysis of these 3 different data sources to happen in the same file?
    Or are they unrelated to the point where the analyses don't have to be aware of one another in any way?
    Again, functionality without state.
-   What can be encapsulated?
    Suppose I convince myself that the analyses of my 3 different data sources don't have to be aware of one another, but maybe there are some tools I can define that could be useful in each analysis.
    Perhaps I should encapsulate those tools under a separate file (read: a module!) and then import that module whenever I need it.
    This lets me both keep things separate without repeating the same steps in many places.
    We should be skeptical of encapsulation for its own sake---it isn't always necessarily helpful---but in this case it helps us separate functionality from state.
-   Correspondingly, what can be *exported* to other files in this project, or to other users who might want to use only that part?
    This is probably helpful to remember for cleaned data, repeated data manipulation tools, a new model that you build, and more.

If more pieces of your project are separable, interchangeable, and exportable, it becomes much easier to share little pieces of your project with other researchers.

### There's organization, and then there's organization

We know that our code should be organized, but it is easy to organize code ineffectively.
Something we see a lot in research code is an organizational structure that is perfectly *discernible* but not exactly *useful*.
I have created plenty of impeccably "organized" but unhelpful repositories.

One discernible but not-very-useful organizational pattern is to name your files as steps along a data analysis pipeline: `01_setup`, `02_clean-data`, `03_model`, `04_tables-figs`, `05_robustness`, and so on.
Again, guilty.
This setup doesn't help the researcher keep themselves "organized" if every problem they have to solve is tangled together in one bucket ambiguously labeled "data cleaning".
And it doesn't help anyone consuming the project understand or modify which pieces of the code are responsible for which functionality.

But if you are being a good citizen---designing modularity into your code, creating a useful interface, dividing functionality across files, separating analyses that don't depend on one another, and so on---the pipeline organization will not be the dominant feature.
It will naturally be replaced by a layout that reflects the concepts in the code, not the rhetorical contours of a research paper.
The code is not a paper, and a paper is not its code.

To be sure, you cannot kill every little pipeline; data always need to be read, shaped, and analyzed.
But building your code on effective abstractions lets you write smaller pipelines that are quicker from start to finish, conceptually simpler, and untangled from other independent ingredients in your project.
The ultimate goal is usable code, not killing pipelines.
It just happens that small, minimal pipelines are more usable than gigantic, all-encompassing pipelines.

### Judicious usage of "literate programming"

Many researchers agree that statistical output should be algorithmically injected into research writeups to ensure the accuracy of the reporting.
This is the *real* reason to use document prep systems like Rmarkdown or (increasingly) Quarto: not for the math typesetting.

But it is also a *problem* if the statistical work is so intertwined with the manuscript that they cannot be severed in the code.
I myself have written plenty of "technically impressive" Rmarkdown documents that are actually are fragile Jenga towers of tangled functionality.

This is a pretty easy lesson though.
The .Rmd file shouldn't be the place where important, novel analysis happens.
That should happen elsewhere, and your paper should be epiphenomenal to it.

### Who's looking at your code?

You learn a lot by having other people make suggestions to you about the way your code is structured.
I suspect most academic projects, even those with multiple co-authors, don't feature much code criticism or review of any kind.
Outsourcing code tasks to graduate students is great for developing their skills, but if you (the person reading this) are the veteran researcher, they would also benefit from your advice.
The student and your project will be better for it.

### Don't propose methods. Provide them.

I have said this already, but I wanted to sloganize it.

## Better code vs. the Academy

This section could be its own blog post, but I am not an academic anymore and do not want to spend too much energy arguing about stuff that I intentionally left behind.
But in case you are thinking about the following things, I just want you to know what I see you, I hear you, but I think these are the questions you have to answer for yourselves.

-   **Writing better code will not help my paper get published.**
    Yeah, that sucks, right?
    Why is that?
    If we can agree that more usable code will make it easier to share tools among researchers, test-drive the contributions of other researchers, and bolster the credibility of your field overall, why does your publication model think that it's a waste of your time as a researcher?
-   **This all sounds very hard, and I am not a software engineer.**
    You shouldn't have to be a software engineer if you do not want to be.
    What I *do* wish is for your field to sustain broader collaboration where you have a team of people who are good at different things so your field can put out more reliable products.
    But many fields care about superstar researchers.
    I do not care about superstar researchers.

## What we haven't said

Here's a recap of all the things we did not mention about replication / archiving discussions:

-   Packaging environments and dependencies
-   Relatedly, containerization
-   Solutions for long-term archiving
-   Commenting code / other documentation

I think these problems are important to varying degrees.
I mean, I am not as concerned about containerization, but you are free to be.
But these issues are more commonly discussed than the design, usability, and shareability of code.
So I didn't talk about them.

[^1]: It is also worth noting that merely *hiding* the messiness behind a function isn't really the best way to proceed.
    What you want to achieve by separating the implementation is some kind of abstraction away from the particularities of your data into something simpler and more principled.
    See this entertaining talk on the difference between ["easy" and "simple"](https://www.youtube.com/watch?v=SxdOUGdseq4).

[^2]: Better yet, if the patterns you need to clean about the names are the same things you would need to clean about other strings, you could design the function to be abstracted away from "names" altogether.
