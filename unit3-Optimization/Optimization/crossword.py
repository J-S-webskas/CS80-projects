class Variable():

    ACROSS = "across"
    DOWN = "down"

    def __init__(self, i, j, direction, length):
        """Create a new variable with starting point, direction, and length."""
        self.i = i 
        self.j = j
        self.direction = direction
        self.length = length
        self.cells = []  # A list of (row, column) tuples representing all grid positions occupied by the word
        for k in range(self.length):
            self.cells.append(
                (self.i + (k if self.direction == Variable.DOWN else 0),  # If DOWN, increment row
                 self.j + (k if self.direction == Variable.ACROSS else 0))  # If ACROSS, increment column
            )

    def __hash__(self):
        return hash((self.i, self.j, self.direction, self.length))

    def __eq__(self, other):
        return (
            (self.i == other.i) and
            (self.j == other.j) and
            (self.direction == other.direction) and
            (self.length == other.length)
        )

    def __str__(self):
        return f"({self.i}, {self.j}) {self.direction} : {self.length}"

    def __repr__(self):
        direction = repr(self.direction)
        return f"Variable({self.i}, {self.j}, {direction}, {self.length})"


class Crossword():

    def __init__(self, structure_file, words_file):  # layout and list of words
        # Determine structure of crossword
        """
        open(structure_file) opens the file in read mode (default mode)
        as f assigns the file object to variable f

        with: Creates a context where:
        The file is automatically opened when entering the block
        The file is automatically closed when exiting the block (even if an error occurs)
        This is safer than manually opening/closing files because it guarantees proper cleanup.
        (block = indented code section underneath with)

        f.read():
        Reads the entire contents of the file as a single string
        Includes all characters, including newlines (\n)
        strucutre0 becomes: '#___#\n#_##_\n#_##_\n#_##_\n#____'

        .splitlines():
        A string method that splits the content at line boundaries
        Returns a list where each element is one line from the file
        Unlike .split('\n'), it handles different line endings consistently (\n, \r, \r\n)
        Removes the newline characters from each line
        structure0 become ['#___#', '#_##_', '#_##_', '#_##_', '#____']
        """
        with open(structure_file) as f:
            contents = f.read().splitlines()  # Forms a string with \n separating rows + splits at `\n` and removes them
            self.height = len(contents)
            self.width = max(len(line) for line in contents)

            self.structure = []  # 2D list: True at (i, j) if cell _ , False otherwise
            for i in range(self.height):
                row = []
                for j in range(self.width):
                    if j >= len(contents[i]):
                        row.append(False)
                    elif contents[i][j] == "_":
                        row.append(True)
                    else:
                        row.append(False)
                self.structure.append(row)
        # First block ends here
        # Save vocabulary list/ set of all valid words
        with open(words_file) as f:  # Opens the file specified by words_file in read mode
            self.words = set(f.read().upper().splitlines())  # .upper() Converts all letters in the file to uppercase

        # Determine variable set
        self.variables = set()  # set of all of the variabe objects in the puzzle
        for i in range(self.height):
            for j in range(self.width):

                # Vertical words
                starts_word = (
                    self.structure[i][j]
                    and (i == 0 or not self.structure[i - 1][j])
                )
                if starts_word:
                    length = 1
                    for k in range(i + 1, self.height):
                        if self.structure[k][j]:
                            length += 1
                        else:
                            break
                    if length > 1:
                        self.variables.add(Variable(
                            i=i, j=j,
                            direction=Variable.DOWN,
                            length=length
                        ))

                # Horizontal words
                starts_word = (
                    self.structure[i][j]
                    and (j == 0 or not self.structure[i][j - 1])
                )
                if starts_word:
                    length = 1
                    for k in range(j + 1, self.width):
                        if self.structure[i][k]:
                            length += 1
                        else:
                            break
                    if length > 1:
                        self.variables.add(Variable(
                            i=i, j=j,
                            direction=Variable.ACROSS,
                            length=length
                        ))

        # Compute overlaps for each word
        # For any pair of variables v1, v2, their overlap is either:
        #    None, if the two variables do not overlap; or
        #    (i, j), where v1's ith character overlaps v2's jth character
        self.overlaps = dict()
        for v1 in self.variables:
            for v2 in self.variables:
                if v1 == v2:
                    continue
                cells1 = v1.cells  # index squares of word1
                cells2 = v2.cells  # index square of word2
                intersection = set(cells1).intersection(cells2)  # The most efficient way (O(min(n,m)) for finding common elements between collections
                if not intersection:  # If no overlap, return None
                    self.overlaps[v1, v2] = None
                else:
                    intersection = intersection.pop()  # two variables can intersect at most once
                    self.overlaps[v1, v2] = (
                        cells1.index(intersection),
                        cells2.index(intersection)
                    )

    def neighbors(self, var):
        """Given a variable, return set of overlapping variables."""
        # crossword.neighbors(v1) will return a set of all of the variables that are neighbors to the variable v1.
        return set(
            v for v in self.variables
            if v != var and self.overlaps[v, var]
        )
