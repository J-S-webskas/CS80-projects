import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines

    def main():
        m = MinesweeperAI
        m.add_knowledge((0, 1), 1)


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        mines = set()
        if len(self.cells) == self.count:
            for cell in self.cells:
                mines.add(cell)
        return mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safe = set()
        if self.count == 0:  # If all the cells are safe
            for cell in self.cells:
                safe.add(cell)
        return safe

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:  # Checks THIS sentence's specific cells
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)

        """
        Only add neighbors if they are not in self.safes/mines
        -not safes or mines by pre-evaluating for count and length of neighbors
        -subtract count to avoid counting mines already determiend
        """

        neighbors = set()  # Set of tuples
        for diri in range(max(0, cell[0] - 1), min(cell[0] + 1, self.height)):
            for dirj in range(max(0, cell[1] - 1), min(cell[1] + 1, self.width)):
                i = cell[0] + diri
                j = cell[1] + dirj
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) not in self.safes and (i, j) not in self.mines:
                        if count == 0:
                            self.mark_safe((i, j))
                        else:
                            neighbors.add((i, j))
                    elif (i, j) in self.mines:
                        count -= 1
                        
        if len(neighbors) == count:
            for cell in neighbors:
                self.mark_mine(cell)
        elif count > 0:  # sentences are not pure safes or mines
            self.knowledge.append(Sentence(neighbors, count))

        """
        Filter all sentences for obvious all mines and safes
        and mark them until no more can be inferred from this process.
        This clears up lots of sentences that can be simplified.

        From known_mines and known_safes, loop through all sentence, if there are any sentences purely mine or safe,
        (that is either present or derived from subtracting subsets)
        simplify all sentences by calling mark_mine or mark_safe (in this class) that updates all sentences in the sentencec class

        After simplifying all sentences, simplify subsets to derive new information
        and continue the process (always good to keep simplifying the obvious mines or safes until clean)
        This way is most efficient.
        """

        changed = True
        while changed:
            changed = False
            for sentence in self.knowledge:
                set_of_pure_mines = sentence.known_mines()
                for mine in set_of_pure_mines:
                    if mine not in self.mines:
                        self.mark_mine(mine)
                        changed = True

                set_of_pure_safes = sentence.known_safes()
                for safe in set_of_pure_safes:
                    if safe not in self.safes:
                        self.mark_safe(safe)
                        changed = True
            """
            Nested for loop compares all pairs in sentence but not efficient
            An issue: creating new subsets have two types:
            1. empty
            2. not empty and is subset

            an empty set will be a subset of all sets. So, if set - empty-set, it will create 
            a duplicate of the set (distinct in memory but containing the same value).
            So this will lead to processing more sentences than necessary->checked out after 60 seconds

            In python, a for loop keeps track of the number of indexes the original list has.
            So, the iterator does not iterate over new elements that are added to the end of the original list.
            Thus, even without copying self.knowledge, this is will not cause an error unlike 
            modifying over iteration.
            """
            for i, s1 in enumerate(self.Knowledge):
                for j, s2 in enumerate(self.Knowledge[i + 1:]):
                    newSent = None
                    if s1.cells.issubset(s2.cells) and s1:  # and s1 prevents empty subset
                        newCells = s2.cells - s1.cells
                        newCount = s2.count - s1.count
                        changed = True
                        newSent = Sentence(newCells, newCount)
                    if s2.cells.issubset(s1.cells) and s2:
                        newCells = s1.cells - s2.cells
                        newCount = s1.count - s2.count
                        changed = True
                        newSent = Sentence(newCells, newCount)
                    if newSent and newSent not in self.knowledge:  # newSent not in self.knowledge does not prevent dplicate sentences in the empty subset way
                        self.knowledge.append(newSent)  # Adds to the end
                        changed = True

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        random_moves = [(i, j)
                        for i in range(self.height)
                        for j in range(self.width)
                        if (i, j) not in self.moves_made and (i, j) not in self.mines]
        
        return random.choice(random_moves) if len(random_moves >= 1) else None

