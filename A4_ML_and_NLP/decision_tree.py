'''
decision_tree.py

Author Korbinian Randl
'''
import random
import math
class BinaryDecisionTree:
    def __init__(self, X:dict, y:list, bias:float=.5, max_depth:int=float('inf')) -> None:
        '''Creates and trains a decision tree.

        inputs:
            X:          dictionary str->list[float] of attributes and their values.

            y:          list[bool] of labels.

            bias:       decision bias for non-pure leaves.

            max_depth:  max_depth of the tree.
        '''
        # calculate decision threshold:
        self.fit(X, y)

        # split:
        self.children = []
        for data in self.split(X, y):
            # if no features left, max_depth reached, or unanimous label in split:
            if (len(data['X']) == 0) or (len(set(data['y'])) == 1) or (max_depth <= 1):
                # always predict average value:
                n = len(data['y'])
                if n == 0: self.children.append(False)
                else:      self.children.append((sum(data['y']) / n) > bias)
                
            else:
                # otherwise train subtree:
                subtree = BinaryDecisionTree(data['X'], data['y'], bias=bias, max_depth=max_depth-1)

                # check if subtree actually decides something:
                all_true = True
                all_false = True
                for child in subtree.children:
                    if isinstance(child, BinaryDecisionTree):
                        all_true = False
                        all_false = False
                        break

                    all_true  &= (child == True)
                    all_false &= (child == False)

                if all_true:    self.children.append(True)
                elif all_false: self.children.append(False)
                else:           self.children.append(subtree)

    def fit(self, X:dict, y:list) -> None:
        '''Calculates the best split and best attribute.

        inputs:
            X:          dictionary str->list[float] of attributes and their values.

            y:          list[bool] of labels.
        '''
        best_info_gain = -1.
        best_threshold =  0.
        best_attribute = random.choice(list(X.keys()))
        
        # for every attribute in the data:
        for attribute in X:
            x = X[attribute]

            # for every unique value of that attribute:
            for threshold in set(x):
                # split data:
                i_left  = [index for index, value in enumerate(x) if value <= threshold]
                i_right = [index for index, value in enumerate(x) if value > threshold]

                if len(i_left) > 0 and len(i_right) > 0:
                    # caclulate the information gain:
                    info_gain = self.get_information_gain(y, ([y[i] for i in i_left], [y[i] for i in i_right]))

                    # if the current split is better then the previous best:
                    if info_gain > best_info_gain:
                        best_info_gain = info_gain
                        best_threshold = threshold
                        best_attribute = attribute

        # save parameters:
        self.threshold = best_threshold
        self.attribute = best_attribute
    
    def split(self, X:dict, y:list=None) -> tuple:
        '''Splits the dataset at the threshold:

        inputs:
            X:          dictionary str->list[float] of attributes and their values.

            y:          list[bool] of labels.


        returns:        split data in dictionaries.
        '''
        # split data:
        left_split = {
            'indices':[index for index, value in enumerate(X[self.attribute]) if value <= self.threshold]
        }
        right_split = {
            'indices':[index for index, value in enumerate(X[self.attribute]) if value > self.threshold]
        }

        # split dataset:
        left_split['X']  = {key:[X[key][i] for i in left_split['indices']] for key in X if key != self.attribute}
        right_split['X'] = {key:[X[key][i] for i in right_split['indices']] for key in X if key != self.attribute}

        # split labels:
        if y is not None:
            left_split['y']  = [y[i] for i in left_split['indices']]
            right_split['y'] = [y[i] for i in right_split['indices']]

        return left_split, right_split

    def predict(self, X:dict) -> list:
        '''Predict the class of the input.

        inputs:
            X:      dictionary str->list[float] of attributes and their values.

        
        returns:    predicted boolean classes.
        '''
        predictions = [False]*len(X[self.attribute])

        # split data and process per child:
        for child, data in zip(self.children, self.split(X)):
            # if child is a Binary decision tree:
            if isinstance(child, BinaryDecisionTree):
                # predict labels:
                for i, pred in zip(data['indices'], child.predict(data['X'])):
                    predictions[i] = pred

            else:
                # otherwise assign average label:
                for i in data['indices']:
                    predictions[i] = child

        return predictions
    
    def pretty_print(self, indent:int=0) -> None:
        '''Prints the decision tree to console.
        '''
        options = [
            '  '*indent + f'{self.attribute.upper()} <= {self.threshold:.2f}:',
            '  '*indent + f'{self.attribute.upper()} > {self.threshold:.2f}:'
        ]

        for i,s in enumerate(options):
            if isinstance(self.children[i], BinaryDecisionTree):
                print(s)
                self.children[i].pretty_print(indent+1)

            else: print(s, self.children[i])

    def get_information_gain(self, y_all: list, y_split: tuple) -> float:
        '''Calculates the information gain of the split.

        inputs:
            y_all:      list[bool] of labels.
            y_split:    tuple[list[bool]] of labels in each of the splits.

        returns:        information gain of the split.
        '''

        def entropy(y):
            if len(y) == 0:
                return 0
            p_plus = sum(y) / len(y)
            p_minus = 1 - p_plus

            if p_plus == 0 or p_minus == 0:  # This avoids log(0) scenario
                return 0
            return -p_plus * math.log2(p_plus) - p_minus * math.log2(p_minus)

        # Entropy before split
        entropy_before = entropy(y_all)

        # Weighted entropy after split
        entropy_after = sum((len(s) / len(y_all)) * entropy(s) for s in y_split)

        # Information gain
        info_gain = entropy_before - entropy_after

        return info_gain