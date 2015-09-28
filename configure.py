#!/usr/bin/env python3
# -*- coding: utf-8 -*-g
import logging
import yaml
from os import chdir, listdir, mkdir, path, remove
from shutil import move
import subprocess
import argparse


def main():
    absBase = path.dirname(path.abspath(__file__))
    # Options parser.
    prs = argparse.ArgumentParser(description='Setup directories and compile\
                                               subroutines for the cascading\
                                               detection meta-algorithm.')
    prs.add_argument('-c', '--configuration', type=str, dest='confPath',
                     default=path.join(absBase, "conf/configuration.yml"),
                     help='Relative path of the global configuration file.')
    prs.add_argument('-n', '--no_compile', action='store_true',
                     help='Do not compile subroutines.')
    args = prs.parse_args()

    # Load the script configuration.
    conf = yaml.load(open(args.confPath).read())

    # Initialize logging.
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(levelname)s] %(asctime)s : %(message)s',
                        datefmt='%d-%m-%y %H:%M:%S')
    log = logging.getLogger("setup")

    # Create temporary and result.
    log.info("Setup the temporary directory: " + conf['temporary_dir'] + ".")
    try:
        mkdir(conf['temporary_dir'], 0o755)
        log.info(conf['temporary_dir'] + " created with 755 privilege.")
    except OSError:
        log.info(conf['temporary_dir'] + " already exists.")
        pass
    log.info("Setup the cluster directory: " + conf['result_dir'] + ".")
    try:
        mkdir(conf['result_dir'], 0o755)
        log.info(conf['result_dir'] + " created with 755 privilege.")
    except OSError:
        log.info(conf['result_dir'] + " already exists.")
        pass

    # Compile cpp subroutines.
    if not args.no_compile:
        # GCE
        bpth = path.join(absBase, "cdtools", "GCE", "src", "build")
        try:
            compilerCall = ["make"]
            log.info("Compiling: " + str(compilerCall) + "(GCE)")
            log.info("Entering " + bpth)
            chdir(bpth)
            returnVal = subprocess.check_call(compilerCall)
            move(path.join(bpth, "GCECommunityFinder"),
                 path.join(absBase, "cdtools", "GCE", "bin", "GCE"))
            log.info("Exit value: " + str(returnVal))
        except subprocess.CalledProcessError as exc:
            log.error("Compiler error!")
            log.error(exc)
            pass
        finally:
            log.info("Cleaning up.")
            dellist = [path.join(bpth, x) for x in listdir(bpth)]
            dellist.remove(path.join(bpth, "makefile"))
            for f in dellist:
                remove(f)
            log.info("Entering " + absBase)
            chdir(absBase)
        # LCA
        bpth = path.join(absBase, "cdtools", "LCA")
        try:
            compilerCall = [conf["cpp_compiler"],
                            conf["compiler_flag"],
                            path.join(bpth, "src/calcAndWrite_Jaccards.cpp"),
                            "-o", path.join(bpth, "bin/LCA_calc")]
            log.info("Compiling: " + str(compilerCall))
            returnVal = subprocess.check_call(compilerCall)
            log.info("Exit value: " + str(returnVal))
        except subprocess.CalledProcessError as exc:
            log.error("Compiler error!")
            log.error(exc)
            pass
        try:
            compilerCall = [conf["cpp_compiler"],
                            conf["compiler_flag"],
                            path.join(bpth, "src/clusterJaccsFile.cpp"),
                            "-o", path.join(bpth, "bin/LCA_cluster")]
            log.info("Compiling: " + str(compilerCall))
            returnVal = subprocess.check_call(compilerCall)
            log.info("Exit value: " + str(returnVal))
        except subprocess.CalledProcessError as exc:
            log.error("Compiler error!")
            log.error(exc)
            pass

if __name__ == "__main__":
    main()
