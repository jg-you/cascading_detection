# -*- coding: utf-8 -*-
# cdtools -- a python library for cascading community detection on networks
# @author: Jean-Gabriel Young <jean.gabriel.young@gmail.com>
#
# cdtools/LCA/detection.py -- Wraps the clique percolation algo for cdtools.
import subprocess
import locale
import yaml
import logging
from os import path, remove
from ..utilities import DeleteCommas, drange
from ..generic import PurgeClusters


def Detect(edgeListPath, tmpDirectory, minSize,
           nwSize=0, uniqueId="tmp", verbose=False):
    '''
        Interface of the LCA algorithm.
        "nwSize" is useless but kept for polymorphism purposes.
    '''

    log = logging.getLogger("cascading_logger")

    # LCA configurations.
    configurationFile = path.join(path.dirname(__file__), "LCA_conf.yml")
    conf = yaml.load(open(configurationFile).read())
    T_increment = conf['threshold_increments']
    min_T = conf['min_threshold']
    max_T = conf['max_threshold']
    ignoreSingleton = conf["ignore_singleton"]

    # Compute Jaccard coefficients.
    CalcJaccards(edgeListPath, tmpDirectory, uniqueId)

    # Identify maximal density.
    optimal_T = min_T
    optimal_D = 0
    optimalClustersPath = ""
    discardList = []
    for T in drange(min_T, max_T, T_increment):
        D, clustersPath = Cluster(T, edgeListPath, tmpDirectory,
                                  uniqueId, ignoreSingleton)
        if D > optimal_D:
            optimal_D = D
            optimal_T = T
            discardList.append(optimalClustersPath)
            optimalClustersPath = clustersPath
        else:
            discardList.append(clustersPath)

    # Determine if further detection should be applied:
    log.info("optimal_T=" + str(optimal_T) + " optimal_D=" + str(optimal_D))
    if optimal_T == min_T and optimal_D < 1:
        log.info("LCA.Detect(): Too sparse. Rejecting.")
        tooSparse = True
        discardList.append(optimalClustersPath)
    else:
        log.info("LCA.Detect(): Dense enough. Proceeding.")
        tooSparse = False
        DeleteCommas(optimalClustersPath)
        PurgeClusters(optimalClustersPath, minSize)

    # Cleanup: remove unused files (more portable than writing to /dev/null).
    discardList.append(path.join(tmpDirectory, uniqueId + ".stats"))
    discardList.append(path.join(tmpDirectory, uniqueId + ".jaccs"))
    Cleanup(discardList)

    return optimalClustersPath, tooSparse


def CalcJaccards(edgeListPath, tmpDirectory, uniqueId):
    ''' Comupte jaccards coefficients using a C++ subroutine. '''

    log = logging.getLogger("cascading_logger")

    try:
        absPath = path.dirname(path.abspath(__file__))
        calcJaccCall = [path.join(absPath, "bin", "LCA_calc"),
                        edgeListPath,
                        path.join(tmpDirectory, uniqueId + ".jaccs")]
        subprocess.check_call(calcJaccCall)
    except subprocess.CalledProcessError:
        log.error("Unexpected error with ", calcJaccCall)


def Cluster(T, edgeListPath, tmpDirectory, uniqueId, ignoreSingleton):
    ''' Cluster edges that are more similar than a threshold value together.'''

    log = logging.getLogger("cascading_logger")

    T_str = str(T).replace(".", "_")  # Underscores are safer than "_".
    fileJacc = path.join(tmpDirectory, uniqueId + ".jaccs")
    fileClus = path.join(tmpDirectory, T_str + uniqueId + ".dat")
    fileStat = path.join(tmpDirectory, uniqueId + ".stats")
    # Cluster edges call
    absPath = path.dirname(path.abspath(__file__))
    clusterCall = [path.join(absPath, "bin", "LCA_cluster"),
                   edgeListPath, fileJacc, fileClus, fileStat, str(T)]
    try:
        # Execute clustering function
        proc = subprocess.Popen(clusterCall, stdout=subprocess.PIPE)
        # Fetch density from stdout (WILL break on LCA_cluster API change)
        #
        # NOTE: This fragile API forces one to read and strip a  specific line
        # of the stdout. The density of the partition is found on line 2,
        # formatted as:
        #     D = FLOAT_VALUE
        # whereas it is found on line 4 if one does not consider singletons.
        if ignoreSingleton:
            D_lineNo = 4
        else:
            D_lineNo = 2
        proc_out, proc_err = proc.communicate()
        encodingLocale = None
        try:
            encodingLocale = locale.getdefaultlocale()[1]
        except:
            pass
        if encodingLocale is None:
            encodingLocale = 'UTF-8'
        tmp = proc_out.decode(encodingLocale).split("\n")
        current_D = float(tmp[D_lineNo].replace(" ", "").replace("D=", ""))

    except subprocess.CalledProcessError:
        log.error("Unexpected error with ", clusterCall)

    return current_D, fileClus


def Cleanup(discardList):
    ''' Cleanup temporary files after the detection algorithm is done.'''
    for f in discardList:
        try:
            remove(f)
        except:
            pass
