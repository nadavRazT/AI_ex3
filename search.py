"""
In search.py, you will implement generic search algorithms
"""
from collections import defaultdict

import numpy as np

import util
# from displays import GuiDisplay
import time


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current_ state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def draw_b(board, display):
    # todo delete
    dots = [(board.board_h - 1, board.board_w - 1), (0, board.board_w - 1), (board.board_h - 1, 0)]
    display.draw_board(board, dots=dots)
    input("press Enter: ")


def dfs_helper(node, visited_set, problem, stack, sol):
    for son in reversed(problem.get_successors(node)):
        if not son:
            return False, sol
        stack.append(son)
        sol.append(son[1])
        if problem.is_goal_state(son[0]):
            return True, sol
        # check legal
        state = son[0]
        if hash(state) not in visited_set:
            visited_set.add(hash(state))
            sol_flag, sol = dfs_helper(son[0], visited_set, problem, stack, sol)
            if sol_flag:
                return True, sol
        stack.pop()
        sol.pop()
    return False, sol


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    print("Start's successors:", problem.get_successors(problem.get_start_state()))
    """

    start_state = problem.get_start_state()
    stack = []
    visited_set = {hash(start_state)}
    # display = GuiDisplay(problem.board.board_w, problem.board.board_h, title='Intro to AI -- 67842 -- Ex1')
    sol = []
    sol_flag, sol = dfs_helper(start_state, visited_set, problem, stack, sol)
    if sol_flag:
        return sol
    return sol


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    queue = []
    visited_set = {hash(problem.get_start_state())}
    first_in_q = [(problem.get_start_state(), 0)]
    queue.append(first_in_q)
    ret = []
    while queue:
        path = queue.pop(0)
        s = path[-1]  #
        if problem.is_goal_state(s[0]):
            path.pop(0)
            ret = [tup[1] for tup in path]
            return ret
        for neighbour in problem.get_successors(s[0]):
            neighboard = neighbour[0]
            if hash(neighboard) not in visited_set:
                visited_set.add(hash(neighboard))
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
    return ret


def get_move_list(path, visited):
    return [visited[i][1] for i in path]


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    global_index = 0
    p_queue = util.PriorityQueue()
    start_state = problem.get_start_state()
    visited = [(start_state, None, 0, global_index)]
    state_set = {global_index: [(start_state, None, 0, global_index)]}
    p_queue.push(item=global_index, priority=0)
    while not p_queue.isEmpty():
        path = state_set[p_queue.pop()]
        node = path[-1]
        if problem.is_goal_state(node[0]):
            sol = [p[1] for p in path][1:]
            return sol
        for son in problem.get_successors(node[0]):
            global_index += 1
            if son and global_index not in state_set.keys():
                n = len(state_set)
                cost = son[2] + node[2]
                son_node = (son[0], son[1], cost, global_index)
                visited.append(son_node)
                new_path = list(path)
                new_path.append(son_node)
                state_set[global_index] = new_path
                p_queue.push(item=global_index, priority=cost)
    return []


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def reconstruct_path(hash_path, state_set):
    return [state_set[h][1] for h in hash_path]


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    global_index = 0
    g_score, f_score = {}, {}
    g_score, f_score = defaultdict(lambda: np.inf, g_score), defaultdict(lambda: np.inf, f_score)
    start = (problem.get_start_state(), None, 0)
    openset = util.PriorityQueue()
    hashed_openset = {global_index}
    g_score[global_index] = 0
    f_score[global_index] = heuristic(start[0], problem)
    openset.push([global_index], f_score[global_index])
    state_set = {global_index: start}
    n = 0

    while not openset.isEmpty():
        hash_path = openset.pop()
        curr = state_set[hash_path[-1]]
        curr_index = hash_path[-1]
        if problem.is_goal_state(curr[0]):
            return reconstruct_path(hash_path[1:], state_set)
        neighbors = problem.get_successors(curr[0])
        for neighbor in neighbors:
            global_index += 1
            state_set[global_index] = neighbor
            tent_g_score = g_score[curr_index] + neighbor[2]
            if tent_g_score < g_score[global_index]:
                g_score[global_index] = tent_g_score
                f_score[global_index] = tent_g_score + heuristic(neighbor[0], problem)
                if global_index not in hashed_openset:
                    hashed_openset.add(global_index)
                    new_path = list(hash_path)
                    new_path.append(global_index)
                    openset.push(new_path, f_score[global_index])
    return None


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
