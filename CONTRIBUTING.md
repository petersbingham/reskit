# Contributing

## Pull Request Process

1. Discuss the change you wish to make via issue, email, or any other method before making a change.
2. Ensure your code complies with the conventions given in the section below. If you identify ambiguity please raise as an issue.
3. Ensure the [reskit features](https://github.com/petersbingham/reskit) are satisfied where relevant and that the appropriate utilities are used. 
4. Ensure any install or build dependencies are removed.
5. Update the README.md with details of your new Tool or any changes to current Tools.
6. Increase the version numbers in setup.py to the new version that this Pull Request would represent. The versioning scheme used by reskit is [SemVer](http://semver.org/).
7. Respond to any feedback if given. Once at the required standard the Pull Request will be accepted (assuming you got the go-ahead at step 1).

## Conventions

### Naming
 - Follows [PEP8](https://www.python.org/dev/peps/pep-0008/), with the following exceptions:
   - Function names can have an upper case letter if that letter represents a scattering matrix. (eg get_elastic_Smat).
   - Function parameters can have an upper case if that letter represents a documented math variable (eg Npnts).
   - Otherwise, variable names must always be lower case.
   - The matfuncutil and tisutils containers have a lower case initial letter to indicate if discrete or continuous. Otherwise follows CapWord convention (eg `dSmat`). Instances of these classes are all lower case. eg dmat, dsmat etc.

### Documentation
 - All public functions must provide [numpy style docstrings](http://www.numpy.org/devdocs/docs/howto_document.html).

### Matrix indices
 - When annotating results: One based with `m`,`n` for subscripts.
 - When indexing in code: Zero based with `i`,`j` for index reference.
 
### File
 - Lines endings always Linux style.

## Hints and Tips
 - When converting between matrices (eg calling to_dKmat on a tisutil container) ensure that any slices are carried out first if applicable. This will reduce the number of conversion calculations.
