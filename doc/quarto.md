Quarto things to remember:

- We get the best control over `render` and `output-dir` when `_quarto.yml` is local to the src.
  This is not necessarily at the top level of the project.
- We will want a way to ensure we build in the correct environment _per post_.
  This probably means we should walk the content with a build script instead of running `quarto` on the whole directory.
- clone to `submodules`, link content to `src` and place other build scripts there?
