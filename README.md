# Lumerical Monte-Carlo simulation helper scripts
Helper scripts to generate Monte-Carlo simulations and analyse them for Lumerical FDTD.
# Instructions
There are two scripts: _monte_result.py_ and _monte_generator.py_. There is also an additional file _config.ini_. Most important note is make sure that all of these files remain in the same directory. Then the next important thing is the dependencies for these scripts. You need the following libraries to use these scripts:

- numpy;
- matplotlib;
- shapely;
- pandas;
- geopandas.

Numpy and matplotlib you most likely will have already. The others can be installed with pip: `pip install shapely pandas geopandas`. Once these preliminary steps are done, the scripts should work.

The _monte_result.py_ script is the one that collects the results from Monte-Carlo simulations and _monte_generator.py_ is the script that generates the simulation files. The _config.ini_ file is separated in to three sections: _COMMON_, _MONTE_GENERATION_ and _MONTE_ANALYSIS_. The _COMMON_ section sets parameters that are common for both scripts. The other two set parameters to their corresponding scripts.

To run the _monte_result.py_ script, first place your Monte-Carlo simulation files in some directory and make sure they are named something like _name_{number}.py_ (most important is that a number follows the underscore). Then open the config file and set filepath parameter to the directory where the simulation files are kept in. Then set the output file path and name if you would like and run the script.

To run the _monte_generator.py_ script, first you will need an already set up simulation file with a source, structure, monitors and etc. After that set the filepath for where the base structure simulation file is located. Then set up the various parameters that are described in the comments of the config file and then you can run the script. Once you run the script, a plot window will show up showing where your random points will be located. If you want the script to continue to generate the files, close the plot window and it will. If this is unnecessary, line 84 can be commented out.
