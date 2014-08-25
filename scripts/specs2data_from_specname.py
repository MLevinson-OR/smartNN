import glob
import os
import argparse
import numpy as np

def savenpy(ext, spec_dir, specnames, dtype, feature_size, output_dir):
    
    assert dtype in ['f4', 'f8']
    
    specnames_ls = glob.glob(specnames)
    
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
    
    for specname in specnames_ls:
        
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
        with open(output_dir + '/%s'%data_basename, 'wb') as npy:
            print('..saving %s'%data_basename)
            assert len(data)%feature_size == 0
            data = np.asarray(data).reshape(len(data)/feature_size, feature_size)
            np.save(npy, data)

        specname_fin.close()
        
    print('all files saved to %s'%output_dir)
    
   
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''combine specs files inside splits of npy files''')
    parser.add_argument('--spec_dir', metavar='DIR', type=str, help='''dir of the spec files''')
    parser.add_argument('--ext', metavar='EXT', default='spec', help='''extension of spec files''')
    parser.add_argument('--specnames', metavar='PATH', help='''path to specnames npy files''')
    parser.add_argument('--input_spec_dtype', metavar='f4|f8', default='f4', 
                        help='''dtype of the input spec files f4|f8, default=f4''')
    parser.add_argument('--feature_size', metavar='INT', default=2049, type=int, 
                        help='''feature size in an example''')
    parser.add_argument('--output_dir', metavar='PATH', default='.', 
                        help='''directory to save the combined data file''')

    args = parser.parse_args()

    print('..dataset directory: %s'%args.spec_dir)
    print('..spec extension: %s'%args.ext)
    print('..specnames: %s'%args.specnames)
    print('..input data files dtype: %s'%args.input_spec_dtype)
    print('..feature_size: %s'%args.feature_size)
    print('..save outputs to: %s'%args.output_dir)
    
    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)
    
    savenpy(args.ext, args.spec_dir, args.specnames, args.input_spec_dtype, args.feature_size, args.output_dir)
        
        
        
