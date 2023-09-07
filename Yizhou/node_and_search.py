'''
Define nodes of search tree and vanilla bfs search algorithm

Author: Tony Lindgren
'''
from queue import PriorityQueue
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
        self.heuristic = 0
        if parent:
            self.depth = parent.depth + 1 

    def goal_state(self):
        return self.state.check_goal()

    def set_heuristic(self, heuristic=0):
        if heuristic== 0:
            self.heuristic=0
        elif heuristic==1:
            self.heuristic=1
    def successor(self):

        successors = queue.Queue()
        for action in self.state.action:
            child = self.state.move(action)
            if child != None:
                childNode = Node(child, self.cost + 1, self, action)
                successors.put(childNode)

        return successors

    def __lt__(self, other):
        # Compare based on the h1 heuristic value
        if self.heuristic == 0:
            return self.state.h1() < other.state.h1()
        elif self.heuristic == 1:
            return self.state.h2() < other.state.h2()

    def __le__(self, other):
        # Compare based on the h1 heuristic value
        if self.heuristic == 0:
            return self.state.h1() <= other.state.h1()
        elif self.heuristic == 1:
            return self.state.h2() <= other.state.h2()

    def pretty_print_solution(self, verbose=False):
        if self.parent == None:
            if verbose:
                self.state.pretty_print()
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
                if next_node.state.state not in [node.state.state for node in frontier_copy.queue]:
                    frontier.put(next_node)
                    frontier_copy.put(next_node)

    def dfs(self, depth_limit=None, verbose=False, statistics=False):
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
                if (next_node.state.state not in [node.state.state for node in frontier_copy] and (depth_limit == None or next_node.depth <= depth_limit)):
                    frontier.append(next_node)
                    frontier_copy.append(next_node)

    def ids(self, verbose=False, statistics=False):
        start_time = time.process_time()
        depth_limit = 0
        while True:
            result = self.dfs(depth_limit, verbose, False)

            if result != None:
                end_time = time.process_time()
                self.time_cost = end_time - start_time
                result.pretty_print_solution(verbose)
                if statistics:
                    self.statistics()
                return result
            depth_limit += 1

    def greedy_search(self, heuristic=0, depth_limit=None, verbose=False, statistics=False):
        start_time = time.process_time()
        frontier = PriorityQueue()
        frontier_copy = queue.Queue()
        self.start.set_heuristic(heuristic)
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
                next_node = successor.get()
                self.search_cost = self.search_cost + 1
                if (next_node.state.state not in [node.state.state for node in frontier_copy.queue] and (depth_limit == None or next_node.depth <= depth_limit)):
                    next_node.set_heuristic(heuristic)
                    frontier.put(next_node)
                    frontier_copy.put(next_node)

    def statistics(self):
        depth = self.goal.depth
        search_cost = self.search_cost
        cost_for_solution = self.goal.cost
        cpu_time_consumed = self.time_cost
        effective_branching_factor = self.goal.cost ** (1 / self.goal.depth)
        print("Elapsed time (s): ", cpu_time_consumed)
        print("Solution found at depth: ", depth)
        print("Number of nodes explored: ", search_cost)
        print("Cost of solution: ", cost_for_solution)
        print("Estimated effective branching factor: ", effective_branching_factor)
