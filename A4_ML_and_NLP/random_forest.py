'''
random_forest.py

Author Korbinian Randl
'''
from decision_tree import BinaryDecisionTree
import random

class BinaryRandomForest:
    def __init__(self, X:dict, y:list, n_trees:int, bias:float=.5, max_depth:int=float('inf')) -> None:
        '''Creates and trains a binary random forest.

        inputs:
            X:          dictionary str->list[float] of attributes and their values.

            y:          list[bool] of labels.

            n_trees:    number of trees in the forest.

            bias:       decision bias for non-pure leaves.

            max_depth:  max_depth of the tree.
        '''
        self.trees = [BinaryDecisionTree(*self.get_sample(X, y), **{'bias':bias, 'max_depth':max_depth}) for _ in range(n_trees)]

    def predict(self, X:dict) -> bool:
        '''Predict the class of the input.

        inputs:
            X:          dictionary str->list[float] of attributes and their values.

        
        returns:        predicted boolean class
        '''
        predictions = [tree.predict(X) for tree in self.trees]
        true_predictions = []
        for idx in range(len(predictions[0])):
            true_predictions.append(sum([prediction[idx] for prediction in predictions]) > len(predictions)/2)
        return true_predictions

    def get_sample(self, X: dict, y: list) -> tuple:
        '''Implements feature bagging for X and returns a bootstrap sample of X and y.

        inputs:
            X:          dictionary str->list[float] of attributes and their values.
            y:          list[bool] of labels.

        returns:        a bootstrap sample of X and y
        '''
        sample_size = len(next(iter(X.values())))  # number of data points in X
        sampled_indices = [random.choice(range(sample_size)) for _ in range(sample_size)]  # bootstrapped indices

        bootstrapped_X = {attribute: [X[attribute][index] for index in sampled_indices] for attribute in X}
        bootstrapped_y = [y[index] for index in sampled_indices]

        return bootstrapped_X, bootstrapped_y