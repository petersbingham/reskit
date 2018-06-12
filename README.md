# reskit
Python Package to assist with the identification and characterisation of quantum scattering resonances.

WARNING: There are known issues with the latest version of sympy that affect the execution of reskit. We recommend using virtualenv to use the correct versions of the dependencies. This is fully explained in the instructions below.

## Getting reskit

Git clone the repository with the following command:

    git clone https://github.com/petersbingham/reskit
    
## Dependencies

Currently reskit only supports python 2.7.

Third party packages:
  - numpy
  - scipy   
  - sympy
  - mpmath
  - matplotlib
  - pyyaml
  - tabulate

reskit utilities:  
  - [matfuncutil](https://github.com/petersbingham/matfuncutil)
  - [tisutil](https://github.com/petersbingham/tisutil)
  - [channelutil](https://github.com/petersbingham/channelutil)
  - [pynumwrap](https://github.com/petersbingham/pynumwrap)
  - [parsmat](https://github.com/petersbingham/parsmat)
  - [stelempy](https://github.com/petersbingham/stelempy)
  - [pynumutil](https://github.com/petersbingham/pynumutil)
  - [twochanradialwell](https://github.com/petersbingham/twochanradialwell)
  - [ukrmolmatreader](https://github.com/petersbingham/ukrmolmatreader)

We recommend using specific versions of these dependencies, especially for the third party packages. If the user wishes to try his luck with later versions of the utilities they should check the version number for any compatibility breaks (the utilities use [SemVer](http://semver.org/)). Note that some distributions of reskit come with the utilities already installed.

### Installing dependencies with virtualenv

virtualenv sets up an entire python distribution, with the correct dependency versions in a local directory. This means that you won't affect your global python distribution (since installing a specified version into your global distribution will override any existing install versions of that dependency). 

virtualenv is a tool, which you can install (if not already installed) with the following command (if you dont have root access add '--user' to the end of the command to install into your home):

    pip install virtualenv

Once installed and assuming that you are in the same directory where you did the git clone set up the local virtualenv with the following commands:

    cd reskit
    virtualenv env
    
You now need to run a virtualenv activate script to setup your path to use this local version of python. Note that for some versions of virtualenv the activate script is in the `bin` folder rather than the `Lib` folder. On Windows type:

    env/Scripts/activate.bat

On Linux type:

    source env/bin/activate

You can now install the dependencies into your virtualenv with the following commands:

    pip install -r requirements.txt
    python setup.py install

## Running reskit

If you are using virtualenv you will have to setup your environment before invoking the interpreter by running the activate script as detailed above. If you are in the reskit folder on Windows you can type the following commands:

    env/Scripts/activate.bat  # source env/bin/activate on Linux
    python  # will start the interpreter
    import reskit

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
  - `get_tool`: Returns a Tool using the reskit container returned from `get_dmat_from_discrete` or `get_dmat_from_continuous`. A Tool is typically an implementation of a technique for the location and characterisation of resonances.
  - `use_python_types`: Specifies to use python types with numpy operations.
  - `use_mpmath_types`: Specifies to use mpmath types and operations. The dps can be provided as argument.

![reskit design](https://github.com/petersbingham/reskit/blob/master/reskit.jpg)

## Tools

Reskit currently has two Tools, the `Chart` Tool and the `MCSMatFit` Tool. These are introduced in the examples below, detailed reference can be found in the code docstrings. There are two example systems that are used and are provided by reskit. These can be located in the reskit/examples folder; they are the radial well and the pyrazine molecule.

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

# Get the chart Tool
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

# Get the mcsmatfit Tool
sfittool = rk.get_tool(rk.mcsmatfit, dkmat2, "results")

# Perform the calculation of the poles and the qualityindicators
cfins = sfittool.get_elastic_Fins(range(2,32,2))
sfittool.find_stable_Smat_poles(cfins)
```

Again, the "results" argument in the `rk.get_tool` function is the location of an archive into which the results will be stored. There are many more result files generated from this example than for the `Chart`, since there are intermediate calculations. The final results are in the QIs_E.dat and QIs_k.dat files, which list the identified poles (as either Es or ks) and their associated QIs (quality indicators). These files (for the given example) can be found in: ./results/pyrazine/mpmath_100/(0,1200,None)/mcsmatfit/poles/default/[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]. The following intermediate results are generated:
  - Pole convergence tables. In the same folder as the QIs_E.dat and QIs_k.dat files, they are named like dk1e-09.dat, referring to the relative comparison threshold used in the calculation. The user is referred to [stelempy](https://github.com/petersbingham/stelempy) for a description of the tables contained in these files.
  - Root files. These list all of the roots for a given M and can be found in: ./results/pyrazine/mpmath_100/(0,1200,None)/mcsmatfit/roots/default. See [parsmat](https://github.com/petersbingham/parsmat) and [matfuncutil](https://github.com/petersbingham/matfuncutil) for further details.
  - Coefficient dirs. These contain the coefficients for a given M and can be found in: ./results/pyrazine/mpmath_100/(0,1200,None)/mcsmatfit/coeffs/default. See [parsmat](https://github.com/petersbingham/parsmat) for further details.

## Contributing

Contributions are welcome. Please see [CONTRIBUTING.md](https://github.com/petersbingham/reskit/blob/master/CONTRIBUTING.md) for guidelines.
