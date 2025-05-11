---
title: 'Sugar-free: Python dictionaries'
author: Michael DeCrescenzo
date: 2025-05-08T00:00:00.000Z
engine: knitr
knitr:
  opts_chunk:
    collapse: true
    comment: |-

      ##[out]
---


The subject of our madness today is **syntax sugar** and **Python dictionaries**.
Specifically, the operation of combining multiple dictionaries into one.
We ask the following question as motivation:

> Does there exist a *function* in Python that merges two or more dictionaries into a single, new dictionary?

There exist plenty of *ways* to merge dictionaries in Python, but are any of them functions with signatures like this?

``` python
def merge_dicts(dicts: Iterable[dict]) -> dict:
    # insert definition here
```

## Why do I care about this?

Here's the way it usually goes.

-   You learn a bit of functional programming, and it really clicks how functions can express tons (most? all?) of useful programming concepts in a general way.
-   The framework is *so* general that you start applying it places where it shouldn't be applied.
-   Your suffering is now your own fault.

I am being silly, but I have this irrational beef with Python.
Python has a lot of trivial syntax sugar for operations that could simply be functions.
I like functions because you can *do things* with functions: composing, mapping, reducing, currying.
You can't *do* much with syntax sugar.
In Python, all the sugar is parsed away to C code before any operations are actually executed against your data.
So the syntax sugar in Python is convenient, but *programmatically* it is kind of useless.

Let's look at the ways Python can combine dictionaries.

## For-looping and `dict.update`

You have two dictionaries.

``` python
dict_1 = {"A": 1, "B": 2}
dict_2 = {"C": 3, "D": 4}
```

Dictionaries have the `.update` method, which adds key--value associations to a dictionary inplace.
This will mutate the dictionary, so if you want to create a *new* dictionary containing the union of these associations, you must initialize an empty dictionary first.

``` python
result = {}
result.update(dict_1)
result.update(dict_2)
print(result)

##[out] {'A': 1, 'B': 2, 'C': 3, 'D': 4}
```

I wouldn't call this "syntax sugar", but it isn't usable in higher-order functions because `dict.update` doesn't return a value.
So you cannot `reduce` this function over a list of dictionaries.

``` python
from functools import reduce

list_of_dicts = [dict_1, dict_2]

a = reduce(dict.update, list_of_dicts, {})

##[out] TypeError: descriptor 'update' for 'dict' objects doesn't apply to a 'NoneType' object
print(a)

##[out] NameError: name 'a' is not defined
```

That said you can do multiple `.update`s in a loop:

``` python
result = {}
for d in list_of_dicts:
    result.update(d)

print(result)

##[out] {'A': 1, 'B': 2, 'C': 3, 'D': 4}
```

You would need to turn this into your own function to pass it to higher-order functions.

``` python
def merge_dicts(dicts: list[dict]) -> dict:
    result = {}
    for d in dicts:
        result.update(d)
    return result
```

## Unpacking

Dictionary unpacking *does* create a new dictionary; it doesn't mutate an existing dictionary.
However it *is* syntax sugar, so it *cannot* be scaled over a large number of dictionaries.

``` python
{**dict_1, **dict_2}

##[out] {'A': 1, 'B': 2, 'C': 3, 'D': 4}
```

I would admit that the unpacking mechanism is useful for arbitrary keyword arguments in function definitions.
But as a way of merging dictionaries I think it is basically useless compared to dictionary comprehension.

## Dictionary comprehension

This is pure syntax sugar, so it cannot be used in higher order functions.
But it creates a new dictionary, which I prefer, and you can scale this method to arbitrarily many dictionaries.

``` python
{key: val for dict in list_of_dicts for key, val in dict.items()}

##[out] {'A': 1, 'B': 2, 'C': 3, 'D': 4}
```

## The OR (`|`) operator

<figure>
<img src="linkedin_dict_or.jpeg" alt="The text of the post reads: Do you need a clean way to merge two dictionaries in Python? Use the | operator (available since Python 3.9) Unlike other methods (like the .update method or unpacking), it offers a neat way to merge dictionaries. See below for a small example." />
<figcaption aria-hidden="true">The text of the post reads: Do you need a clean way to merge two dictionaries in Python? Use the | operator (available since Python 3.9) Unlike other methods (like the .update method or unpacking), it offers a neat way to merge dictionaries. See below for a small example.</figcaption>
</figure>

The OR operator is a weird sugar hybrid becuase although its *intended* use is pure sugar...

``` python
result = dict_1 | dict_2
print(result)

##[out] {'A': 1, 'B': 2, 'C': 3, 'D': 4}
```

