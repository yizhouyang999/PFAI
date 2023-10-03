'''
run_assignment4b.py

Author Korbinian Randl
'''

from decision_tree import BinaryDecisionTree
import metrics
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Ensure the necessary NLTK resources are downloaded:
nltk.download('punkt')
nltk.download('stopwords')


####################################################################################################
# Functions:                                                                                       #
####################################################################################################

def count_tokens(tokens:list, columns:list=None) -> tuple:
    '''Converts the provided tokenized texts to a bag of words.

    inputs:
        tokens:     list[str] of texts to be tokenized.

        columns:    list of allowed feature names.


    returns: a lists of tokens for each of the texts.
    '''
    if columns is None:
        columns = list(set(token for entry in tokens for token in entry))
        print(f"Found {len(columns)} unique tokens.")

    result = {column: [0] * len(tokens) for column in columns}
    for i, entry in enumerate(tokens):
        for token in entry:
            if token in result:
                result[token][i] += 1

    return result

####################################################################################################
# Load Data:                                                                                       #
####################################################################################################

with open('movies.json', 'r') as file:
    data = json.load(file)

X_train = data['text'][:1600]
y_train = data['class'][:1600]

X_test  = data['text'][1600:]
y_test  = data['class'][1600:]

####################################################################################################
# Main Function:                                                                                   #
####################################################################################################

if __name__ == '__main__':
    # print a sample of the data:
    print('Cornell Movie Review Data By B. Pang et al 2005 (https://www.cs.cornell.edu/home/llee/papers/pang-lee-stars.home.html):')
    for text,label in zip(X_train[:5],y_train[:5]):
        print(f'"{text}" -> {str(label)}\n')


    #TODO: improve the tokenization and preprocessing of the texts
    #hint you can use functions from the nltk library
    stop_words = set(stopwords.words('english'))

    X_train = [word_tokenize(text) for text in X_train]
    X_train = [[word.lower() for word in text if word.isalpha() and word.lower() not in stop_words] for text in X_train]

    X_test = [word_tokenize(text) for text in X_test]
    X_test = [[word.lower() for word in text if word.isalpha() and word.lower() not in stop_words] for text in X_test]

    # create bag of words:
    X_train = count_tokens(X_train)
    X_test  = count_tokens(X_test, columns=list(X_train.keys()))

    # train a decision tree classifier and predict the test set:
    print('Training Decision Tree ...')
    tree = BinaryDecisionTree(X_train, y_train, max_depth=5)
    predictions_tree = tree.predict(X_test)
    print('Done.\n')

    # print decision tree:
    print('Final Decision Tree:')
    tree.pretty_print()
    print()
    
    # print confusion matrix:
    print('Performance Decision Tree:')
    metrics.pretty_print(y_test, predictions_tree)