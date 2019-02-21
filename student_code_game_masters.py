from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        res_tup = []
        for i in range(1, 4):
            peg_tup = []
            bindings = self.kb.kb_ask(parse_input("fact: (on ?x peg" + str(i) + ")"))
            if bindings:
                for binding in bindings:
                    disk_str = binding['?x']
                    disk_int = int(disk_str[-1])
                    peg_tup.append(disk_int)
            peg_tup.sort()
            res_tup.append(tuple(peg_tup))

        return tuple(res_tup)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        # Student code goes here
        disk = str(movable_statement.terms[0])
        pegi = str(movable_statement.terms[1])
        pegf = str(movable_statement.terms[2])

        # if pegf has a top, it is no longer the top, and disk is stacked on it
        # if pegf is empty, it is no longer empty
        top_bindings = self.kb.kb_ask(parse_input("fact: (top " + " ?x" + " " + pegf + ")"))
        if top_bindings:
            old_top = top_bindings[0]
            self.kb.kb_retract(parse_input("fact: (top " + old_top['?x'] + " " + pegf + ")"))
            self.kb.kb_assert(parse_input("fact: (stacked " + disk + " " + old_top['?x'] + ")"))
        else:
            self.kb.kb_retract(parse_input("fact: (empty " + pegf + ")"))

        # disk is no longer top of peg i, it it now top of pegf
        self.kb.kb_retract(parse_input("fact: (top " + disk + " " + pegi + ")"))
        self.kb.kb_assert(parse_input("fact: (top " + disk + " " + pegf + ")"))

        # disk is no longer on peg i, it is on pegf
        self.kb.kb_retract(parse_input("fact: (on " + disk + " " + pegi + ")"))
        self.kb.kb_assert(parse_input("fact: (on " + disk + " " + pegf + ")"))

        # if the disk was on top of another disk, that disk becomes new top of pegi, else pegi is empty
        stack_bindings = self.kb.kb_ask(parse_input("fact: (stacked " + disk + " ?y)"))
        if stack_bindings:
            new_top = stack_bindings[0]
            self.kb.kb_retract(parse_input("fact: (stacked " + disk + " " + new_top['?y'] + ")"))
            self.kb.kb_assert(parse_input("fact: (top " + new_top['?y'] + " " + pegi + ")"))
        else:
            self.kb.kb_assert(parse_input("fact: (empty " + pegi + ")"))







    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        # Student code goes here
        # fact: (x tile1 pos1)
        # fact: (y tile1 pos1)

        res_tup = []
        for i in range(1, 4):
            peg_tup = [99, 99, 99]
            bindings = self.kb.kb_ask(parse_input("fact: (y ?tile pos" + str(i) + ")"))
            if bindings:
                for binding in bindings:
                    tile_str = binding['?tile']
                    if tile_str == "empty":
                        tile_int = -1
                    else:
                        tile_int = int(tile_str[-1])
                    xpos_bindings = self.kb.kb_ask(parse_input("fact: (x " + tile_str + " ?y)"))
                    xpos_binding = xpos_bindings[0]
                    xpos_string = xpos_binding['?y']
                    xpos_int = int(xpos_string[-1]) - 1
                    peg_tup[xpos_int] = tile_int
            res_tup.append(tuple(peg_tup))

        return tuple(res_tup)

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        tile = str(movable_statement.terms[0])
        xi = str(movable_statement.terms[1])
        yi = str(movable_statement.terms[2])
        xf = str(movable_statement.terms[3])
        yf = str(movable_statement.terms[4])

        self.kb.kb_retract(parse_input("fact: (x " + tile + " " + xi + ")"))
        self.kb.kb_retract(parse_input("fact: (y " + tile + " " + yi + ")"))

        self.kb.kb_retract(parse_input("fact: (x empty " + xf + ")"))
        self.kb.kb_retract(parse_input("fact: (y empty " + yf + ")"))

        self.kb.kb_assert(parse_input("fact: (x empty " + xi + ")"))
        self.kb.kb_assert(parse_input("fact: (y empty " + yi + ")"))

        self.kb.kb_assert(parse_input("fact: (x " + tile + " " + xf + ")"))
        self.kb.kb_assert(parse_input("fact: (y " + tile + " " + yf + ")"))



    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
