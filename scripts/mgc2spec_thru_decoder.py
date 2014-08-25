import glob
import os
import argparse
import numpy as np

def savenpy(ext, spec_dir, specnames, datafiles, dtype, 
            feature_size, output_dir, preprocessor, output_dtype):
    
    assert dtype in ['f4', 'f8']
    
    specnames_ls = glob.glob(specnames)
    datafiles_ls = glob.glob(datafiles)
    specnames_ls.sort()
    datafiles_ls.sort()
    
#     import pdb
#     pdb.set_trace()
    
    spec_files = "%s/*.%s"%(spec_dir, ext)
    dataset = os.path.basename(os.path.dirname(spec_files))
    files = glob.glob(spec_files)

    size = len(files)
    assert size > 0, 'empty folder'
    print '..number of files %d'%size
    data = []
    count = 0
    
    for datafile, specname in zip(datafiles_ls, specnames_ls):
        specname_fin = open(specname)
        specname_data = np.load(specname_fin)
        
        data = []
        for name, num_frames in specname_data:
            basename = name.split('.')[0]
            f = '%s/%s.%s'%(spec_dir, basename, ext)
            print '..opening ' + f            
            count += 1

            clip = np.fromfile(f, dtype='<%s'%dtype, count=-1)
            assert clip.shape[0] % feature_size == 0, \
                  'clip.shape[0]:%s, feature_size:%s'%(clip.shape[0],feature_size)
#                 assert clip.shape[0] / feature_size == int(num_frames)
            data.extend(clip)
                
            print(str(count) + '/' + str(size) + ' opened: '  + name)

        specname_basename = os.path.basename(specname)
        data_basename = specname_basename.replace('specnames', 'data')
#         with open(output_dir + '/%s'%data_basename, 'wb') as npy:
#             print('..saving %s'%data_basename)
        assert len(data)%feature_size == 0
        low_dim_data = np.asarray(data).reshape(len(data)/feature_size, feature_size)
#             np.save(npy, data)

        print 'datafile: ' + datafile
        print 'specname: ' + specname
        
        assert datafile.split('_data_')[-1] == specname.split('_specnames_')[-1]

        data_fin = open(datafile)
        dataset_raw = np.load(data_fin)

#             g = open(low_dim_path)
#             low_dim_data = np.load(g)

        proc = getattr(procs, preprocessor)()
        print 'applying preprocessing: ' + preprocessor
        dataset_proc = proc.apply(dataset_raw)
        del dataset_raw
        print 'decoding..'
        dataset_out = model.decode(low_dim_data)
        del low_dim_data

        print 'invert dataset..'
        dataset = proc.invert(dataset_out)
        dataset = dataset.astype(output_dtype)
        del dataset_out

#             name = os.path.basename(f_path)
#             name = name.replace('data', 'specnames')
#     
#             print 'opening.. ' + name
#             g = open(os.path.dirname(f_path) + '/' + name)

#             names_arr = np.load(g)

#         num_exp = [int(num) for f_name, num in specname_data]
#         assert sum(num_exp) == dataset.shape[0], \
#                 'number of examples %s in data array is different from the spec files %s'%(sum(num_exp), dataset.shape[0])
#  
        pointer = 0
        for f_name, num in specname_data:
            print 'f_name, num_exp : %s, %s'%(f_name, num)
            dataset[pointer:pointer+int(num)].tofile(output_dir + '/' + f_name+'.%s'%output_dtype, format=output_dtype)
            pointer += int(num)

        assert pointer == dataset.shape[0], 'did not recur until the end of array'    

        print 'closing files..'
        data_fin.close()
        specname_fin.close()
#         g.close()
        print 'Done!'

        
    print('all files saved to %s'%output_dir)
    
   
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Generate specs from hmm generated mgcs using the decoding part of Autoencoder''')
    parser.add_argument('--mgc_dir', metavar='DIR', type=str, help='''dir of the mgc files''')
    parser.add_argument('--ext', metavar='EXT', default='spec', help='''extension of mgc files''')
    parser.add_argument('--specnames', metavar='PATH', help='''path to specnames npy files''')
    parser.add_argument('--dataset', metavar='PATH', help='path to data npy file')
    parser.add_argument('--input_spec_dtype', metavar='f4|f8', default='f4', 
                        help='''dtype of the input spec files f4|f8, default=f4''')
    parser.add_argument('--feature_size', metavar='INT', default=2049, type=int, 
                        help='''feature size in an example, default=2049''')
    parser.add_argument('--output_dir', metavar='PATH', default='.', 
                        help='''directory to save the combined data file''')
    parser.add_argument('--preprocessor', metavar='NAME', help='name of the preprocessor')
    parser.add_argument('--output_dtype', metavar='f4|f8', default='f8', 
                    help='output datatype of spec file, f4|f8, default=f8')


    args = parser.parse_args()

    print('..dataset directory: %s'%args.mgc_dir)
    print('..spec extension: %s'%args.ext)
    print('..specnames: %s'%args.specnames)
    print('..original npy dataset: %s'%args.dataset)
    print('..input data files dtype: %s'%args.input_spec_dtype)
    print('..feature_size: %s'%args.feature_size)
    print('..save outputs to: %s'%args.output_dir)
    print('..preprocessor: %s'%args.preprocessor)
    print('..output_dtype: %s'%args.output_dtype)
    
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)
    
    savenpy(args.ext, args.mgc_dir, args.specnames, args.dataset, args.input_spec_dtype, 
            args.feature_size, args.output_dir, args.preprocessor, args.output_dtype)
        
        
        
