import theano.tensor as T
import theano

floatX = theano.config.floatX

class Cost(object):
    """
    Cost inherits MLP so that cost can make use of the 
    """
    def __init__(self, type = 'nll'):
        self.type = type
        
    def get_accuracy(self, y, y_pred):
        """Return a float representing the number of errors in the minibatch
        over the total number of examples of the minibatch ; zero one
        loss over the size of the minibatch

        :type y: theano.tensor.TensorType
        :param y: corresponds to a vector that gives for each example the
                  correct label
        """

        # check if y has same dimension of y_pred
        if y.ndim != y_pred.ndim:
            raise TypeError('y should have the same shape as self.y_pred',
                ('y', y.type, 'y_pred', y_pred.type))

        return T.eq(y_pred.argmax(axis=1), 
                    y.argmax(axis=1)).sum(dtype=floatX) / y.shape[0]

    
    def positives(self, y, y_pred):
        """
        return the number of correctly predicted examples in a batch
        """
        return T.eq(y_pred.argmax(axis=1), y.argmax(axis=1)).sum(dtype=floatX)
    
    def get_batch_cost(self, y, y_pred):
        return getattr(self, '_batch_cost_' + self.type)(y, y_pred)
    
    def _batch_cost_nll(self, y, y_pred):
        """
        return the total cost of all the examples in a batch
        """
        return T.sum(T.log(y_pred)[T.arange(y.shape[0]), y.argmin(axis=1)])
    
    def confusion_matrix(self, y, y_pred):
        pass
            
    def get_cost(self, y, y_pred):
        return getattr(self, '_cost_' + self.type)(y, y_pred)
    
    def _cost_mse(self, y, y_pred):
        L = T.sum(T.sqr(y - y_pred), axis=1)
        return T.mean(L, dtype=floatX)
        
    def _cost_entropy(self, y, y_pred):        
        L = - T.sum(y * T.log(y_pred) + (1-y) * T.log(1-y_pred), axis=1)
        return T.mean(L, dtype=floatX)
    
    def _cost_error(self, y, y_pred):
        L = T.neq(y_pred.argmax(axis=1), y.argmax(axis=1))
        return T.mean(L, dtype=floatX)
    
    def _cost_abs(self, y, y_pred):
        L = T.sum(T.abs_(y - y_pred, axis=1))
        return T.mean(L, dtype=floatX)
    
    def _cost_top1(self, y, y_pred):
        TP = y[T.arange(y.shape[0]), y_pred.argmax(axis=1)]
        return T.sum(TP, dtype=floatX) / TP.shape[0]
        
    def _cost_top5(self, y, y_pred):
        tp = T.zeros(y.shape)
        
        for row, z in zip(y_pred,tp):
            sorted = row.argsort(axis=1)[:5] # top 5 values
            z[sorted] = 1 
        
        for k in T.arange(y_pred.shape[1]):
            if k < y_shape[1] - 5:
                y_pred[T.arange(y_pred.shape[0]), y_pred.argmin(axis=1)] = 1
            else:
                y_pred[T.arange(y_pred.shape[0]), y_pred.argmax(axis=1)] = -1
        
        
            
        return T.sum(tp)
        
    
        
    