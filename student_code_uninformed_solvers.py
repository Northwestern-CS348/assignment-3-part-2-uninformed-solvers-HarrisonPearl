
from solver import *

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




class SolverBFS(UninformedSolver):
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
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        return True
