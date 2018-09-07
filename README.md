# reskit
Python Package to assist with the identification and characterisation of quantum scattering resonances.

TROUBLESHOOTING: If you encounter any issues with reskit please consult the [TROUBLESHOOTING.md](https://github.com/petersbingham/reskit/blob/master/TROUBLESHOOTING.md). If these are due to a bug please leave an issue report in github.

## Getting reskit

Git clone the repository with the following command:

    git clone https://github.com/petersbingham/reskit

## Dependencies

Currently reskit only supports python 2.7 (tested on 2.7.15). If you are using Linux and have no root access see here for installing a specific version of python into your user space: http://thelazylog.com/install-python-as-local-user-on-linux/

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

We recommend using the specific versions of these dependencies as indicated in the [requirements.txt](https://github.com/petersbingham/reskit/blob/master/requirements.txt), especially for the third party packages. If you wish to try your luck with later versions of the utilities you should should check the version number for any compatibility breaks (the utilities use [SemVer](http://semver.org/)). Note that some distributions of reskit come with the utilities already installed.

If you plan to install the recommended versions of the dependencies you may not want to override those that already exist in your global python distribution. If this is the case we recommend setting up a virtual environment.either using the virtualenv tool or, if using an anaconda distribution, the `conda create` command. 

### Installing Dependencies

There are three options here, refer to the corresponding section further below depending on your installation preference:

1. Install into a virtual environment using Anaconda.
2. Install into a virtual environment with a standalone python installation.
3. Install into your global python space.

Again, if you encounter problems please see [TROUBLESHOOTING.md](https://github.com/petersbingham/reskit/blob/master/TROUBLESHOOTING.md).

#### 1. Install into a virtual environment using Anaconda.

Assuming that you have anaconda correctly installed and that you are in the same directory where you did the git clone set up the local virtual environment with the following commands:

    cd reskit
    conda create -n env python=2.7.15 -y

You now need to activate your virtual environment. On Windows Powershell type:

    activate env

On Linux type:

    conda activate env  # or source activate env

With the virtual environment activated then install the dependencies with the following commands:

    conda install --file requirements.txt -y
    python setup.py install
    
Note that Anaconda will by default still search in the global python user sites when running the virtual environment, which could be a problem if you have different versions of the dependencies in these locations. To remove this behaviour you need to set an environment variable on each reskit session.  On Windows Powershell type:

    set PYTHONNOUSERSITE=1

On Linux type:

    export PYTHONNOUSERSITE=1

#### 2. Install into a virtual environment with a standalone python installation.

virtualenv sets up an entire python distribution in a local directory, into which can be installed dependency versions specific to your project requirements.

virtualenv is a tool, which you can install (if not already installed) with the following command (if you don't have root access add '--user' to the end of the command to install into your home):

    pip install virtualenv

Once installed and assuming that you are in the same directory where you did the git clone set up the local virtualenv with the following commands:

    cd reskit
    virtualenv env

You now need to run a virtualenv activate script to setup your path to use this local version of python. On Windows Powershell type:

    env/Scripts/activate

On Linux type:

    source env/bin/activate

With the virtual environment activated then install the dependencies with the following commands:

    pip install -r requirements.txt
    python setup.py install

#### 3. Install into your global python space.

Assuming that you are in the same directory where you did the git clone install with the following commands (if you don't have root access on Linux you can install into your user space by adding `--user` to the end of both commands below):

    cd reskit
    pip install -r requirements.txt
    python setup.py install

## Running reskit

### Using the reskit API

If you are using a virtual environment ensure that you have activated using the instructions given in the Setting up a virtual environment section above. From the command line type:

    python  # will start the python interpreter
    import reskit as rk

You can now interact with the reskit API. See the examples given below or function docstrings for further details.

### Running the examples

Example reskit calculations for the radial well and the pyrazine and uracil molecules can be found in the examples folder. Refer to the 
readme.txt in this folder for further details. Again, if you are using a virtual environment ensure that you have activated before running these examples.

## Overview

Reskit was designed with the following features in mind:
  - Easily extendable. Different techniques for location and characterisation of quantum resonances can be implemented and added as reskit Tools.
  - Tidy parameter specification. Often calculations have extensive parameters and it can be messy to pass all of these in as function arguments. Reskit provides two levels of parametrisation:
    - High level parameters as function arguments.
    - Low level (and/or advanced) parameters specified in yaml files. The software will provide defaults for these in a default.yaml. If the user wishes to override they can create their own .yaml and pass the path to this to the reskit API.
  - Smart archiving of results. Reskit takes a path to an archive into which all calculations will be written, along with their parameters. This provides a high level of traceability, easy reproduction and reuse of previously acquired intermediate results.
  - Type abstraction. Reskit supports both standard python types (using the numpy package) and arbitrary precision mpmath types.
  - Support for data in both continuous and discrete forms. For example, S-matrix data can be provided as both a discrete set of data or as a function reference to some analytical expression.

As such the reskit interface is fairly generic, providing the following functions (see doc strings for details and parameter descriptions):
  - `get_asym_calc`: Returns a calculator (`AsymCalc`) containing all of the channel information for the scattering system.
  - `get_dmat_from_discrete`: Initialises a reskit container from a discrete set of data and an `AsymCalc`. The data can be K, S or T matrices.
  - `get_dmat_from_continuous`: Initialises a reskit container from a function reference. The function reference will map an energy argument to either a K, S or T matrix.
  - `get_tool`: Returns a Tool using the reskit container returned from `get_dmat_from_discrete` or `get_dmat_from_continuous`. A Tool is typically an implementation of a technique for the location and characterisation of resonances.
  - `use_python_types`: Specifies to use python types with numpy operations.
  - `use_mpmath_types`: Specifies to use mpmath types and operations. The dps can be provided as argument.

![reskit design](https://github.com/petersbingham/reskit/blob/master/reskit.jpg)

## Tools

Reskit currently has two Tools, the `Chart` Tool and the `MCSMatFit` Tool. These are introduced in the examples below, detailed reference can be found in the code docstrings. There are three example systems that are used and are provided by reskit. These can be located in the reskit/examples folder; they are the radial well and the pyrazine and uracil molecules.

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

The `MCSMatFit` Tool is based on the technique described in "S.A. Rakityansky P.O.G. Ogunbade. S-matrix parametrization as a way of locating quantum resonances and bound states: multichannel case, 2010". In essence, it provides a rational S-matrix from a set of discrete S-matrix values along the real energy axis. The poles of the S-matrix can then be located by looking for the stable roots of the denominator. It uses the packages [parsmat](https://github.com/petersbingham/parsmat) and [stelempy](https://github.com/petersbingham/stelempy); additional documentation can be found in the README.mds included in these packages.  

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

# Perform the calculation of the poles and the quality indicators
cfins = sfittool.get_elastic_Fins(range(2,32,2))
sfittool.find_stable_Smat_poles(cfins)
```

Again, the "results" argument in the `rk.get_tool` function is the location of an archive into which the results will be stored. There are many more result files generated from this example than for the `Chart`, since there are intermediate calculations. The final results are in the QIs_E.dat and QIs_k.dat files, which list the identified poles (as either Es or ks) and their associated QIs (quality indicators). These files (for the given example) can be found in: ./results/pyrazine/mpmath_100/(0,1200,None)/mcsmatfit/poles/default/[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30]. The following intermediate results are generated:
  - Pole convergence tables. In the same folder as the QIs_E.dat and QIs_k.dat files, they are named like dk1e-09.dat, referring to the relative comparison threshold used in the calculation. The user is referred to [stelempy](https://github.com/petersbingham/stelempy) for a description of the tables contained in these files.
  - Root files. These list all of the roots for a given M and can be found in: ./results/pyrazine/mpmath_100/(0,1200,None)/mcsmatfit/roots/default. See [parsmat](https://github.com/petersbingham/parsmat) and [matfuncutil](https://github.com/petersbingham/matfuncutil) for further details.
  - Coefficient dirs. These contain the coefficients for a given M and can be found in: ./results/pyrazine/mpmath_100/(0,1200,None)/mcsmatfit/coeffs/default. See [parsmat](https://github.com/petersbingham/parsmat) for further details.

## Contributing

Contributions are appreciated. If you find yourself having to change the code please considering pushing this to the GitHub master or at least opening an issue. See [CONTRIBUTING.md](https://github.com/petersbingham/reskit/blob/master/CONTRIBUTING.md) for guidelines.
