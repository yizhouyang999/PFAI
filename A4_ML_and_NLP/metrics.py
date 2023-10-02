'''
metrics.py

Author Korbinian Randl
'''

def get_false_positives(y_true:list, y_pred:list) -> int:
    '''Returns the number of false positives.'''
    assert len(y_true) == len(y_pred), "Input lists must have the same length"
    return sum([1 for yt, yp in zip(y_true, y_pred) if yt == False and yp == True])

def get_true_positives(y_true:list, y_pred:list) -> int:
    '''Returns the number of true positives.'''
    assert len(y_true) == len(y_pred), "Input lists must have the same length"
    return sum([1 for yt, yp in zip(y_true, y_pred) if yt == True and yp == True])

def get_false_negatives(y_true:list, y_pred:list) -> int:
    '''Returns the number of false negatives.'''
    assert len(y_true) == len(y_pred), "Input lists must have the same length"
    return sum([1 for yt, yp in zip(y_true, y_pred) if yt == True and yp == False])

def get_true_negatives(y_true:list, y_pred:list) -> int:
    '''Returns the number of true negatives.'''
    assert len(y_true) == len(y_pred), "Input lists must have the same length"
    return sum([1 for yt, yp in zip(y_true, y_pred) if yt == False and yp == False])

def get_accuracy(y_true:list, y_pred:list) -> float:
    '''Returns the accuracy of the predictions.'''
    assert len(y_true) == len(y_pred), "Input lists must have the same length"
    tp = get_true_positives(y_true, y_pred)
    tn = get_true_negatives(y_true, y_pred)
    return (tp + tn) / len(y_true)

def get_f1(y_true:list, y_pred:list) -> float:
    '''Returns the f1 score for the predictions.'''
    assert len(y_true) == len(y_pred), "Input lists must have the same length"
    tp = get_true_positives(y_true, y_pred)
    fp = get_false_positives(y_true, y_pred)
    fn = get_false_negatives(y_true, y_pred)
    precision = tp / (tp + fp) if (tp + fp) != 0 else 0
    recall = tp / (tp + fn) if (tp + fn) != 0 else 0
    return 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0


def pretty_print(y_true:list, y_pred:list) -> None:
    '''Prints a confusion matrix in ascii art.

    inputs:
        y_true:      list[bool] of true labels.

        y_pred:      list[bool] of predicted labels.)
    '''
    fp = f'{get_false_positives(y_true, y_pred):4d}'
    fn = f'{get_false_negatives(y_true, y_pred):4d}'
    tp = f'{get_true_positives(y_true, y_pred):4d}'
    tn = f'{get_true_negatives(y_true, y_pred):4d}'

    print( '      |    true    |')
    print( ' pred | TRUE FALSE |')
    print( '------|------------|')
    print(f' TRUE | {tp}  {fp} |')
    print(f'FALSE | {fn}  {tn} |\n')

    print(f'Accuracy: {get_accuracy(y_true, y_pred):.4f}')
    print(f'F1-score: {get_f1(y_true, y_pred):.4f}')