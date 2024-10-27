"""
In search.py, you will implement generic search algorithms
"""

import util


class SearchNode:
    def __init__(self, state, actions, cost):
        """
        Initializes a SearchNode with the specified state, actions, and cost.

        Parameters:
        -----------
        state : object
            The state of the node in the search problem.

        actions :
            A list of actions taken to reach this node from the start state.

        cost :t
            The cost to reach this node from the start state.
        """
        self.state = state
        self.actions = actions
        self.cost = cost

    def __lt__(self, other):
        """
        Compares this SearchNode with another SearchNode based on their costs.

        Parameters:
        -----------
        other : SearchNode
            Another SearchNode to compare against.

        Returns:
        --------
        bool
            True if this SearchNode's cost is less than the other SearchNode's cost, False otherwise.
        """
        return self.cost < other.cost


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
        successor to the current state, 'action' is the action
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


def depth_first_search(search_problem):
    # Stack for holding the nodes to visit, initialized with the start state and an empty path
    stack = util.Stack()
    stack.push((search_problem.get_start_state(), []))

    # Set for tracking visited nodes to avoid revisits and loops
    visited = set()

    while not stack.isEmpty():
        current_state, path = stack.pop()

        # Check if the current state is the goal state
        if search_problem.is_goal_state(current_state):
            return path  # Return the path that led to the goal state

        # If the state hasn't been visited, process its successors
        if current_state not in visited:
            visited.add(current_state)
            # Explore the successors
            for successor, action, step_cost in search_problem.get_successors(current_state):
                if successor not in visited:
                    # Append the current action to the path and push the successor to the stack
                    stack.push((successor, path + [action]))


def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """

    # Initialize the frontier using the initial state of the problem
    queue = util.Queue()
    start_state = problem.get_start_state()
    queue.push((start_state, []))  # Push the initial state and the path to reach it

    # Initialize the explored set to keep track of visited nodes
    visited = set()

    while not queue.isEmpty():
        current_state, path = queue.pop()

        # Check if the current state is a goal state
        if problem.is_goal_state(current_state):
            return path  # Return the path that led to the goal

        # Only process the current state if it has not been visited
        if current_state not in visited:
            visited.add(current_state)

            # Expand the current state to its successors
            for successor, action, step_cost in problem.get_successors(current_state):
                if successor not in visited:
                    # Create a new path to the successor including the current action
                    new_path = path + [action]
                    # Push the successor and the new path to the queue
                    queue.push((successor, new_path))


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """

    # Initialize the priority queue
    frontier = util.PriorityQueue()
    # Start with the initial state
    start_node = SearchNode(problem.get_start_state(), [], 0)
    frontier.push(start_node, start_node.cost)
    # Initialize an empty set for explored nodes
    explored = set()

    while not frontier.isEmpty():
        # Get the node with the lowest cost
        current_node = frontier.pop()

        # Check if the state is the goal state
        if problem.is_goal_state(current_node.state):
            return current_node.actions

        # If the state has not been explored yet
        if current_node.state not in explored:
            explored.add(current_node.state)

            # Expand the node
            for next_state, action, step_cost in problem.get_successors(current_node.state):
                new_cost = current_node.cost + step_cost
                new_actions = current_node.actions + [action]
                new_node = SearchNode(next_state, new_actions, new_cost)
                frontier.push(new_node, new_node.cost)

    # If no solution is found, return failure
    return []


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """

    # Initialize the priority queue
    frontier = util.PriorityQueue()
    # Start with the initial state
    start_state = problem.get_start_state()
    start_node = SearchNode(start_state, [], 0)
    frontier.push(start_node, start_node.cost + heuristic(start_state, problem))
    # Initialize an empty set for explored nodes
    explored = set()

    while not frontier.isEmpty():
        # Get the node with the lowest combined cost and heuristic
        current_node = frontier.pop()

        # Check if the state is the goal state
        if problem.is_goal_state(current_node.state):
            return current_node.actions

        # If the state has not been explored yet
        if current_node.state not in explored:
            explored.add(current_node.state)

            # Expand the node
            for next_state, action, step_cost in problem.get_successors(current_node.state):
                new_cost = current_node.cost + step_cost
                new_actions = current_node.actions + [action]
                new_node = SearchNode(next_state, new_actions, new_cost)
                frontier.push(new_node, new_node.cost + heuristic(next_state, problem))

    # If no solution is found, return failure
    return []


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
