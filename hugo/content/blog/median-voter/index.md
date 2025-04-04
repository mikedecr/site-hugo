---
title: |
  It's perfectly fine to talk about the "median voter" like this
author: Michael DeCrescenzo
date: 2025-04-03T00:00:00.000Z
---


I am letting myself get nerd-sniped by some BlueSky politics discourse, and in my shame I will try to be quick with it.

In the aftermath of the 2024 election, "the left" has appeared divided about whether it should engage in more moderate politics to attract "the median voter".
Political scientist / respected mutual follow Jon Green [shared](https://bsky.app/profile/jongreen.bsky.social/post/3llrd4psnds2w) his [blog post](https://jgreen4919.github.io/notes/2025/04/mvt) about the assumptions behind the "median voter theorem" as popularized by Anthony Downs.
The subtext of the post is, as I read it, "Let's try to be a little more clear about what we're talking about here."
He proceeds to describe the many brittle assumptions that motivate what we call "the Downsian model."
The model is a mathematical formalism, so the assumptions have a particular rigity to them:

-   Voters have a preferred policy outcome in just one dimension (e.g. a left-right axis)
-   Voters preferences are exogenous (not affected by the maneuvers of politicians in the game)
-   Candidates for office position themselves sincerely on the same policy axis
-   Candidates can maneuver themselves freely on policy with no reputational cost
-   Voters have complete information about candidate positions on the same single dimension
-   Everybody "votes"

If the assumptions of the model hold, then the optimal thing for the politicians to do is to stake out identical policy positions at the location of the median voter.

On its face I take *zero issue* whatsoever with Jon's summary of the model.
However I did see [Osita Nwanevu](https://bsky.app/profile/ositanwanevu.bsky.social/post/3llrfskhzac2b) provide a bit of extra interpretation that I maybe find myself disagreeing with?
He writes in a few chained posts:

> I have seen the concept of the "median voter" accurately explained with reference to its actual origin in maybe two posts since policy school ten years ago.
> This is the second time.
> ([source](https://bsky.app/profile/ositanwanevu.bsky.social/post/3llrfgnklpk2n))

For what it's worth, big agreement here.
It is a big-time misunderstanding of the idea to think that the original author either believed in this model or thought it was realistic.
It was an exercise in articulating assumptions, exploring the predictions of a model, and contrasting those predictions with reality.
So, we're good here.

> I'd read an analysis of how this phrase broke out of academia to become a way for people who have no idea what it means to say "candidates should moderate" more wonkily.
> ([source](https://bsky.app/profile/ositanwanevu.bsky.social/post/3llrfskhzac2b))

Hmm...
If people think the text of Downs' work inherently justifies a "candidates should moderate" prescription, then I agree that is a misreading.
*However*, I think there is still a "colloquial" understanding of median-voter dynamics that is both

-   rationalizable as a useful-enough theory of political choice
-   shares the same *high level* conclusion that moderation can be beneficial, even if the exact formulation of what "moderation" means and how to achieve it are different from the single-dimension Downs model

...and I think that when advocates of "popularism" like David Shor or Matt Yglesias talk about how they think Democrats should be more moderate, they are talking about this *other model*.
I will give an informal description of it below to explain myself.

> Even more interestingly, you now have people invoking the median voter as a meme about how incoherent and complicated voter preferences are --- which is the opposite of the MVT's presumption!
> ([source](https://bsky.app/profile/ositanwanevu.bsky.social/post/3llrfzmod7k2c))

Just to make it explicit what Nwanevu is mentioning, there is recent research ([e.g.](https://benjaminlauderdale.net/files/papers/moderates_broockman_lauderdale.pdf)) to say that "moderate" voters are not "middle of the road".
They don't hold moderate stances; they hold extreme stances that are neither consistently liberal nor consistently conservative.
They may think that the stock market is rigged by rich people *and* that fluoride in the water is brainwashing us *and* that same-sex marriage is fine *and* that global warming is a hoax.
I also don't think this is a probem for the "colloquial" median voter theorem!

## A good-enough model for the contemporary "median voter"

Let's start by admitting that Jon Green's rundown of the faulty assumptions is entirely correct.
An incomplete list but covering the main ideas:

-   **One dimension**: clearly there is more going on than liberal vs. conservative
-   **Exogenous preferences:** politicians can influence voters' beliefs about specific issues and the *importance* of those issues
-   **Full participation:** goes without saying
-   **Complete information:** politicians can and will weaponize voter uncertainty to optimize their strategies
-   **Freedom of movement:** parties do have reputations, with both their partisan loyalist voters and oppositional voters

And here is a semi-formal way to describe voter preferences that does a good enough job both (a) explaining how party repuations *and* issue positions / issue salience can matter, and (b) is perfectly consistent with a plain-English use of the phrase "median voter".

-   **Issue dimensionality**: the true issue space is high-dimensional.
    Voters may have any configuration of beliefs about those issues.
-   **Dimensional reduction:** the true issue space is too big for parties to communicate efficienty through and for voters to efficiently understand themselves.
    So voters "project down" their beliefs into lower dimensions.
    If you are a linear algebra person you can imagine that the left-right axis is "in the column space of all issues" meaning that a voter takes a weighted average of their views across unrelated issues to reconstruct their own personal left-right position, or a position in a small number of dimensions where at least one is a common "left right" view.
    It is not really required for voters to have a shared understanding of what this left-right space is, in terms of the issue weights.
    In plain language this means that voters find ways to articulate to themselves how their views are consistent, they have a variety of strategies available to do this.
    They can emphasize the issues that fall most neatly on a liberal--conservative axis, or they just weight issues differently to make things feel the best to them.
    They can even be manipulated by candidates to care more about certain issues than others.
    Any of these mechanisms influence how voters "which" these issues into a simplified space, and they spend way more time in this projected-down space than they do in the full-complexity hyperplane of all issues.
-   **Parties try to influence how issues get bundled when voters conduct this simplification**.
    Again in linear algebra speak, the projection process is a weighted sum of issue "distances", and parties try to influence the basis functions (they try to convince voters that they are aligned on some issue) as well as the weights (they strategically try to make some issues more/less important in the minds of voters).
    In plain language, parties both do work to tie issues together along shared dimensions (abortion doesn't "go with" diplomacy, but parties make it so by presenting a platform), and voters simplify their own views either by using party cues to tie issue dimensions together or by weighting their issue stances to reconcile their own internal conflicts.
    When a partisan voter doesn't agree with their party on some issue, they tend either to change their view on that issue toward their party or tell themselves that the issue isn't that important.
-   **The campaign season is a battle to win a majority in the low-dimensional projected-down space.**
    There's obviously still some notion of "distance" even if we have more than one dimension, and parties try to minimize the distance for a winning number of people.
    This means there is still some notion of "middle" and voters who are near the middle.
    But it is sort of stochastic: the voters aren't all in the same *exact* space, but the spaces share some structure that is affected both by party reputations, partisan dynamics in the electorate, and the issue structure of the campaign.
    Parties may have different ideas of what they want to define as the middle, but it makes *perfect sense* for them to try to compete over how that space is shaped and thus the configuration of voters.
    In plain language, the parties put forth competing narratives and try to convince the most people that their narrative most resonates with voters' political values and priorities, even when the parties can manipulate what those values and priorities are.

I am sure that such a model exists in political economy scholarship, but I don't know that work very well so I can't credit the right person.
If you know who I should credit, please let me know however you can.
Although it does hint at some formalism (linear projection isn't the most intuitive for the lay reader) you don't really need to know linear algebra to get where I'm going with this.

You could be pedantic and say that this model is actually so general that polarization-focused, mobilization-based stratgies are consistent with the same generalized notion of "distance" as "moderate issues" might, it's just that the weight configuration is different and the "center" is closer to your party base.
You are correct, but you are misreading me, and I'm going to tell the teacher on you.
When someone uses the plain-language meaning of "moderate", what they mean is that they think it is *easier*, from a utility-maximization standpoint, for parties to configure the winning coalition by downweighting the most ideologically extreme issues and upweighting more broadly appealing issues.
They think some concentrations of voters in the low-dimensional space will be better for their electoral success, and some will be *easier to achieve* and the party wants to find some optimal compromise that is both advantageous and attainable.
So it is a constrained optimization problem.

We could find a few plausible economic reasons why moderating in the general election campaign could be appealing under this model:

-   It may be easier (that is, less costly) to to change the salience of issues in the minds of "moderate" or "median" voters.
    They have less crystalized beliefs about party reputations and so you might play an "issue ownership" strategy with them more easily.
    (Issue ownership is a concept where one party is more "trusted" to handle certain problems, and so parties to "define the problems" rather than focus on proposed solutions.)
    Critics of popularism accuse the movement of "selling your constituencies down the river," thinking specifically of LGBT rights issues which have been a bit less popular lately.
    I think the popularist retort under a model like this is that you wouldn't have to *do* anything differently as a legislator or an executive in terms of policymaking in order to just *talk about these issues* in ways that are more appealing to more people.
    You are trying to manipulate the salience of these issues and how they affect your party's reputation.
    You are not trying to move your *actual* policy ideas away from your base.
    It's an intervention on the weights, not the distances.
    Or you could try to introduce *uncertainty* about the distance in the eyes of voters who would be unhappy with your true position if they had full knowledge of it.
-   Persuasion on issues is hard to do, but it is easier to persuade the party faithful.
    Partisan voters are much more highly motivated to justify supporting their party, so you can "disappoint" them on the issues with much lower cost than to never court a moderate voter on their preferred issues.
    Your partisan loyalist is unlikely to vote-switch against you!
    There is obviously some tradeoff along the mobilization frontier here: if you are too moderate then your supporters may not turn out.
    I guess the popularists think that is way less risky from an expected-value point-of-view!
    And furthermore, mobilization doesn't happen in a bubble.
    When one party does well among moderate voters, that is typically becase the "tide" of the election is generally in their favor, which also drives mobilization of that party's core supporters.
    And from the hyperplane point-of-view: there's no such thing as the "tide" of an election without issue distances and issue weights, so it's all the same game.

## Conclusion

So, to recap.
I liked Jon's blog post a lot.
I agree with a lot of what Nwanevu was saying, but up to a point.
If he was trying to imply that popularism is somehow "incoherent" because it doesn't have a tenable model of what the median voter actually is, either because popularists believe in a false model or because "moderates" don't exist as such, I just don't agree with that claim.
I think it's perfectly reasonable to have a more authentic "median voter" model that squares just fine with the calls for moderation that we hear from some center-left voices.
