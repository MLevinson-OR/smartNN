from hps.models import *
import os


def setEnv():

    NNdir = os.path.dirname(os.path.realpath(__file__))
    NNdir = os.path.dirname(NNdir)
    NNdir = os.path.dirname(NNdir)

    if not os.getenv('smartNN_DATA_PATH'):
        os.environ['smartNN_DATA_PATH'] = NNdir + '/data'

    if not os.getenv('smartNN_DATABASE_PATH'):
        os.environ['smartNN_DATABASE_PATH'] = NNdir + '/database'

    if not os.getenv('smartNN_SAVE_PATH'):
        os.environ['smartNN_SAVE_PATH'] = NNdir + '/save'

    print('smartNN_DATA_PATH = ' + os.environ['smartNN_DATA_PATH'])
    print('smartNN_SAVE_PATH = ' + os.environ['smartNN_SAVE_PATH'])
    print('smartNN_DATABASE_PATH = ' + os.environ['smartNN_DATABASE_PATH'])


def AE_exp(state, channel):

    setEnv()
    hps = AE(state)
    hps.run()

    return channel.COMPLETE

def AE_Two_Layers_exp(state, channel):

    setEnv()

    hps = AE_Two_Layers(state)
    hps.run()

    return channel.COMPLETE

def AE_Two_Layers_WO_Pretrain_exp(state, channel):

    setEnv()
    hps = AE_Two_Layers_WO_Pretrain(state)
    hps.run()

    return channel.COMPLETE


def AE_Many_Splits_exp(state, channel):

    setEnv()
    hps = AE_Many_Splits(state)
    hps.run()

    return channel.COMPLETE
