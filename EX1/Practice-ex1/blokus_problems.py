from itertools import combinations

from board import Board
from search import SearchProblem
import util
import math


def calculate_generic_heuristic(state, problem, positions, dimension_factor):
    """
    Generic heuristic calculation function for both corners and cover problems.
    """
    uncovered_positions = count_uncovered_positions(state, positions)
    smallest_piece_size = find_smallest_piece_size(problem.piece_list.pieces)
    adjustment_factor = min(smallest_piece_size, (dimension_factor + 1) / 2.0)
    return adjustment_factor * uncovered_positions

def count_uncovered_positions(state, positions):
    """
    Count the number of uncovered positions (either corners or targets) on the board.
    """
    board_state = state.state
    uncovered = 0
    for pos_x, pos_y in positions:
        if board_state[pos_x][pos_y] == 0:  # this position is not covered
            continue
        uncovered += 1
    return uncovered

def find_smallest_piece_size(pieces):
    """
    Find the smallest piece size in terms of the number of tiles.
    """
    min_size = math.inf
    for piece in pieces:
        if piece.num_tiles < min_size:
            min_size = piece.num_tiles
    return min_size



class BlokusFillProblem(SearchProblem):
    """
    A one-player Blokus game as a search problem.
    This problem is implemented for you. You should NOT change it!
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return not any(state.pieces[0])

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, 1) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class BlokusCornersProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.expanded = 0
        self.expansion_count = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.corner_positions = [(0, 0), (board_h - 1, 0), (0, board_w - 1), (board_h - 1, board_w - 1)]
        self.piece_list = piece_list

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        corners = self.corner_positions
        for corner in corners:
            if state.state[corner[0]][corner[1]] == -1:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        total_cost = 0
        for action in actions:
            total_cost += action.piece.get_num_tiles()
        return total_cost


def blokus_corners_heuristic(state, problem):
    """
    Heuristic function for the BlokusCornersProblem.

    This heuristic must be consistent to ensure correctness. Firstly, aim for an
    admissible heuristic; most admissible heuristics will also be consistent.

    If A* search ever finds a solution worse than uniform cost search, your heuristic
    is not consistent and probably not admissible! Conversely, inadmissible or inconsistent
    heuristics may still find optimal solutions, so proceed with caution.
    """
    return calculate_generic_heuristic(state, problem, problem.corner_positions, min(problem.board.board_h,
                                                                                     problem.board.board_w))



class BlokusCoverProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.piece_list = piece_list

        self.min_target_distance = self.calculate_min_target_distance()

    def calculate_min_target_distance(self):
        """
        Calculate the minimum Manhattan distance between any two targets.
        """
        min_distance = math.inf
        num_targets = len(self.targets)
        for i in range(num_targets):
            for j in range(i + 1, num_targets):
                distance = self.manhattan_distance(self.targets[i], self.targets[j])
                if distance < min_distance:
                    min_distance = distance
        return min_distance

    @staticmethod
    def manhattan_distance(point1, point2):
        """
        Calculate the Manhattan distance between two points.
        """
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        targets = self.targets
        for target in targets:
            if state.state[target[0]][target[1]] == -1:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        total_cost = 0
        for action in actions:
            total_cost += action.piece.get_num_tiles()
        return total_cost


def blokus_cover_heuristic(state, problem):
    """
        we checked what is the smallest piece we have and checked the min distance between two targets in the problem.
        we returned the number of uncovered corners multiplied by the mult factor, which is the minimum of the two values
        mentioned above.
        This is a lower bound to the actual amount of tiles required to cover all targets,
        since if two targets can't be covered with one piece, they will take at least the minimum piece size for each
        target.
        """
    return calculate_generic_heuristic(state, problem, problem.targets, problem.min_target_distance)
