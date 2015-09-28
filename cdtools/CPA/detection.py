# -*- coding: utf-8 -*-
# cdtools -- a python library for cascading community detection on networks
# @author: Jean-Gabriel Young <jean.gabriel.young@gmail.com>
#
# cdtools/CPA/detection.py -- Wraps the clique percolation method for cdtools.
import subprocess
import yaml
import logging
import copy
from os import devnull, listdir, path, remove
from shutil import move, rmtree


def Detect(edgeListPath, tmpDirectory, minSize,
           nwSize=0, uniqueId="tmp", verbose=False):
    '''
        Interface of the CPA algorithm.
        Here, 'minSize' is useless but is kept for polymorphism purposes.
    '''
    # Contract:
    # - Will identify the best community structure across all values of
    #   parameters.
    # - Will determine whether, the structure if such an organization exists
    #   or if the remaining edges are too sparse / well mixed for further
    #   detection.
    # - If the stop condition is not met:
    #   * Will clean up any temporary files left in tmpDirectory *beside* the
    #     optimal cluster.
    #   * Will return a path to that optimal cluster.
    # - Otherwise:
    #   * Will clean up any temporary files left in tmpDirectory.
    #
    # Final clusters should be whitespaced, undirected, unweighted edge
    # clusters, where each pair appear in the standard ascending pair order.

    log = logging.getLogger("cascading_logger")

    # CPA configurations.
    configurationFile = path.join(path.dirname(__file__), "CPA_conf.yml")
    conf = yaml.load(open(configurationFile).read())
    # Apply CFinder
    CliquePercolation(edgeListPath, tmpDirectory, uniqueId, verbose,
                      conf['search_time'], conf['binary'], conf['license'])

    # Identify the optimal k.
    ratio = float(conf['extensive_component_ratio'])
    (optimal_k, largest, secondLargest) = SelectCliqueSize(tmpDirectory,
                                                           uniqueId,
                                                           ratio)
    if optimal_k > 0:
        log.info("CPA.Detect():" +
                 " ratio=" + str(ratio) +
                 " largest=" + str(largest) +
                 " secondLargest=" + str(secondLargest))
        log.info("CPA.Detect(): optimal_k=" + str(optimal_k))
        log.info("CPA.Detect(): Dense enough. Proceeding.")
        tooSparse = False
        kdir = "k=" + str(optimal_k)
        optimalClustersPath = path.join(tmpDirectory, uniqueId + "clusters")
        move(path.join(tmpDirectory, uniqueId, kdir, "communities_links"),
             optimalClustersPath)
        ProcessCluster(optimalClustersPath)
    else:
        log.info("CPA.Detect(): Too sparse. Rejecting.")
        tooSparse = True
        optimalClustersPath = ""

    # Cleanup
    rmtree(path.join(tmpDirectory, uniqueId))

    return optimalClustersPath, tooSparse


def CliquePercolation(edgeListPath, tmpDirectory, uniqueId, verbose,
                      maxSearchTime, binName, licensePath):
    ''' Apply the clique percolation algorithm for all k, at the same time. '''

    log = logging.getLogger("cascading_logger")

    try:
        absPath = path.dirname(path.abspath(__file__))
        if maxSearchTime < 0:  # unbounded
            kCliqueCall = [path.join(absPath, "bin", binName),
                           "-l", path.join(absPath, licensePath),
                           "-i", edgeListPath,
                           "-o", path.join(tmpDirectory, uniqueId),
                           "-U"]
        else:
            kCliqueCall = [path.join(absPath, "bin", binName),
                           "-l", path.join(absPath, licensePath),
                           "-i", edgeListPath,
                           "-o", path.join(tmpDirectory, uniqueId),
                           "-t", str(maxSearchTime),
                           "-U"]
        if verbose:
            subprocess.check_call(kCliqueCall)
        else:
            nullstream = open(devnull, 'w')
            subprocess.check_call(kCliqueCall,
                                  stdout=nullstream,
                                  stderr=nullstream)
    except subprocess.CalledProcessError:
        log.error("Unexpected error with ", kCliqueCall)


def SelectCliqueSize(tmpDirectory, uniqueId, ratio):
    ''' Find the highest K such that there is no extensive component '''
    selected_k = float('inf')
    basePath = path.join(tmpDirectory, uniqueId)
    outputExists = False
    extensiveForAll = True
    for kDir in listdir(basePath):
        if kDir.startswith('k'):
            outputExists = True
            sizeDistFile = path.join(basePath, kDir, "size_distribution")
            k = int(kDir.split("=")[1])
            try:
                with open(sizeDistFile, 'r') as f:
                    sizeDistribution = ExtractSizeDist(f)
                    if len(sizeDistribution) > 2:
                        tmp = copy.copy(sizeDistribution)
                        largest = max(sizeDistribution)
                        tmp.pop(largest)
                        secondLargest = max(tmp)
                        if largest * ratio < secondLargest and k < selected_k:
                            selected_k = k
                            selectedLargest = largest
                            selectedSecondLargest = secondLargest
                            extensiveForAll = False
            except (OSError, IOError):
                pass
    if outputExists and not extensiveForAll:
        return (selected_k, selectedLargest, selectedSecondLargest)
    else:
        return (-1, 0, 0)


def ExtractSizeDist(f):
    '''
        Extract a size distribution from the corresponding CFinder output file,
        and format is as a dictionary. The key is the size, the value is the
        number of community of that size.
    '''
    content = [x for x in f if not x.startswith("#")]
    RemoveEmptyLine(content)
    sizeDistribution = {}
    for x in content:
        sizeDistribution[int(x.split()[0])] = int(x.split()[1])
    return sizeDistribution


def RemoveEmptyLine(lst):
    ''' Remove all entries of a list of lines which only contains '\n' '''
    for x in range(0, lst.count("\n")):
        lst.remove("\n")


def ProcessCluster(clusterPath):
    ''' Process the output of CFinder to our custom format '''
    with open(clusterPath, 'r') as f:
        for x in range(0, 8):
            f.readline()  # dump the header
        content = f.read().split("\n")
    try:
        remove(clusterPath)
    except:
        pass
    with open(clusterPath, 'w') as f:
        for line in content:
            l = line.split()
            if len(l) <= 1:
                f.write("\n")
            else:
                f.write(l[0] + " " + l[1] + " ")
