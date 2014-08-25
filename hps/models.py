
from jobman import DD, expand, flatten

import smartNN.layer as layer

from smartNN.model import *
from smartNN.layer import *
from smartNN.datasets.mnist import Mnist
import smartNN.datasets.spec as spec
from smartNN.learning_rule import LearningRule
from smartNN.log import Log
from smartNN.train_object import TrainObject
from smartNN.cost import Cost
import smartNN.datasets.preprocessor as preproc
import cPickle
import os

from smartNN.utils.check_memory import *

class AE:

    def __init__(self, state):
        self.state = state

    def run(self):
        log = self.build_log()
        dataset = self.build_dataset()

        learning_rule = self.build_learning_rule()
        model = self.build_model(dataset)
        train_obj = TrainObject(log = log,
                                dataset = dataset,
                                learning_rule = learning_rule,
                                model = model)
        train_obj.run()


    def build_log(self, id=None):
        log = Log(experiment_name = id is not None and '%s_%s'%(self.state.log.experiment_name,id) \
                                    or self.state.log.experiment_name,
                description = self.state.log.description,
                save_outputs = self.state.log.save_outputs,
                save_hyperparams = self.state.log.save_hyperparams,
                save_model = self.state.log.save_model,
                send_to_database = self.state.log.send_to_database)
        return log


    def build_dataset(self, part=None):

        dataset = None

        preprocessor = None if self.state.dataset.preprocessor is None else \
                       getattr(preproc, self.state.dataset.preprocessor)()

        if self.state.dataset.type == 'Mnist':
            dataset = Mnist(train_valid_test_ratio = self.state.dataset.train_valid_test_ratio,
                            preprocessor = preprocessor,
                            batch_size = self.state.dataset.batch_size,
                            num_batches = self.state.dataset.num_batches,
                            iter_class = self.state.dataset.iter_class,
                            rng = self.state.dataset.rng)

        elif self.state.dataset.type[:4] == 'P276':
            dataset = getattr(spec, self.state.dataset.type)(
                            train_valid_test_ratio = self.state.dataset.train_valid_test_ratio,
                            preprocessor = preprocessor,
                            batch_size = self.state.dataset.batch_size,
                            num_batches = self.state.dataset.num_batches,
                            iter_class = self.state.dataset.iter_class,
                            rng = self.state.dataset.rng)

        elif self.state.dataset.type[:5] == 'Laura':
            assert part is not None, 'split name is required for Laura dataset'
            dataset = getattr(spec, self.state.dataset.type)(
                            part = part,
                            train_valid_test_ratio = self.state.dataset.train_valid_test_ratio,
                            preprocessor = preprocessor,
                            batch_size = self.state.dataset.batch_size,
                            num_batches = self.state.dataset.num_batches,
                            iter_class = self.state.dataset.iter_class,
                            rng = self.state.dataset.rng)

        train = dataset.get_train()
        dataset.set_train(train.X, train.X)

        valid = dataset.get_valid()
        dataset.set_valid(valid.X, valid.X)

        test = dataset.get_test()
        dataset.set_test(test.X, test.X)

        return dataset


    def build_learning_rule(self):
        learning_rule = LearningRule(max_col_norm = self.state.learning_rule.max_col_norm,
                                    learning_rate = self.state.learning_rule.learning_rate,
                                    momentum = self.state.learning_rule.momentum,
                                    momentum_type = self.state.learning_rule.momentum_type,
                                    L1_lambda = self.state.learning_rule.L1_lambda,
                                    L2_lambda = self.state.learning_rule.L2_lambda,
                                    cost = Cost(type = self.state.learning_rule.cost),
                                    stopping_criteria = {'max_epoch' : self.state.learning_rule.stopping_criteria.max_epoch,
                                                        'epoch_look_back' : self.state.learning_rule.stopping_criteria.epoch_look_back,
                                                        'cost' : Cost(type=self.state.learning_rule.stopping_criteria.cost),
                                                        'percent_decrease' : self.state.learning_rule.stopping_criteria.percent_decrease})
        return learning_rule


    def build_one_hid_model(self, input_dim):
        model = AutoEncoder(input_dim = input_dim, rand_seed=self.state.model.rand_seed)
        hidden_layer = getattr(layer, self.state.hidden_layer.type)(dim=self.state.hidden_layer.dim,
                                                                    name=self.state.hidden_layer.name,
                                                                    dropout_below=self.state.hidden_layer.dropout_below)
        model.add_encode_layer(hidden_layer)
        output_layer = getattr(layer, self.state.output_layer.type)(dim=dataset.target_size(),
                                                                    name=self.state.output_layer.name,
                                                                    W=hidden_layer.W.T,
                                                                    dropout_below=self.state.output_layer.dropout_below)
        model.add_decode_layer(output_layer)
        return model


    def build_two_hid_model(self, input_dim):
        model = AutoEncoder(input_dim=input_dim, rand_seed=self.state.model.rand_seed)
        hidden1 = getattr(layer, self.state.hidden1.type)(dim=self.state.hidden1.dim,
                                                        name=self.state.hidden1.name,
                                                        dropout_below=self.state.hidden1.dropout_below)
        model.add_encode_layer(hidden1)

        hidden2 = getattr(layer, self.state.hidden2.type)(dim=self.state.hidden2.dim,
                                                        name=self.state.hidden2.name,
                                                        dropout_below=self.state.hidden2.dropout_below)
        model.add_encode_layer(hidden2)

        hidden2_mirror = getattr(layer, self.state.h2_mirror.type)(dim=self.state.hidden1.dim,
                                                                name=self.state.h2_mirror.name,
                                                                W = hidden2.W.T)
        model.add_decode_layer(hidden2_mirror)

        hidden1_mirror = getattr(layer, self.state.h1_mirror.type)(dim=input_dim,
                                                                name=self.state.h1_mirror.name,
                                                                W = hidden1.W.T)
        model.add_decode_layer(hidden1_mirror)
        return model


