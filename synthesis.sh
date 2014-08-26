#!/bin/bash

vol='/home/smg/zhenzhou'

. $vol/VCTK/Research-Demo/fa-tts/STRAIGHT-TTS/local.conf.0
TMP_DIR=$vol/VCTK/Research-Demo/fa-tts/STRAIGHT-TTS/tmp/England/Laura
F0_OUTPUT=$vol/VCTK/data/inter-module/f0/England/Laura

model=AE0713_Warp_500_20140714_1317_43818059
SPECS_DIR=$vol/generated_specs/Laura/$model
WAV_DIR=$vol/generated_wavs/Laura/$model

if [ ! -d $WAV_DIR ]; then
    echo 'make wav dir'
    mkdir $WAV_DIR
fi

ext="spec.unwarp.f8"
basenames=`ls $SPECS_DIR/ | awk -F '[/.]' '{print $1}'`
# basenames="001_4"
echo $basenames

for base in $basenames; do
    echo $base;
    filename="$base.$ext";
    echo $filename;
    synthesis_fft -f $rate -spec -fftl $fftlen -order $order -shift $shift -sigp 1.2 -cornf 4000 -bap -apfile ${TMP_DIR}/abs/${base}.bndap.double ${F0_OUTPUT}/${base}.f0 $SPECS_DIR/${filename} $WAV_DIR/${base}.wav > ${TMP_DIR}/log/${base}.log;
done
