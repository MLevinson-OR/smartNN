import argparse
import cPickle
import glob
import os
import numpy as np
import pynet.datasets.preprocessor as procs

parser = argparse.ArgumentParser(description='generate specs from the encoded high level'
                                            + ' features save in npy form'
                                            + ' by first decoding through an autoencoder'
                                            + ' follow by splitting the decoded npy files into spec files')
parser.add_argument('--model', metavar='PATH', help='path for the model')
parser.add_argument('--preprocessor', metavar='NAME', help='name of the preprocessor')
parser.add_argument('--dataset', metavar='PATH', help='path to the original numpy data file')
parser.add_argument('--encoded_dataset', metavar='PATH', help='path to the encoded numpy')
parser.add_argument('--output_dir', metavar='DIR', 
                    help='directory to which to save the generated spec files')
parser.add_argument('--output_dtype', metavar='f4|f8', default='f8', 
                    help='output datatype of spec file, f4|f8, default=f8')

args = parser.parse_args()


print 'opening model.. ' + args.model
with open(args.model) as m:
  model = cPickle.load(m)

dataset_files = glob.glob(args.dataset)
dataset_files.sort()
low_dim_files = glob.glob(args.low_dim_dataset)
low_dim_files.sort()

if not os.path.exists(args.output_dir):
    os.mkdir(args.output_dir)

for f_path, low_dim_path in zip(dataset_files, low_dim_files):

    print 'opening.. ' + f_path
    print 'opening.. ' + low_dim_path
    
    assert f_path.split('_data_')[-1] == low_dim_path.split('_data_')[-1]
    
    f = open(f_path)
    dataset_raw = np.load(f)
    
    g = open(low_dim_path)
    low_dim_data = np.load(g)

    proc = getattr(procs, args.preprocessor)()
    print 'applying preprocessing: ' + args.preprocessor
    dataset_proc = proc.apply(dataset_raw)
    del dataset_raw
    print 'decoding..'
    dataset_out = model.decode(low_dim_data)
    del low_dim_data
    
    print 'invert dataset..'
    dataset = proc.invert(dataset_out)
    dataset = dataset.astype(args.output_dtype)
    del dataset_out

    name = os.path.basename(f_path)
    name = name.replace('data', 'specnames')
    
    print 'opening.. ' + name
    g = open(os.path.dirname(f_path) + '/' + name)
    
    names_arr = np.load(g)
    
    num_exp = [int(num) for f_name, num in names_arr]
    assert sum(num_exp) == dataset.shape[0], \
            'number of examples %s in data array is different from the spec files %s'%(sum(num_exp), dataset.shape[0])
     
    pointer = 0
    for f_name, num in names_arr:
        print 'f_name, num_exp : %s, %s'%(f_name, num)
        dataset[pointer:pointer+int(num)].tofile(args.output_dir + '/' + f_name+'.%s'%args.output_dtype, format=args.output_dtype)
        pointer += int(num)
    
    assert pointer == dataset.shape[0], 'did not recur until the end of array'    
    
    print 'closing files..'
    f.close()
    g.close()
    print 'Done!'
    





