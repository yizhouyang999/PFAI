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
    goal_node = sa.dfs(verbose=False, statistics=True)
    goal_node = sa.bfs(verbose=False, statistics=True)
    goal_node = sa.ids(verbose=False, statistics=True)
    goal_node = ep_sa.greedy_search(heuristic=0, verbose=False, statistics=True)
    goal_node = ep_sa.greedy_search(heuristic=1, verbose=False, statistics=True)
    goal_node = ep_sa.a_star(heuristic=0, verbose=False, statistics=True)
    goal_node = ep_sa.a_star(heuristic=1, verbose=False, statistics=True)

    # Try the uninformed search
    # goal_node = ep_sa.bfs(verbose=False, statistics=True)
    # goal_node = ep_sa.dfs(verbose=False, statistics=True)
    # goal_node = ep_sa.ids(verbose=False, statistics=True)
if __name__ == "__main__":
    main()