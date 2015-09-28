#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cdtools as cdt
import cdtools.CPA as algoCPA
import cdtools.GCE as algoGCE
import cdtools.LCA as algoLCA
from os import path, remove
from shutil import copyfile, move
import argparse
import logging
import yaml
import time



def main():
    absBase = path.dirname(path.abspath(__file__))
    # Options parser.
    prs = argparse.ArgumentParser(description='Apply a detection algorithm\
                                               iteratively, removes detected\
                                               edges, and continues until a\
                                               predetermined spareness\
                                               condition is reached.')
    prs.add_argument('-e', '--edge_list_path', type=str, dest='edgeListPath',
                     required=True, help='Path of an edge list file.')
    prs.add_argument('-o', '--output_directory', type=str, dest='outputDir',
                     required=True, help='Name of the base output directory.')
    prs.add_argument('-a', '--algo', type=str, dest='algorithm', default="LCA",
                     required=True,
                     help='Set the detection aglorithm (LCA, CPA, GCE).')
    prs.add_argument('-l', '--log', type=str, dest='logPath',
                     default="cascading.log", help='Log file path.')
    prs.add_argument('--chrono', '-C', dest='chrono', action='store_true',
                     help='Output timestamps, in ms.')
    prs.add_argument('--verbose', '-v', dest='verbose', action='store_true',
                     help='Show the output of the detection subroutines.')
    prs.add_argument('-u', '--unique_id', type=str, dest='uniqueId',
                     default="tmp",
                     help="Unique identifier that is appended to temporary\
                           files paths. Reduces collisions when multiple\
                           instances of cascading_detection are running\
                           concurrently on the same machine.")
    prs.add_argument('-c', '--configuration', type=str, dest='confPath',
                     default=path.join(absBase, "conf/configuration.yml"),
                     help='Relative path of the global configuration file.')
    args = prs.parse_args()

    # Load the script configuration.
    conf = yaml.load(open(args.confPath).read())
    logging.basicConfig(filename=args.logPath, level=logging.DEBUG,
                        format='[%(levelname)s] %(asctime)s: %(message)s',
                        datefmt='%H:%M:%S %d-%m-%y')
    log = logging.getLogger("cascading_logger")

    # Log options and configuration.
    log.info('---------------------------------------------------------------')
    log.info('Starting the cascading_detection.py script.')
    log.info(args.confPath + ' content:')
    log.info('    temporary_dir : ' + conf['temporary_dir'])
    log.info('    result_dir : ' + conf['result_dir'])
    log.info('argparse content:')
    log.info('    --edge_list_path : ' + args.edgeListPath)
    log.info('    --output_directory : ' + args.outputDir)
    log.info('    --algo : ' + args.algorithm)
    log.info('    --log : ' + args.logPath)
    log.info('    --unique_id : ' + args.uniqueId)
    log.info('---------------------------------------------------------------')

    # Assign abstract variables base upon the selected algorithm.
    if  args.algorithm == 'CPA':
        baseOutputPath = path.join(conf['result_dir'], args.outputDir, "CPA")
        cdt.PreparePaths(baseOutputPath)
        minSize = 2
        Detect = algoCPA.Detect
    elif args.algorithm == 'GCE':
        baseOutputPath = path.join(conf['result_dir'], args.outputDir, "GCE")
        cdt.PreparePaths(baseOutputPath)
        minSize = 2
        Detect = algoGCE.Detect
    elif args.algorithm == 'LCA':
        baseOutputPath = path.join(conf['result_dir'], args.outputDir, "LCA")
        cdt.PreparePaths(baseOutputPath)
        minSize = 2
        Detect = algoLCA.Detect
    else:
        exit()

    # Preparation of the cascading detection algorithm.
    if args.chrono:
        current_milli_time = lambda: int(round(time.time() * 1000))
    it = 1
    edgeListPath = path.join(baseOutputPath, "edgelists", "it1.dat")
    copyfile(args.edgeListPath, edgeListPath)
    nodesCount = cdt.UniqueCount(edgeListPath)
    edgesCount = cdt.EdgeCount(edgeListPath)
    while True:
        log.info('iteration = ' + str(it))
        # Detect communities, and stop if the sparsity is verified.
        if args.chrono:
            log.info("precise timestamp: " + str(current_milli_time()))
        (tmpClusterPath, tooSparse) = Detect(edgeListPath,
                                             conf['temporary_dir'],
                                             minSize,
                                             nodesCount,
                                             args.uniqueId,
                                             args.verbose)
        if args.chrono:
            log.info("precise timestamp: " + str(current_milli_time()))
        if tooSparse:
            remove(edgeListPath)
            break

        # Obtain the sparsified network (i.e. sparsified edge list)
        sparserEdgeList = cdt.SparsifyEdgeList(edgeListPath, tmpClusterPath)

        # Save state (through file moving => no memory required)
        # Edge clusters file
        fileSuffix = "it" + str(it) + ".dat"
        clustersPath = path.join(baseOutputPath, "clusters", fileSuffix)
        move(tmpClusterPath, clustersPath)
        # Edge list file
        nextFileSuffix = "it" + str(it + 1) + ".dat"
        edgeListPath = path.join(baseOutputPath, "edgelists", nextFileSuffix)
        cdt.SaveSortedList(sparserEdgeList, edgeListPath)

        # Compute and save statistics.
        edgesStatsFile = open(path.join(baseOutputPath,
                                        "statistics",
                                        "edges.dat"), 'a')
        unassigendEdges = cdt.EdgeCount(edgeListPath)
        assignedFraction = (edgesCount - unassigendEdges) / edgesCount
        edgesStatsFile.write(str(it) + " " +
                             str(edgesCount - unassigendEdges) + " " +
                             str(assignedFraction) + " " +
                             str(1 - assignedFraction) + "\n")
        edgesStatsFile.close()

        # Prepare next iteration.
        it += 1

if __name__ == "__main__":
    main()
