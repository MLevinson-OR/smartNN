#!/bin/bash

# SPEC_DIR='/Volumes/Storage/generated_specs/Laura/orig_specs'
# WARP_DIR='/Volumes/Storage/generated_specs/Laura/warp_specs'

# default directories
# SPEC_DIR='/home/smg/zhenzhou/VCTK/data/inter-module/mcep/England/Laura'
# WARP_DIR='/home/smg/zhenzhou/datasets/Laura_warp'


while [ "$1" != "" ]; do
    case $1 in
        --warp_dir )            shift
                                WARP_DIR=$1
                                ;;
        --spec_dir )            shift
                                SPEC_DIR=$1
                                ;; 
        -h | --help )           echo 'options'
                                echo '--spec_dir : directory for spec files'
                                echo '--warp_dir : directory for saving warp files'
                                exit
                                ;;
    esac
    shift
done


if [ ! -d $WARP_DIR ]; then
    echo 'make warp dir' $WARP_DIR
    mkdir $WARP_DIR
fi


files=`ls $SPEC_DIR/*.spec`

for f in $files; do
    f=`basename $f`
    echo 'warping: ' $f
    x2x +ff $SPEC_DIR/$f | sopr -LN | freqt -m 2048 -M 2048 -a 0.0 -A  0.77 > $WARP_DIR/$f.warp.f4
done

echo 'saved to ' $WARP_DIR
echo 'done!'
