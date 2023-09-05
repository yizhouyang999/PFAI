'''
Define nodes of search tree and vanilla bfs search algorithm

Author: Tony Lindgren
'''

import queue
import time

class Node:
    '''
    This class defines nodes in search trees. It keep track of: 
    state, cost, parent, action, and depth 
    '''
    def __init__(self, state, cost=0, parent=None, action=None):
        self.parent = parent
        self.state = state
        self.action = action
        self.cost = cost
        self.depth = 0
        if parent:
            self.depth = parent.depth + 1 

    def goal_state(self):
        return self.state.check_goal()
    
    def successor(self):

        successors = queue.Queue()
        for action in self.state.action:
            child = self.state.move(action)
            if child != None:
                childNode = Node(child, self.cost + 1, self, action)
                successors.put(childNode)

        return successors

    def pretty_print_solution(self, verbose=False):
        if self.parent == None:
            if verbose:
                self.state.pretty_print()
            print("Start state")
        else:
            self.parent.pretty_print_solution(verbose)
            if verbose:
                self.state.pretty_print()
            print("Action: ", self.action)
             
class SearchAlgorithm:
    '''
    Class for search algorithms, call it with a defined problem 
    '''
    def __init__(self, problem):
        self.start = Node(problem)
        self.goal = None
        self.time_cost = 0
        self.search_cost = 0
        
    def bfs(self, verbose=False, statistics=False):
        start_time = time.process_time()
        frontier = queue.Queue()
        frontier_copy=queue.Queue()
        frontier.put(self.start)
        frontier_copy.put(self.start)
        stop = False
        while not stop:
            if frontier.empty():
                return None
            curr_node = frontier.get()
            if curr_node.goal_state():
                self.goal = curr_node
                stop = True
                end_time = time.process_time()
                self.time_cost = end_time - start_time
                self.search_cost = self.search_cost + 1
                curr_node.pretty_print_solution(verbose)
                if statistics:
                    self.statistics()
                return curr_node
                        
            successor = curr_node.successor()
            while not successor.empty():
                next_node=successor.get()
                self.search_cost=self.search_cost+1
                if next_node.state not in [node.state for node in frontier_copy.queue]:
                    frontier.put(next_node)
                    frontier_copy.put(next_node)

    def dfs(self, verbose=False, statistics=False):
        start_time = time.process_time()
        frontier = []
        frontier_copy = []
        frontier.append(self.start)
        frontier_copy.append(self.start)
        stop = False
        while not stop:
            if not frontier:
                return None
            curr_node = frontier.pop()
            if curr_node.goal_state():
                self.goal = curr_node
                stop = True
                end_time = time.process_time()
                self.time_cost = end_time - start_time
                self.search_cost = self.search_cost + 1
                curr_node.pretty_print_solution(verbose)
                if statistics:
                    self.statistics()
                return curr_node

            successor = curr_node.successor()
            while not successor.empty():
                next_node = successor.get()
                self.search_cost = self.search_cost + 1
                if next_node.state not in [node.state for node in frontier_copy]:
                    frontier.append(next_node)
                    frontier_copy.append(next_node)


    def statistics(self):
        depth = self.goal.depth
        search_cost = self.search_cost
        cost_for_solution = self.goal.cost
        cpu_time_consumed = self.time_cost
        effective_branching_factor = self.goal.cost ** (1 / self.goal.depth)
        print("depth: ", depth)
        print("search cost: ", search_cost)
        print("cost for solution: ", cost_for_solution)
        print("cpu time consumed: ", cpu_time_consumed)
        print("effective branching factor: ", effective_branching_factor)