The unique thing about the OR operator is that operators in Python are just methods in disguise.
In the case of the OR operator, the method name is `__or__`.

``` python
result = dict_1.__or__(dict_2)
print(result)

##[out] {'A': 1, 'B': 2, 'C': 3, 'D': 4}
```

And although it is ugly, you *can* pass the `__or__` dunder-method to higher-order functions.

``` python
result = reduce(dict.__or__, list_of_dicts)
print(result)

##[out] {'A': 1, 'B': 2, 'C': 3, 'D': 4}
```

And if we wanted to make a `merge_dicts` function, using `dict.__or__` is the most functional-programming-brained way to do it so far.

``` python
from functools import partial

merge_dicts = partial(reduce, dict.__or__)
```

You probably see this and say "WTF did I just read", but as you can see...

``` python
merge_dicts(list_of_dicts)

##[out] {'A': 1, 'B': 2, 'C': 3, 'D': 4}
```

## The `ChainMap` class

Ah. Okay.
Here is a class in the standard library that actually takes multiple mappings, on construction, and returns a new object containing the union of the mappings.
And it feels like a function call.

``` python
from collections import ChainMap

chain = ChainMap(*list_of_dicts)
print(chain)

##[out] ChainMap({'A': 1, 'B': 2}, {'C': 3, 'D': 4})
```

You can get creative with these mapping unions...

``` python
nested_chain = ChainMap(dict_1, ChainMap(dict_2))
print(nested_chain["C"])

##[out] 3
```

You can pass this constructor to `reduce`!

``` python
reduced_chain = reduce(ChainMap, list_of_dicts)
reduced_chain["A"]

##[out] 1
```

But the behaviors of `ChainMap` are unusual compared to other approaches.
We can learn how by reading the docstring.

> class ChainMap(collections.abc.MutableMapping)
> ChainMap(\*maps)
>
> A ChainMap groups multiple dicts (or other mappings) together
> to create a single, updateable view.

OK so far so good...

> The underlying mappings are stored in a list. That list is public and can
> be accessed or updated using the *maps* attribute. There is no other state.

Interesting, let's see this:

``` python
chain.maps

##[out] [{'A': 1, 'B': 2}, {'C': 3, 'D': 4}]
```

Let's go on.

> Lookups search the underlying mappings successively until a key is found.

This sounds benign at first but it is actually opposite the behavior of other "union" methods.
To demonstrate, let's give two different mappings an "X" key.

``` python
a = {"X": 1}
b = {"X": 2}
```

When we merge these dictionaries using, say, `.update`, "new" associations always override "old" associations.

``` python
result = {}
result.update(a)
result.update(b)
print(result["X"])

##[out] 2
```

Similar for dictionary comprehension:

``` python
result = {key: val for dict in [a, b] for key, val in dict.items()}
print(result["X"])

##[out] 2
```

but with `ChainMap`, the original mappings are preserved, and we search for the first occurence of the key in order from the first mapping to the last.
So when when we pass dicts that map "X" to 1 and "X" to 2, we stop when we find 1.

``` python
chain2 = ChainMap(a, b)
print(chain2["X"])

##[out] 1
```

And now the most "Pythonic" thing of all: mutating stuff that you don't want to be mutated.

> In contrast, writes, updates, and deletions only operate
> on the first
> mapping.

So if we try to add a new association, we mutate the first dictionary that we supplied to the `ChainMap`.
Recall that we built this chain out of two dictionaries, `a` and `b`.
If I add an association to the `ChainMap`...

``` python
chain2["Y"] = 3
```

Look what happens to `a`.

``` python
print(a)

##[out] {'X': 1, 'Y': 3}
```

This is insanity.

## What if we could fix `ChainMap`?

As a fun little exercise, let's "fix" these two weird aspects with `ChainMap`.
Newer associations should dominate older associations on construction, and additional associations should not mutate any data.

All we need to do is initialize a `ChainMap`-like object with two additional details.
First, we sneak an empty dictionary into the front of our list of maps.
This way, new keys are added to this empty dictionary instead of mutating any data.
And second, we reverse the list of provided maps, so new keys always "override" the old keys.

``` python
class MergedMap(ChainMap):

    def __init__(self, *maps):
        self.maps = [{}, *reversed(maps)]
```

``` python
a = {"X": 1}
```

``` python
merged = MergedMap(a, b)
```

Now when we lookup "X", we should get 2 instead of 1.

``` python
print(merged["X"])

##[out] 2
```

And if we add a new "Y" association, it should not affect our original mappings.

``` python
merged["Y"] = 3
print(f"{merged['Y']=}")

##[out] merged['Y']=3
print(f"{a=}, {b=}")

##[out] a={'X': 1}, b={'X': 2}
```
