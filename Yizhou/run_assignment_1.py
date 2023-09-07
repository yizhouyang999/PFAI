'''
Define problem and start execution of search problems

Author: Tony Lindgren
'''

from missionaries_and_cannibals import MissionariesAndCannibals
from eight_puzzle import EightPuzzle
from node_and_search import SearchAlgorithm

init_state = [[0, 0], 'r', [3, 3]] 
goal_state = [[3, 3], 'l', [0, 0]]
ep_init_state = [[7, 2, 4], [5, 'e', 6], [8, 3, 1]]

def main():
    mc = MissionariesAndCannibals(init_state, goal_state)
    ep= EightPuzzle(ep_init_state)
    sa = SearchAlgorithm(mc)
    ep_sa=SearchAlgorithm(ep)
    # print('BFS')
    # print('Start state: ')
    # mc.pretty_print()
    # goal_node = sa.bfs(verbose=False, statistics=True)
    # print('goal state: ')
    # goal_node.state.pretty_print()
    # goal_node.pretty_print_solution(verbose=False)
    # sa.statistics()
    goal_node=ep_sa.greedy_search(heuristic=1, verbose=False, statistics=True)
if __name__ == "__main__":
    main()