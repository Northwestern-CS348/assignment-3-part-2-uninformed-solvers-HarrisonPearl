
from solver import *
import queue


class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        # If we are already at the victory state just return true

        #print(self.gm.getGameState())

        if self.currentState.state == self.victoryCondition:
            return True

        # Add all possible moves that can be taken from the given state to the states list of children
        # Iterate through all moves
        posmoves = self.gm.getMovables()
        curr = self.currentState
        if posmoves:
            for move in posmoves:
                self.gm.makeMove(move)
                child_state = GameState(self.gm.getGameState(), curr.depth + 1, move)
                curr.children.append(child_state)
                child_state.parent = curr
                self.gm.reverseMove(move)
            for child in curr.children:
                if child not in self.visited:
                    self.visited[child] = True
                    self.gm.makeMove(child.requiredMovable)
                    self.currentState = child

                    break
        else:
            self.gm.reverseMove(self.currentState.requiredMovable)

        return False




class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.path = dict()
        self.Q = queue.Queue()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        #print(self.gm.getGameState())

        # print(self.currentState.state)
        if self.currentState.state == self.victoryCondition:
            return True

        if self.currentState.depth == 0:
            self.path[self.currentState] = []

        # Add all possible moves that can be taken from the given state to the states list of children
        posmoves = self.gm.getMovables()
        curr = self.currentState
        self.visited[curr] = True

        # add children
        if posmoves:
            for move in posmoves:
                self.gm.makeMove(move)
                child_state = GameState(self.gm.getGameState(), curr.depth + 1, move)
                if child_state not in self.visited:
                    self.visited[child_state] = True
                    self.Q.put(child_state)
                    self.path[child_state] = self.path[curr].copy()
                    self.path[child_state].append(child_state)
                self.gm.reverseMove(move)

        path_to_root = self.path[self.currentState]
        path_to_root.reverse()
        self.currentState = self.Q.get()
        path_to_next = self.path[self.currentState]

        for n in path_to_root:
            self.gm.reverseMove(n.requiredMovable)

        for p in path_to_next:
            self.gm.makeMove(p.requiredMovable)

        if self.currentState.state == self.victoryCondition:
            return True

        return False


