
import argparse
import os

parser = argparse.ArgumentParser(description='''Sync smartNN with biaree, udem or nii server''')

parser.add_argument('--udem', action='store_true', help='''sync with udem''')

parser.add_argument('--nii', action='store_true', help='''sync with nii''')

parser.add_argument('--biaree', action='store_true', help='''sync with biaree''')

parser.add_argument('--image', action='store_true', help='''sync with the image folder''')

parser.add_argument('--udemrd', action='store_true', help='''sync with the udem research demo folder''')

parser.add_argument('--udemlua', action='store_true', help='''sync with the udem lua_packages folder''')

parser.add_argument('--niklua', action='store_true', help='''sync with the nikopia lua_packages folder''')


args = parser.parse_args()

source = '/Volumes/Storage/Dropbox/CodingProjects/smartNN'
exclude = '--exclude-from=%s/exclude.txt'%source
lua_package = '/Volumes/Storage/lua_packages'
lua_exclude = '--exclude-from=%s/exclude.txt'%lua_package

if args.udem:
	if args.image:
		os.system("rsync -rvu wuzhen@elisa2.iro.umontreal.ca:/data/lisa/exp/wuzhen/smartNN/save/images \
					%s/save/images/udem"%source) 
	else:
		os.system("rsync -rvu %s %s wuzhen@elisa2.iro.umontreal.ca:/data/lisa/exp/wuzhen"%(exclude, source)) 

elif args.nii:
	if args.image:
		os.system("rsync -rvu zhenzhou@136.187.97.216:~/smartNN/save/images \
					%s/save/images/nii"%source) 
	else:
		os.system("rsync -rvu %s %s zhenzhou@136.187.97.216:~/"%(exclude, source)) 

elif args.biaree:
	if args.image:
		os.system("rsync -rvu hycis@briaree.calculquebec.ca:~/smartNN/save/images \
					%s/save/images/biaree"%source) 		
	else:
		os.system("rsync -rvu %s %s hycis@briaree.calculquebec.ca:~/"%(exclude, source))

elif args.udemrd:
    os.system("rsync -rvu %s /Volumes/Storage/VCTK/Research-Demo \
                wuzhen@elisa2.iro.umontreal.ca:/data/lisa/exp/wuzhen/nii/VoiceCloneCommercial2/"%exclude)

elif args.udemlua:
	os.system("rsync -rvu %s /Volumes/Storage/lua_packages \
                wuzhen@frontal07.iro.umontreal.ca:/data/lisa/exp/wuzhen/"%lua_exclude)

elif args.niklua:
    os.system("rsync -rvu %s /Volumes/Storage/lua_packages \
                zhenzhou@nikopia.net:/home/zhenzhou/"%lua_exclude)

else:
	raise ValueError('options is neither --udem | --nii | --biaree | --udemrd | --udemlua | --image')

