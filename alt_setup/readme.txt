To install:
- Unzip.
- Consult reskit/README.md for installation instructions.
- Following installation consult reskit/examples/readme.txt for
  instructions on running the example code.

Description of Directories and Files.

reskit/README.md                   - Main readme in markdown format (for GitHub
                                     display). Contains installation and usage
                                     instructions.

reskit/CONTRIBUTING.md             - Documentation outlining instructions for
                                     contributing to the reskit code base.

reskit/TROUBLESHOOTING.md           - Documentation outlining hints for
                                      resolving known issues.

reskit/setup.py                    - Installation script. See reskit/README.md.

reskit/requirements.txt            - List of third party dependencies and
                                     versions to be used during installation.

reskit/reskit.vpp                  - reskit visual paradigm project.
                                     
reskit/reskit.jpg                  - reskit design diagram created using vpp
                                     file.

reskit/examples                    - Scripts to generate results from the
                                     provided test data.
    /readme.txt                    - Instructions for running the example test
                                     data.
    /reskit_examples.py            - Python script containing the example code.
    /kmatrix_input_pyrazine.txt    - K-matrix data for the pyrazine example.
    /kmatrix_input_uracil.txt      - K-matrix data for the uracil example.
    /*.yaml                        - Configurations used in the examples
                                     calculations.
    /author-results                - Results obtained by authors using example
                                     code and data.

reskit/reskit                      - This is the installable reskit package 
                                     folder.
    /doc                           - Python scripts for creating documentation
                                     from the numpy-style docstrings.
    /tools                         - The tools used by reskit.
        /chart                     - Contains python module and default
                                     configuration for the chart Tool.
        /mcsmatfit                 - Contains python module and default
                                     configuration for the mcsmatfit Tool.
        /toolhelper.py             - Generic Tool code.
    /tests                         - Folder containing automated tests.
        /run_tests.sh              - Bash script to run the automated tests.
        /*.py                      - Python files containing tests for
                                     particular functionalities.
    /utilities                     - These contain the reskit utilities as
                                     described in the reskit/README.md doc.

reskit/tests                       - Chart tests and demos.
        /chart_demo.py             - This cycles through all the available chart
                                     types and parameters.
        /chart_Smat_fin_fit.py     - This plots a container returned from the
                                     mcsmatfit Tool using the chart Tool and
                                     saves to a sensible archive location.
