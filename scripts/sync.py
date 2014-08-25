
import argparse
import os

parser = argparse.ArgumentParser(description='''Sync smartNN with biaree, udem or nii server''')

parser.add_argument('--udem', action='store_true', help='''sync with udem''')

parser.add_argument('--nii', action='store_true', help='''sync with nii''')

parser.add_argument('--biaree', action='store_true', help='''sync with biaree''')

parser.add_argument('--image', action='store_true', help='''sync with the image folder''')

parser.add_argument('--scratch', action='store_true', help='''sync with the scratch folder''')

parser.add_argument('--udemrd', action='store_true', help='''sync with the udem research demo folder''')

parser.add_argument('--udemlua', action='store_true', help='''sync with the udem lua_packages folder''')

parser.add_argument('--niklua', action='store_true', help='''sync with the nikopia lua_packages folder''')

parser.add_argument('--pynet', action='store_true', help='''sync with the pynet folder''')

parser.add_argument('--gill', action='store_true', help='''sync with gillimin''')

args = parser.parse_args()

source = '/Volumes/Storage/Dropbox/CodingProjects'
exclude = '--exclude-from=%s/smartNN/exclude.txt'%source
lua_package = '/Volumes/Storage/lua_packages'
lua_exclude = '--exclude-from=%s/exclude.txt'%lua_package

if args.udem:
	if args.image:
		os.system("rsync -rvu wuzhen@frontal07.iro.umontreal.ca:/data/lisa/exp/wuzhen/smartNN/save/images \
					%s/smartNN/save/images/udem"%source)
	else:
		os.system("rsync -rvu %s %s/smartNN wuzhen@frontal07.iro.umontreal.ca:/data/lisa/exp/wuzhen"%(exclude, source))

elif args.gill:
	if args.pynet:
	    os.system("rsync -rvu %s %s/pynet hycis@guillimin.clumeq.ca:/sb/project/jvb-000-aa/zhenzhou"%(exclude, source))
	
	else:
		os.system("rsync -rvu %s %s/smartNN hycis@guillimin.clumeq.ca:/sb/project/jvb-000-aa/zhenzhou"%(exclude, source))  

elif args.nii:
	if args.image:
		os.system("rsync -rvu zhenzhou@136.187.97.216:~/smartNN/save/images \
					%s/smartNN/save/images/nii"%source)
					
	elif args.pynet:
	    os.system("rsync -rvu %s %s/pynet zhenzhou@136.187.97.216:~/"%(exclude, source))
	
	else:
		os.system("rsync -rvu %s %s/smartNN zhenzhou@136.187.97.216:~/"%(exclude, source))

elif args.biaree:
	if args.image:
		os.system("rsync -rvu hycis@briaree.calculquebec.ca:~/smartNN/save/images \
					%s/smartNN/save/images/biaree"%source)

# 	elif args.scratch:
# 		os.system("rsync -rvu %s %s/smartNN hycis@briaree.calculquebec.ca:/RQexec/hycis"%(exclude, source))

	elif args.pynet:
		os.system("rsync -rvu %s %s/pynet hycis@briaree.calculquebec.ca:/RQexec/hycis"%(exclude, source))
    
	else:
		os.system("rsync -rvu %s %s/smartNN hycis@briaree.calculquebec.ca:/RQexec/hycis"%(exclude, source))

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
	raise ValueError('options is neither --udem | --nii | --biaree | --udemrd | --udemlua | --image | --niklua | --pynet')
