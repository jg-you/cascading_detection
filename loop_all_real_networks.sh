#!/usr/bin/bash
#
# Execute the cascading_detection.py program on all the real networks edge lists.
# Arguments:
#    argv[1] : the name of the algorithm (CPA/LCA/GCE).
# 
# Example usage:
#    ./loop_all_real_networks.sh GCE
#
# NOTE: Configure the program correctly before running this script! 
#       Rename and edit conf/example_configuration.yml, then run configure.py.
# 
# Author: JG Young
base_log=./
algorithm=$1

echo "Running cascading on arXiv.txt"
python cascading_detection.py -e edgelists/arXiv.txt      -o arXiv      -a $algorithm -l $base_log"/arXiv_"$algorithm".log"       --chrono   -c conf/configuration.yml
echo "Running cascading on Email.txt"
python cascading_detection.py -e edgelists/Email.txt      -o Email      -a $algorithm -l $base_log"/Email_"$algorithm".log"       --chrono   -c conf/configuration.yml
echo "Running cascading on Gnutella.txt"
python cascading_detection.py -e edgelists/Gnutella.txt   -o Gnutella   -a $algorithm -l $base_log"/Gnutella_"$algorithm".log"    --chrono   -c conf/configuration.yml
echo "Running cascading on Internet.txt"
python cascading_detection.py -e edgelists/Internet.txt   -o Internet   -a $algorithm -l $base_log"/Internet_"$algorithm".log"    --chrono   -c conf/configuration.yml
echo "Running cascading on PGP.txt"
python cascading_detection.py -e edgelists/PGP.txt        -o PGP        -a $algorithm -l $base_log"/PGP_"$algorithm".log"         --chrono   -c conf/configuration.yml
echo "Running cascading on Power.txt"
python cascading_detection.py -e edgelists/Power.txt      -o Power      -a $algorithm -l $base_log"/Power_"$algorithm".log"       --chrono   -c conf/configuration.yml
echo "Running cascading on Protein.txt"
python cascading_detection.py -e edgelists/Protein.txt    -o Protein    -a $algorithm -l $base_log"/Protein_"$algorithm".log"     --chrono   -c conf/configuration.yml
echo "Running cascading on Words.txt"
python cascading_detection.py -e edgelists/Words.txt      -o Words      -a $algorithm -l $base_log"/Words_"$algorithm".log"       --chrono   -c conf/configuration.yml
