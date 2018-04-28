## Conventions

### Matrix indices
 - When annotating results: One based with i,j for subscripts.
 - When indexing in code: Zero based with m,n for index reference.
 
### matfuncutil and tisutil Containers
 - Class definitions use the format dVal, dVec, dMat, dSmat, dKmat etc. ie. First letter after d or c is capitalised.
 - Instances of these classes are all lower case. eg dmat, dsmat etc.

## Hints and Tips
 - When converting between matrices (eg calling to_dKmat on a tisutil container) ensure that any slices are carried out first if appropriate. This will reduce the number of conversion calculations.