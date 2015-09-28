// calcAndWrite_Jaccards.cpp
// Jim Bagrow
// Last Modified: 2014-12-06

/*
Copyright 2008-2014 James Bagrow


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


// USAGE:
//      g++ -O3 -o calc calcAndWrite_Jaccards.cpp
//      ./calc network.pairs network.jaccs
//
//  -- network.pairs is an integer edgelist (one edge, two nodes
//  per line)
//  -- network.jaccs will contain the jaccard coefficient for each
//  pair of edges compared, of the form:
//      i_0 i_1 j_0 j_1 jaccard<newline>
//      ...
//  for edges (i_0,i_1) and (j_0,j_1)


// same as calcAndWrite_Jaccards.cpp, but without the graph code...
// but not much quicker (:-()

// all this does is calculate the jaccard for "each" edge pair and
// write it to a file.  Two make this into real code will take some
// more work (the next step can be the hierarchical clustering over
// the output jacc file...)

// CORRECTNESS:
//  Returns same jaccard file as calcAndWrite_Jaccards.cpp, as shown
//  by compareTwoJaccs.py...

#include <fstream>
#include <iostream>
#include <set>
#include <map>
#include <utility> // pairs
#include <vector>
#include <algorithm> // for swap
using namespace std;


// "custom" (cppreference.com) std::next implementation (unavailable in c++98)
template<class ForwardIt>
ForwardIt next(ForwardIt it, typename std::iterator_traits<ForwardIt>::difference_type n = 1)
{
    std::advance(it, n);
    return it;
}

int intersection_size( const set<int> &A, const set<int> &B ) {
    // only get number of elements, don't build a new set
    // this assumes the sets are ordered, which std::sets are!
    int num = 0;
    set<int>::const_iterator As = A.begin(), Af = A.end(),
                             Bs = B.begin(), Bf = B.end();
    while ( As != Af && Bs != Bf ) {
        if ( *As < *Bs) {
            ++As;
        } else if ( *Bs < *As ) {
            ++Bs;
        } else {
            ++num;
            ++As;
            ++Bs;
        }
    }
    return num;
}

int main (int argc, char const *argv[]){
    // make sure args are present:
    if (!argv[1]){
        cerr << "ERROR: no input file specified" << endl;
        cerr << "usage:\n    " << argv[0] << " input.pairs output.jaccs" << endl;
        exit(1);
    }
    if (!argv[2]){
        cerr << "ERROR: no output file specified" << endl;
        cerr << "usage:\n    " << argv[0] << " input.pairs output.jaccs" << endl;
        exit(1);
    }


    // load edgelist into two arrays, and into an array of sets:
    ifstream inFile;
    inFile.open (argv[1]);
    if (!inFile) {
        cerr << "ERROR: unable to open input file" << endl;
        exit(1); // terminate with error
    }

    // scan edgelist once to build the node to idx dictionary
    // will determine num_nodes at the same time
    int ni,nj, nodeCtr = 0;
    map<int, int> node2idx;
    while (inFile >> ni >> nj){
        if (node2idx.count(ni) == 0) { 
            node2idx[ni] = nodeCtr;
            ++nodeCtr;
        }
        if (node2idx.count(nj) == 0) { 
            node2idx[nj] = nodeCtr;
            ++nodeCtr;
        }
    }
    int num_nodes = node2idx.size();
    inFile.close();
    
    vector< set<int> > neighbors(num_nodes);
    inFile.open( argv[1] );
    while (inFile >> ni >> nj){ // rescan edgelist to populate 
        neighbors[node2idx[ni]].insert(nj);
        neighbors[node2idx[nj]].insert(ni); // undirected
    }
    for (map<int, int>::iterator it = node2idx.begin(); it!=node2idx.end();++it) {
        neighbors[it->second].insert(it->first); // neighbors[] is now INCLUSIVE!
    }
    inFile.close();
    // end load edgelist


    // do the gosh darn calculation, fool!
    FILE * jaccFile = fopen(argv[2],"w");
    double curr_jacc, intersection;
    set<int>::iterator i, j, t;
    for (map<int, int>::iterator keystoneIt = node2idx.begin(); keystoneIt != node2idx.end(); ++keystoneIt) { // loop over keystones
        int keystone = keystoneIt->first;
        int keystoneIdx = keystoneIt->second;
        for (i = neighbors[keystoneIdx].begin(); i != neighbors[keystoneIdx].end(); i++) { // neighbors of keystone
            if (*i == keystone)
                continue;

            for (j = next(i); j != neighbors[keystoneIdx].end(); ++j ) { // neighbors of keystone (for pair-wise comparison with i)
                if (*j == keystone)
                    continue;
                
                intersection = (double) intersection_size( neighbors[node2idx[*i]], neighbors[node2idx[*j]]);    // my set intersection function
                curr_jacc = intersection / (double)( neighbors[node2idx[*i]].size() + neighbors[node2idx[*j]].size() - intersection );

                if (keystone < *i && keystone < *j) {
                    fprintf( jaccFile, "%i\t%i\t%i\t%i\t%f\n", keystone, *i, keystone, *j, curr_jacc );
                } else if (keystone < *i && keystone > *j){
                    fprintf( jaccFile, "%i\t%i\t%i\t%i\t%f\n", keystone, *i, *j, keystone, curr_jacc );
                } else if (keystone > *i && keystone < *j){
                    fprintf( jaccFile, "%i\t%i\t%i\t%i\t%f\n", *i, keystone, keystone, *j, curr_jacc );
                } else {
                    fprintf( jaccFile, "%i\t%i\t%i\t%i\t%f\n", *i, keystone, *j, keystone, curr_jacc );
                }
            }
        }
    } // done loop over keystones
    fclose(jaccFile);
    return 0;
}
