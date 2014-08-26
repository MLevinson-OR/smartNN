
# Generate mceps from the encoder part of autoencoder #

__Summary of steps for generating mcep files from Autoencoder__

1. Generate warp specs from original spec
2. Merge warp specs into npy arrays to be feeded into Autoencoder
3. Pass the npy arrays through the encoding part of the Autoencoder to get
   lower dimensional npy arrays
4. Split the lower dimensional npy arrays into mcep files


__1. Generate warp specs from original spec__

To generate warp specs run [warp.sh](../scripts/warp.sh)

```bash
$ bash warp.sh --spec_dir /home/smg/zhenzhou/VCTK/data/inter-module/mcep/England/Laura 
  --warp_dir /home/smg/zhenzhou/demo/Laura_warp
```

__2. Merge warp specs into npy arrays to be feeded into Autoencoder__

In order to run the Autoencoder on the warp spec files, the warp spec files has to be
merged into a numpy array by running [specs2data.py](../scripts/specs2data.py) 
```bash
$ python specs2data.py --spec_dir /home/smg/zhenzhou/datasets/Laura_warp --ext spec.warp.f4 \
  --splits 20 --input_spec_dtype f4 --feature_size 2049 --output_dir /home/smg/zhenzhou/demo/Laura_warp_npy
```

__3. Pass the npy arrays through the encoding part of the Autoencoder to get
   lower dimensional npy arrays__

run [encode_dataset.py](../scripts/encode_dataset.py) to output the lower dimensional features
```bash
$ model=AE0729_warp_3layers_finetune_20140729_1221_54548278
$ python encode_dataset.py --model /home/smg/zhenzhou/pynet/save/log/$model/model.pkl \
  --preprocessor Scale --dataset '/home/smg/zhenzhou/demo/Laura_warp_npy/Laura_warp_data*' \
  --output_dir /home/smg/zhenzhou/demo/encoded/AE-120_npy
```

__4. Split the lower dimensional npy arrays into mcep files__

run [data2specs.py](../scripts/specs2data.py) to split npy arrays into individual mcep|spec files
```bash
$ python data2specs.py --dataset '/home/smg/zhenzhou/demo/encoded/AE-120_npy/Laura_warp_data*' \
  --specnames '/home/smg/zhenzhou/demo/Laura_warp_npy/Laura_warp_specnames*' --output_spec_dtype f4 \
  --output_dir /home/smg/zhenzhou/demo/generated_mceps/$model
```

# Pass HMM generated mgc through decoder to generate specs which is synthesized to wav #
__Summary of steps for generating wave files using hmm generated mceps passing through decoder__

1. Generate specs from hmm generated mgcs using the decoding part of Autoencoder
2. Unwarp the generated specs
3. Synthesize wav from unwarp specs

__1. Generate specs from hmm generated mgcs using the decoding part of Autoencoder__

run [mgc2spec_thru_decoder.py](../scripts/mgc2spec_thru_decoder.py) to generate the spec files
by passing the mgc files through the decoding part of the encoder
```bash
$ model=AE0729_warp_3layers_finetune_20140729_1221_54548278
$ python mgc2spec_thru_decoder.py  --mgc_dir /home/smg/takaki/DNN/Zhenzhou/20140805/AE-120/AE-120 \
    --ext mgc --specnames '/home/smg/zhenzhou/demo/Laura_warp_npy/Laura_warp_specnames*' \
    --dataset '/home/smg/zhenzhou/demo/Laura_warp_npy/Laura_warp_data*' \
    --input_spec_dtype f4 --feature_size 120 --output_dir /home/smg/zhenzhou/demo/decoded_specs/$model \
    --preprocessor Scale --output_dtype f4 --model /home/smg/zhenzhou/pynet/save/log/$model/model.pkl
```

__2. Unwarp the generated specs__

run [unwarp.sh](../scripts/unwarp.sh) to unwarp the generated warp specs
```bash
$ bash unwarp.sh --warp_dir /home/smg/zhenzhou/demo/decoded_specs/$model \
  --warp_ext spec.warp.f4 --unwarp_dir /home/smg/zhenzhou/demo/decoded_specs/$model \
  --warp_txt_file /home/smg/zhenzhou/datasets/test_spec.txt
```

__3. Synthesize wav from unwarp specs__

run [mk_wav.sh](../scripts/mk_wav.sh) for synthesizing wav files from unwarp specs
```bash
$ bash mk_wav.sh
```


# Reconstruct spec file using autoencoder and use it to synthesize wav #

__Summary of steps for generating wave files from Autoencoder__

1. Generate reconstructed specs from the Autoencoder (combining encoding and decoding)
2. Unwarp the reconstructed specs
3. Synthesize wav from unwarp specs


__1. Generate reconstructed specs from the Autoencoder (combining encoding and decoding)__

run [generate_specs_from_model.py](../scripts/generate_specs_from_model.py)
```bash
$ model=AE0729_warp_3layers_finetune_20140729_1221_54548278
$ python generate_specs_from_model.py --model /home/smg/zhenzhou/pynet/save/log/$model/model.pkl \
  --preprocessor Scale --dataset '/home/smg/zhenzhou/demo/Laura_warp_npy/Laura_warp_data*' \
  --output_dir /home/smg/zhenzhou/demo/generated_specs/$model --output_dtype f4
```

__2. Unwarp the reconstructed specs__

run [unwarp.sh](../scripts/unwarp.sh) to unwarp the reconstructed warp specs
```bash
$ bash unwarp.sh --warp_dir /home/smg/zhenzhou/demo/generated_specs/$model \
  --warp_ext spec.warp.f4 --unwarp_dir /home/smg/zhenzhou/demo/generated_specs/$model \
  --warp_txt_file /home/smg/zhenzhou/datasets/test_spec.txt
```

__3. Synthesize wav from unwarp specs__

run [synthesis.sh](../scripts/synthesis.sh) for synthesizing wav files from unwarp specs
```bash
$ bash synthesis.sh --spec_dir /home/smg/zhenzhou/demo/generated_specs/$model --spec_ext spec.unwarp.f8 \
  --wav_dir /home/smg/zhenzhou/demo/generated_wavs/$model \
  --warp_txt_file /home/smg/zhenzhou/datasets/test_spec.txt
```


