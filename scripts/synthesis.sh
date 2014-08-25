#!/bin/bash

# vol='/Volumes/Storage'
vol=~
. $vol/VCTK/Research-Demo/fa-tts/STRAIGHT-TTS/local.conf.0
TMP_DIR=$vol/VCTK/Research-Demo/fa-tts/STRAIGHT-TTS/tmp/England/Laura
F0_OUTPUT=$vol/VCTK/data/inter-module/f0/England/Laura

model=DCT_64
# SPECS_DIR=$vol/generated_specs/Laura/$model
SPECS_DIR=$vol/VCTK/Research-Demo/fa-tts/STRAIGHT-TTS/tmp/England/Laura/abs
WAV_DIR=$vol/generated_wavs/Laura/$model

if [ ! -d $WAV_DIR ]; then
    echo 'make wav dir'
    mkdir $WAV_DIR
fi
WARP_EXT=spec.warp.f4
# ext="spec.unwarp.f8"
ext=spec.double
# basenames=`ls $SPECS_DIR/ | awk -F '[/.]' '{print $1}'`
# basenames="1119_1"
echo $basenames
files=`cat /home/smg/zhenzhou/datasets/test_spec.txt`
echo $files
for f in $files; do
    base=`basename $f .$WARP_EXT`
#     echo 'unwarping: ' $f
# for base in $basenames; do
    filename="$base.$ext";
    echo $filename;
    synthesis_fft -f $rate -spec -fftl $fftlen -order $order -shift $shift -sigp 1.2 -cornf 4000 -bap -apfile ${TMP_DIR}/abs/${base}.bndap.double ${F0_OUTPUT}/${base}.f0 $SPECS_DIR/${filename} $WAV_DIR/${base}.wav > ${TMP_DIR}/log/${base}.log;
done
