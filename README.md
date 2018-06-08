# reskit
Python Package to assist with the identification and characterisation of quantum scattering resonances.

WARNING: There are known issues with the latest version of sympy that affect the execution of reskit. See the instructions below for installing the known working version into a special folder inside the reskit package. 

## Installation

Clone the repository and install with the following commands:

    git clone https://github.com/petersbingham/reskit
    cd reskit
    python setup.py install
    
## Dependencies

Currently reskit only supports python 2.7.

reskit encapsulates a group of python packages referred to as reskit utilities (see below). These can either be installed separately, in which case the readme for that utility should be consulted, or a contained script can be executed to install versions of the utilities that were tested against for the current reskit release. These will be installed into an internal reskit folder that will be added to the path on import of reskit. If the user wishes to use the latest versions of the utilities they should check the version number for any compatibility breaks ([SemVer](http://semver.org/): basically when the major version number changes there has been a compatibility break). Note that some distributions of reskit come with the utilities already installed.

In a similar manner there is an optional (but recommended) script to install tested versions of the third party (eg numpy etc) dependencies required by reskit. Again these are installed into an internal reskit folder and will not affect any current version of these dependencies that the user happens to have installed into their standard site-packages folder. The remainder of this section will describe the two scripts for installing the dependencies.

Both of the scripts can be found in: https://github.com/petersbingham/reskit/tree/master/reskit/site-packages. Following installation as described above these scripts are typically found in:
  - Windows: `C:\Python27\Lib\site-packages\reskit\site-packages`
  - Linux root: `/usr/local/lib/python2.7/site-packages`
  - Linux home: `~/.local/lib/python2.7/site-packages`

The scripts are:
  - `get-thirdparty.sh`, which installs the specified versions of:
    - numpy
    - scipy
    - sympy
    - mpmath
    - matplotlib
    - pyyaml
    - tabulate
  - `get-utilities.sh`, which installs the specified versions of:
    - [matfuncutil](https://github.com/petersbingham/matfuncutil)
    - [tisutil](https://github.com/petersbingham/tisutil)
    - [channelutil](https://github.com/petersbingham/channelutil)
    - [pynumwrap](https://github.com/petersbingham/pynumwrap)
    - [parsmat](https://github.com/petersbingham/parsmat)
    - [stelempy](https://github.com/petersbingham/stelempy)
    - [pynumutil](https://github.com/petersbingham/pynumutil)
    - [twochanradialwell](https://github.com/petersbingham/twochanradialwell)
    - [ukrmolmatreader](https://github.com/petersbingham/ukrmolmatreader)

The user can modify either of the get scripts to remove or comment any package he doesn't require before running the script. For example, if only the locked sympy version is required and the user is happy with his own version of numpy, he can open the get-thirdparty.sh and comment the line responsible for installing numpy.

## Overview

Reskit was designed with the following features in mind:
  - Easily extendable. Different techniques for location and characterisation of quantum resonances can be implemented and added as reskit Tools.
  - Tidy parameter specification. Often calculations have extensive parameters and it can be messy to pass all of these in as function arguments. Reskit provides two levels of parametrisation:
    - High level parameters as function arguments.
    - Low level (and/or advanced) parameters specified in yaml files. The software will provide defaults for these in a default.yaml. If the user wishes to override they can create their own .yaml and pass the path to this to the reskit API.
  - Smart archiving of results. Reskit takes a path to an archive into which all calculations will be written, along with their parameters. This provides a high level of tracability, easy reproduction and reuse of previously acquired intermediate results.
  - Type abstraction. Reskit supports both standard python types (using the numpy package) and arbitrary precision mpmath types.
  - Support for data in both continuous and discrete forms. For example S-matrix data can be provided as both a discrete set of data or as a function reference to some analytical expression.

As such the reskit interface is fairly generic, providing the following functions (see doc strings for details and parameter descriptions):
  - `get_asym_calc`: Returns a calculator (`AsymCalc`) containing all of the channel information for the scattering system.
  - `get_dmat_from_discrete`: Initialises a reskit container from a discrete set of data and an `AsymCalc`. The data can be K, S or T matrices.
  - `get_dmat_from_continuous`: Initialises a reskit container from a function reference. The function reference will map an energy argument to either a K, S or T matrix.
  - `get_tool`: Returns a Tool using the reskit container returned from `get_dmat_from_discrete` or `get_dmat_from_continuous`. A tool is typically an implementation of a technique for the location and characterisation of resonances or scattering data.
  - `use_python_types`: Specifies to use python types with numpy operations.
  - `use_mpmath_types`: Specifies to use mpmath types and operations. The dps can be provided as argument.

![reskit design](https://github.com/petersbingham/reskit/blob/master/reskit.jpg)

## Tools

Reskit currently has two Tools, the `chart` Tool and the `mcsmatfit` Tool. These are introduced in the examples below, detailed reference can be found in the code docstrings. There are two example systems that are used and are provided by resket. These can be located in the reskit/examples folder; they are the radial well and the pyrazine molecule.

### `Chart` Tool

The `Chart` Tool provides simple charting of the scattering representations and their observable quantities.

```python
import reskit as rk
import channelutil as cu
import twochanradialwell as tcrw

# Get a calculator with units and channel angular momentum for the two channel,
# elastic radial well.
calc = rk.get_asym_calc(rk.hartrees, [0,0])
# Get a function reference for the S matrix.
csmat = tcrw.get_Smat_fun(1.0, 2.0, 2.0, calc, 1.0)
# Initialise the data from the function reference into the required container
# (get_Smat_fun returns the required container but we include the following line
# for illustration purposes).
dmat = rk.get_dmat_from_continuous(rk.Smat, csmat, calc, 1., 8., 1200, "radwell")

# Get the chart tool
chart = rk.get_tool(rk.chart, dmat, "results")

# Do some plots
chart.plot_Kmatrix(num_plot_points=300)
chart.plot_TotalXS(num_plot_points=300, logy=True)
```

The "results" argument in the `rk.get_tool` function is the location of an archive into which the results will be stored. A copy of the two plotted charts in the example will be saved to the path: ./results/radwell/numpy/(1e+00,8e+00,1200)/chart.

### `MCSMatFit` Tool

The `MCSMatFit` Tool is based on the technique described in "S.A. Rakityansky P.O.G. Ogunbade. S-matrix parametrization as a way of locating quantum resonances and bound states:multichannel case, 2010". In essence, it provides a rational S-matrix from a set of discrete S-matrix values along the real energy axis. The poles of the S-matrix can then be located by looking for the stable roots of the denominator. It uses the packages [parsmat](https://github.com/petersbingham/parsmat) and [stelempy](https://github.com/petersbingham/stelempy); additional documentation can be found in the README.mds included in these packages.  

```python
import reskit as rk
import channelutil as cu
import ukrmolmatreader as rmol

# Use mpmath types (optional)
rk.use_mpmath_types()

# Read in the K matrix data
kmatdict,_ = rmol.read_Kmats("kmatrix_input_pyrazine.dat")

# Get a calculator with units and channel angular momentum
calc = rk.get_asym_calc(rk.rydbergs, [3,5,5])
# Initialise the data into the required container
dkmat = rk.get_dmat_from_discrete(rk.Kmat, kmatdict, calc, "pyrazine")
# Slice the data set (optional)
dkmat2 = dkmat[0:1200]

# Get the mcsmatfit tool
sfittool = rk.get_tool(rk.mcsmatfit, dkmat2, "results")

# Perform the calculation of the poles and the qualityindicators
cfins = sfittool.get_elastic_Fins(range(2,32,2))
sfittool.find_stable_Smat_poles(cfins)
```

Again, the "results" argument in the `rk.get_tool` function is the location of an archive into which the results will be stored. There are many more result files generated from this example than for the chart, since there are intermediate calculations. The final results are in the QIs_E.dat and QIs_k.dat files, which list the identified poles (as either Es or ks) and their associated QIs. These files (for the given example) can be found in: ./results/pyrazine/mpmath_100/(0,1200,None)/mcsmatfit/poles/default/[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]. The following intermediate results are generated:
  - Pole convergence tables. In the same folder as the QIs_E.dat and QIs_k.dat files, they are named like dk1e-09.dat, referring to the relative comparison threshold used in the calculation. The user is referred to [stelempy](https://github.com/petersbingham/stelempy) for a description of this table.
  - Root files. These list all of the roots for a given M and can be found in: ./results/pyrazine/mpmath_100/(0,1200,None)/mcsmatfit/roots/default. See [parsmat](https://github.com/petersbingham/parsmat) for further details.
  - Coefficient dirs. These contain the coefficients for a given M and can be found in: ./results/pyrazine/mpmath_100/(0,1200,None)/mcsmatfit/coeffs/default. See [parsmat](https://github.com/petersbingham/parsmat) for further details.

## Contributing

Contributions are welcome. Please see [CONTRIBUTING.md](https://github.com/petersbingham/reskit/blob/master/CONTRIBUTING.md) for guidelines.
