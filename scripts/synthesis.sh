#!/bin/bash

# vol='/Volumes/Storage'
vol=/home/smg/zhenzhou
. $vol/VCTK/Research-Demo/fa-tts/STRAIGHT-TTS/local.conf.0
TMP_DIR=$vol/VCTK/Research-Demo/fa-tts/STRAIGHT-TTS/tmp/England/Laura
F0_OUTPUT=$vol/VCTK/data/inter-module/f0/England/Laura


SPEC_DIR=
SPEC_EXT=
WAV_DIR=
files=

while [ "$1" != "" ]; do
    case $1 in
        --spec_dir )            shift
                                SPEC_DIR=$1
                                ;;
        --spec_ext )            shift
                                SPEC_EXT=$1
                                ;; 
        --wav_dir )          shift
                                WAV_DIR=$1
                                ;; 
        --warp_txt_file )       shift
                                files=`cat $1`
                                ;;
        -h | --help )           echo 'options'
                                echo '--spec_dir : directory for spec files'
                                echo '--spec_ext : extension of the spec files, input file type has to be f8'
                                echo '--wav_dir : directory for saving the output wav files'
                                echo '[--spec_txt_file] : path to the txt file that contains list of files for processing'
                                exit
                                ;;
    esac
    shift
done


n=`echo $files | wc -w`
if [ $n == 0 ]; then
    files=`ls $SPEC_DIR/*.$SPEC_EXT | awk -F '[.]' '{print $1}'`
fi


echo 'number of files: ' `echo $files | wc -w`


if [ ! -d $WAV_DIR ]; then
    echo 'make wav dir' $WAV_DIR
    mkdir $WAV_DIR
fi


# model=DCT_64
# SPECS_DIR=$vol/generated_specs/Laura/$model
# SPECS_DIR=$vol/VCTK/Research-Demo/fa-tts/STRAIGHT-TTS/tmp/England/Laura/abs
# WAV_DIR=$vol/generated_wavs/Laura/$model

# SPEC_EXT=spec.warp.f4
# ext="spec.unwarp.f8"
# ext=spec.double
# basenames=`ls $SPECS_DIR/ | awk -F '[/.]' '{print $1}'`
# basenames="1119_1"
# echo $basenames
# files=`cat /home/smg/zhenzhou/datasets/test_spec.txt`
# echo $files
for f in $files; do
#     base=`basename $f .$SPEC_EXT`
#     echo 'unwarping: ' $f
# for base in $basenames; do
#     filename="$base.$ext";
    filename=`basename $f`
    echo $filename;
    synthesis_fft -f $rate -spec -fftl $fftlen -order $order -shift $shift -sigp 1.2 -cornf 4000 -bap -apfile ${TMP_DIR}/abs/${base}.bndap.double ${F0_OUTPUT}/${base}.f0 $SPECS_DIR/${filename} $WAV_DIR/${base}.wav > ${TMP_DIR}/log/${base}.log;
done
