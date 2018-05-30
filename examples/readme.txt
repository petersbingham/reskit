After you have installed reskit and all of its dependencies (see README.md) type
at a command prompt in this directory:

python reskit_examples.py 1st 2nd 3rd
where:
 1st: Scattering system. Either:
  radwell, pyrazine or uracil
 2nd: Command. Either:
  poles, plotSmat, plotTotXS or createLatex
 3rd: Max N (if 2nd==poles) or plot N (if 2nd==plotSmat or 2nd==plotTotXS)
  optional. Default 40 (if 2nd==poles) or 20 (if 2nd==plotSmat or 2nd==plotTotXS)

Eg: python reskit_examples.py radwell poles

A file path will be outputted to the prompt. The location of results will be
contained in this file. There are a lot of intermediate results; the final
results will be near the end of the log when the calculation has completed.
