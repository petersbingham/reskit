After you have installed reskit and all of its dependencies (see README.md) type
at a command prompt in this directory:

python reskit_examples.py 1st 2nd
where:
 1st: Scattering system. Either:
  radwell, pyrazine, uracil6ch or uracil10ch
 2nd: Command. Either:
  poles, plotSmat or plotTotXS.

Eg: python reskit_examples.py radwell poles

A file path will be outputted to the prompt. The location of results will be
contained in this file. There are a lot of intermediate results; the final
results will be near the end of the log when the calculation has completed.
