# -*- coding: utf-8 -*-
# cdtools -- a python library for cascading community detection on networks
# @author: Jean-Gabriel Young <jean.gabriel.young@gmail.com>
#
# cdtools/GCE/detection.py -- Wraps GCE for cdtools.
import subprocess
import yaml
import logging
from os import devnull, remove, path
from ..generic import PurgeClusters, ToEdgeClusters
from ..statistics import EdgeCount
from ..utilities import drange

def Detect(edgeListPath, tmpDirectory, minSize,
           nwSize=0, uniqueId="tmp", verbose=False):
    '''
        Interface of the GCE algorithm. Some useless parameters are present
        for polymorphism purposes.
    '''
    log = logging.getLogger("cascading_logger")

    # GCE configurations.
    configurationFile = path.join(path.dirname(__file__), "GCE_conf.yml")
    conf = yaml.load(open(configurationFile).read())
    k = conf['k']
    critical_overlap = conf['critical_overlap']
    sufficient_cover = conf['sufficient_cover']

    delete_list = []
    tooSparse = True
    while k > 2:
        alpha = conf['alpha']
        # Detect
        errorstream = path.join(tmpDirectory,
                                uniqueId  + str(k) + "_gce_err.txt")
        while IncreaseAlpha(errorstream):
            GCE(edgeListPath, tmpDirectory, uniqueId + str(k),
                verbose, k, critical_overlap, sufficient_cover, alpha)
            alpha += 0.1
        remove(errorstream)
        clustersPath = path.join(tmpDirectory,
                                 uniqueId  + str(k) + "_gce_out.txt")
        if NoCommunities(clustersPath):
            delete_list.append(clustersPath)
            k -= 1
        else:
            log.info("GCE.Detect(): Dense enough. Proceeding.")
            log.info("GCE.Detect(): k=" + str(k))
            log.info("GCE.Detect(): g=" + str(EdgeCount(clustersPath)))
            # Found communities, pre-process
            ToEdgeClusters(edgeListPath, clustersPath)
            PurgeClusters(clustersPath, minSize)
            tooSparse = False
            break
    # Cleanup and exit
    for f in delete_list:
        remove(f)
    if tooSparse:
        log.info("GCE.Detect(): Too sparse. Rejecting.")
    return clustersPath, tooSparse


def GCE(edgeListPath, tmpDirectory, uniqueId, verbose,
        basic_clique_size, critical_overlap, sufficient_cover, alpha):
    ''' Apply GCE using a java subroutine. '''
    try:
        nullstream = open(devnull, 'w')
        absPath = path.dirname(path.abspath(__file__))
        output = open(path.join(tmpDirectory, uniqueId + "_gce_out.txt"), 'w')
        errrorstream = open(path.join(tmpDirectory, uniqueId + "_gce_err.txt"), 'w')
        gce_call = [path.join(absPath, "bin", "GCE"),
                    edgeListPath,
                    str(basic_clique_size),
                    str(critical_overlap),
                    str(alpha),
                    str(sufficient_cover)]
        subprocess.check_call(gce_call, stdout=output, stderr=errrorstream)
        errrorstream.close()
        if verbose:
            errrorstream =  open(path.join(tmpDirectory, uniqueId + "_gce_err.txt"), 'r')
            for l in errrorstream:
                print(l.strip())
    except subprocess.CalledProcessError:
        pass
    finally:
        nullstream.close()
        output.close()
        errrorstream.close()


def NoCommunities(clusterPath):
    try:
        with open(clusterPath, 'r') as f:
            for l in f:
                if len(l.strip().split()) > 1:
                    return False
        return True
    except IOError:
        return True


def IncreaseAlpha(errorstream):
    if path.exists(errorstream):
        with open(errorstream,'r') as f:
            for l in f:
                if l.find("Warning: size of growing communities exceeds probable size:") == 0:
                    return True
            return False
    return True
