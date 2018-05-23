## Conventions

### Naming
 - Follows PEP8, with the following exceptions:
 - Function names can have an upper case letter if that letter represents a scattering matrix. (eg get_elastic_Smat).
 - Function parameters can have an upper case if that letter represents a documented math variable (eg Npnts).
 - Otherwise, variable names must always be lower case.
 - The matfuncutil and tisutils containers have a lower case initial letter to indicate if discrete or continuous. Otherwise follows CapWord convention (eg dSmat). Instances of these classes are all lower case. eg dmat, dsmat etc.
 
### Matrix indices
 - When annotating results: One based with m,n for subscripts.
 - When indexing in code: Zero based with i,j for index reference.
 
### File
 - :Lines endings always Linux style.

## Hints and Tips
 - When converting between matrices (eg calling to_dKmat on a tisutil container) ensure that any slices are carried out first if appropriate. This will reduce the number of conversion calculations.