class AE_Two_Layers(AE):

    def __init__(self, state):
        self.state = state


    def run(self):
        log = self.build_log()

        dataset = self.build_dataset()

        learning_rule = self.build_learning_rule()

        with open(os.environ['smartNN_SAVE_PATH'] + '/log/' +
                self.state.hidden1.model_name + '/model.pkl', 'rb') as f:
            print('unpickling model: ' + self.state.hidden1.model_name)
            h1 = cPickle.load(f)

        with open(os.environ['smartNN_SAVE_PATH'] + '/log/' +
                self.state.hidden2.model_name + '/model.pkl', 'rb') as f:
            print('unpickling model: ' + self.state.hidden2.model_name)
            h2 = cPickle.load(f)

        model = AutoEncoder(input_dim = dataset.feature_size(), rand_seed=self.state.model.rand_seed)
        model.add_encode_layer(h1.layers[0])
        model.add_encode_layer(h2.layers[0])
        model.add_decode_layer(h2.layers[1])
        model.add_decode_layer(h1.layers[1])

        train_obj = TrainObject(log = log,
                                dataset = dataset,
                                learning_rule = learning_rule,
                                model = model)
        train_obj.run()


class AE_Two_Layers_WO_Pretrain(AE):

    def __init__(self, state):
        self.state = state

    def run(self):
        log = self.build_log()
        dataset = self.build_dataset()
        learning_rule = self.build_learning_rule()

        model = self.build_two_hid_model(dataset.feature_size())

        train_obj = TrainObject(log = log,
                                dataset = dataset,
                                learning_rule = learning_rule,
                                model = model)
        train_obj.run()



class AE_Many_Splits(AE):

    def __init__(self, state):
        self.state = state


    def run(self):

        print(type(self.state.xmen))

        parts = ['Laura_data_000.npy', 'Laura_data_010.npy', 'Laura_data_020.npy', 'Laura_data_030.npy',
                'Laura_data_001.npy','Laura_data_011.npy','Laura_data_021.npy','Laura_data_031.npy',
                'Laura_data_002.npy','Laura_data_012.npy','Laura_data_022.npy','Laura_data_032.npy',
                'Laura_data_003.npy','Laura_data_013.npy','Laura_data_023.npy','Laura_data_033.npy',
                'Laura_data_004.npy','Laura_data_014.npy','Laura_data_024.npy','Laura_data_034.npy',
                'Laura_data_005.npy','Laura_data_015.npy','Laura_data_025.npy','Laura_data_035.npy',
                'Laura_data_006.npy','Laura_data_016.npy','Laura_data_026.npy','Laura_data_036.npy',
                'Laura_data_007.npy','Laura_data_017.npy','Laura_data_027.npy','Laura_data_037.npy',
                'Laura_data_008.npy','Laura_data_018.npy','Laura_data_028.npy','Laura_data_038.npy',
                'Laura_data_009.npy','Laura_data_019.npy','Laura_data_029.npy','Laura_data_039.npy']

        learning_rule = self.build_learning_rule()
        dataset = self.build_dataset(parts[0])
        model = self.build_two_hid_model(dataset.feature_size())
        parts.pop(0)
        log = self.build_log()
        train_obj = TrainObject(log = log,
                               dataset = dataset,
                               learning_rule = learning_rule,
                               model = model)
        train_obj.run()

        for r in range(self.state.num_runs):
            for part in parts:
                log.log('run: ' + str(r+1) + ' of %s'%self.state.num_runs)
                log.log('part: ' + part + ' of ' + str(parts))
                log.log('loading dataset..')
                dataset = self.build_dataset(part)
                train_obj.dataset = dataset
                print_mem_usage()
                train_obj.run()
                print_mem_usage()
