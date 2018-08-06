# Contributing

## Pull Request Process

1. Discuss the change you wish to make via issue, email, or any other method before making a change.
2. Ensure your code complies with the conventions given in the section below. If you identify ambiguity please raise as an issue.
3. Ensure the [reskit features](https://github.com/petersbingham/reskit) are satisfied where relevant and that the appropriate utilities are used. 
4. Ensure any install or build dependencies are removed.
5. Update the README.md with details of your new Tool or any changes to current Tools.
6. Increase the version numbers in setup.py to the new version that this Pull Request would represent. See section below on versioning.
7. Respond to any feedback if given during PR review.

## Conventions

### Versioning
 - The reskit package uses semantic versioning: [SemVer](http://semver.org/).
 - The archive and code relating to it follow the convertion:
   - If the default configuration (in the default.yaml) changes, for example through the addition of another option or from optimisation, then a version number will be introduced or incremented in the archive configuration folder to reflect this. (eg. default -> default_v2). This will be accompanied with a patch increment in the reskit package version. In this case the user will have to manually create a copy of the default.yaml in the older release to continue using his old calculations (if they had been created using the old defaults).
   - If the actual routine that the configuration relates to changes then a version number will be introduced or incremented inside the yaml file. In this case the new version of reskit will not be backward compatible with any of the calculations obtained relating to this change using an older version of the software. This type of change will be accompanied with a major increment in the reskit package version.
 
### Naming
 - Follows [PEP8](https://www.python.org/dev/peps/pep-0008/), with the following exceptions:
   - Function names can have an upper case letter if that letter represents a scattering matrix. (eg get_elastic_Smat).
   - Function parameters can have an upper case letter if that letter represents a documented math variable (eg Npnts).
   - Otherwise, variable names must always be lower case.
   - The matfuncutil and tisutils containers have a lower case initial letter to indicate if discrete or continuous. Otherwise follows CapWord convention (eg `dSmat`). Instances of these classes are all lower case. eg dmat, dsmat etc.

### Documentation
 - All public functions must provide [numpy style docstrings](http://www.numpy.org/devdocs/docs/howto_document.html).

### Matrix indices
 - When annotating results: One based with `m`,`n` for subscripts.
 - When indexing in code: Zero based with `i`,`j` for index reference.
 
### File
 - Lines endings always use Linux style.
 - All non-python files also following PEP8 naming (short, all-lowercase names. Underscores only, no hyphens).
 - `.txt` files are used for ascii based results that are meant for user consumption.
 - `.dat` files can also be ascii based but are primarily for internal reskit usage.

## Hints and Tips
 - When converting between matrices (eg calling to_dKmat on a tisutil container) ensure that any slices are carried out first if applicable. This will reduce the number of conversion calculations.
