'''
Definitions for GameNode, GameSearch and MCTS

Author: Tony Lindgren
'''
from time import process_time
import random

class GameNode:
    '''
    This class defines game nodes in game search trees. It keeps track of:
    state, parent, playouts, wins, successors, move, actions_left
    '''
    def __init__(self, state, move=None, parent=None):
        self.state = state
        self.parent = parent
        self.playouts = 0
        self.wins = 0
        self.successors = []
        self.move = move
        self.actions_left = state.actions()

    def ucb1(self, parent_playouts):
        if self.playouts == 0:
            return 100000
        return (self.wins / self.playouts) + (2 * (parent_playouts ** 0.5 / self.playouts))


class GameSearch:
    '''
    Class containing different game search algorithms, call it with a defined game/node
    '''
    def __init__(self, game, depth=10, time_limit=None):
        self.state = game
        self.depth = depth
        self.time_limit = time_limit

    def mcts(self):
        start_time = process_time()
        tree = GameNode(self.state)
        elapsed_time = 0
        while elapsed_time < self.time_limit:
            leaf = self.select(tree)
            child = self.expand(leaf)
            result = self.simulate(child)
            self.back_propagate(result, child)
            stop_time = process_time()
            elapsed_time = stop_time - start_time
        move = self.actions(tree)
        return move

    def select(self, node):
        if node.actions_left:
            return node
        max_ucb1_child = max(node.successors, key=lambda child: child.ucb1(node.playouts))
        return self.select(max_ucb1_child)

    def expand(self, node):
        if not node.actions_left:
            return node

        action = random.choice(node.actions_left)
        child_node = GameNode(node.state.result(action), move=action, parent=node)
        node.successors.append(child_node)
        node.actions_left.remove(action)
        return child_node

    def simulate(self, node):
        current_node = node
        while True:
            terminal_status, utility = current_node.state.is_terminal()
            if terminal_status:
                return utility
            action = random.choice(current_node.state.actions())
            current_node = GameNode(current_node.state.result(action), move=action, parent=current_node)

    def back_propagate(self, result, node):
        current_node = node
        while current_node:
            current_node.playouts += 1
            if result == 100:
                current_node.wins += 1
            current_node = current_node.parent

    def actions(self, node):
        if not node.successors:
            return None
        best_child = max(node.successors, key=lambda child: child.wins / child.playouts if child.playouts != 0 else 0)
        return best_child.move
    
    def minimax_search(self):
        start_time = process_time()
        end_time = start_time + self.time_limit if self.time_limit is not None else None
        _, move = self.max_value(self.state, self.depth,-100000,100000,start_time,end_time)
        return move
    
    def max_value(self, state, depth,alpha,beta,start_time,end_time):
        move = None
        terminal, value = state.is_terminal()
        if terminal:
            return state.eval(), None
        elif (end_time is not None) :
            if process_time() - start_time >= end_time:
                return state.eval(), None
        elif depth == 0:
            return state.eval(), None
        v = -100000
        actions = state.actions()
        for action in actions: 
            new_state = state.result(action)
            v2, _ = self.min_value(new_state, depth - 1,alpha,beta,start_time,end_time)
            if v2 > v:
                v = v2
                move = action
            if v >= beta:
                return v, move
            alpha = max(alpha, v)
        return v, move
    
    def min_value(self, state, depth,alpha,beta,start_time,end_time):
        move = None
        terminal, value = state.is_terminal()
        if terminal:
            return state.eval(), None
        elif (end_time is not None) :
            if process_time() - start_time >= end_time:
                return state.eval(), None
        elif depth == 0:
            return state.eval(), None
        v = 100000
        actions = state.actions()
        for action in actions: 
            new_state = state.result(action)
            v2, _ = self.max_value(new_state, depth - 1,alpha,beta,start_time,end_time)
            if v2 < v:
                v = v2
                move = action
            if v <= alpha:
                return v, move
            beta = min(beta, v)
        return v, move
