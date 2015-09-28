# Cascading Detection
[![DOI](https://zenodo.org/badge/18575/jg-you/cascading_detection.svg)](https://zenodo.org/badge/latestdoi/18575/jg-you/cascading_detection)

Python 3 implementation of the cascading detection algorithm presented in 

[Unveiling Hidden Communities Through Cascading Detection on Network Structures](http://arxiv.org/abs/1211.1364)

Jean-Gabriel Young, Antoine Allard, Laurent Hébert-Dufresne, Louis J. Dubé


## Usage
First time user should setup the output directories and compile detection algorithm binaries.
A python script is provided for convenience:

    python configure.py -c path/to/configuration.yml

`cascading_detection` is not configured by default, and a `configuration.yml` file should therefore be created first.
The repository contains an example configuration file (see [conf/example_configuration.yml](conf/example_configuration.yml)).

    temporary_dir : "/home/USER/WORKING_DIR/"
    result_dir : "/home/USER/WORKING_DIR/RESULTS"
    cpp_compiler : "g++"
    compiler_flag : "-o3"

* `temporary_dir` is the working directory. 
It will hold intermediate result files that will be deleted if the program exits cleanly.
Manual cleanup may be required if an early termination signal is received.
* `result_dir` is the base directory to which results will be outputted.
* `cpp_compiler` and `compiler_flag` allows for compiler and compiler options changes.

The program

    python cascading_detection.py -e EDGE_LIST -o BASE -a AGLO

can then run out of the box.

* `BASE` defines the output directory. The complete path is $result_dir/BASE. $result_dir should be set in `configuration.yml`.
* `ALGO` is the name of the algorithm that will be applied iteratively. Currently, only `CPA`, `GCE` and `LCA` are supported.
* `EDGE_LIST` is a text file containing an undirected edge list.

We use a simple format for edge lists, namely not necessarily contiguous integers, delimited by any whitespace, e.g.


    2 4
    3 2
    3 7
    1 4
    ...

Some examples are provided in the [edgelist/](edgelist/) directory.


Three additional flags are also provided:

* `-l` (optional) sets the log file path. It is defaulted to `cascading.log` in the current working directory.
* `-u` (optional) sets a unique ID which is appended to the path of temporary files. This prevents file name collisions when multiple instance of  `cascading_detection.py` are running concurrently. 
* `-C` (optional) indicates that millisecond precision timing is necessary (for benchmark purposes). Running time information will appear in the logfile.


## Important notes

* Algorithms are applied as prescribed by the original authors, but parameters can be tweaked by modifying the configuration files in sub-module directories (e.g. [cdtools/LCA/LCA_conf.yml](cdtools/LCA/LCA_conf.yml))
* Edges *must* only appear once (e.g. `EDGE_LIST` must not contain a link and its inverse).
* `ALGO` should be one of the following supported algorithm: `CPA`, `LCA`, or `GCE`.
* 32 bit and 64 bit CFinder binaries are both provided. Configure the algorithm  accordingly in [cdtools/CPA/CPA_conf.yml](cdtools/CPA/CPA_conf.yml) (defaulted to 64).


## License
`cascading_detection` is distributed under the [MIT License](COPYING) except for submodules, which are distributed under their original licences (see  [COPYING](COPYING) for more details).

CFinder requires a non-profit license to operate properly.
It is *not* provided with `cascading_detection` for obvious reasons.
Please obtain a license from [CFinder@hal.elte.hu](CFinder@hal.elte.hu) and configure  [cdtools/CPA/CPA_conf.yml](cdtools/CPA/CPA_conf.yml) accordingly.

## Closing note

This software is designed with extensibility in mind.
Feel free to add support for new algorithms by creating sub-modules in the the cdtools package.
