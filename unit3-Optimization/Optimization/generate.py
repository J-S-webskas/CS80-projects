import sys

from crossword import *
from collections import deque


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate. CPS = constraint satisfaction problem
        domains = a dictionary that maps variables to a set of possible words the variable might take on as a value
        """
        self.crossword = crossword  # Instance of Crossword class, accessible to all its functions
        self.domains = {
            var: self.crossword.words.copy()  # Keys: Variables (word slots) from self.crossword.variables
            for var in self.crossword.variables  # Values: A copy of the full word list (self.crossword.words) that could fit in that variable.
        }

    def letter_grid(self, assignment):
        """
        Generates/returns a 2D array/list of all characters in their appropriate positions for a given assignment
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal. Shows the current state of the puzzle
        assignemnt is a dictionary mapping variables/positions to words
        Python print adds a \n by default
        end="" Prevents automatic newlines after printing (keeping the row together)
        """
        letters = self.letter_grid(assignment)  # Converts assignment to a 2D grid of characters
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:  # If cell is a letter square
                    print(letters[i][j] or " ", end="")  # Prints letter if present or  " " if empty cell
                else:  # If cell is blocked
                    print("█", end="")  # Print a block character
            print()  # Adds a newline after each complete row is printed

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file. PNG
        Uses the Pillow library from the Python Imaging Library (PIL) for drawing.
        
        Pillow's core functions:
        Image.new(): Creates a blank image canvas.
        ImageDraw.Draw(): Draws shapes (rectangles) and text.
        ImageFont.truetype(): Loads custom fonts for letter styling. Loads a .ttf (TrueType font) file.
        img.save(): Exports the image to a file (ex. PNG).

        pip3 is the Python package installer for Python 3. Stands for "Pip Installs Packages" (the 3 specifies Python 3).
        RGBA: Color format with transparency (Red, Green, Blue, Alpha).
        Canvas: A drawable image created via Image.new().
        Drawing: Use ImageDraw.Draw() to add shapes/text, then save/show.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100  # each square is 100x100 pixels
        cell_border = 2  # border thickness inside each cell
        interior_size = cell_size - 2 * cell_border  # usable space inside a cell: 100 - 2*2
        letters = self.letter_grid(assignment)  # 2D array after current assignment

        """
        Create a blank canvas
        RGBA is a color model that defines colors using four components:
            R (Red): Intensity of red (0–255)
            G (Green): Intensity of green (0–255)
            B (Blue): Intensity of blue (0–255)
            A (Alpha): Opacity (0 = transparent, 255 = opaque)
        "RGB" (no transparency)
        "L" (grayscale).

        A canvas is a digital "drawing board"
        Created using Image.new(): a blank image (canvas) with specified dimensions and background color.
            Acts like an empty pixel grid.
        ImageDraw.Draw(): Attaches a "drawing tool" (draw) to the canvas. Lets you add shapes/text using methods:
            draw.rectangle([(10, 10), (100, 100)], fill="red")  # Draw a red square
            draw.text((50, 50), "Hello", fill="black")          # Add text
            etc.
        """
        img = Image.new(  # Makes a black background image with matching dimensions
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        """
        Path to the font file (relative to the project root)
        Font size in points converts this to pixels based on the image’s DPI (default is 72 DPI, so 80pt ≈ 80px at 72 DPI)
        DPI (Dots Per Inch): Measures how many pixels fit into one inch of an image
        Default in Pillow: 72 DPI (common screen resolution).
            At 72 DPI, 1 point = 1 pixel (ex. 80pt font ≈ 80px tall).
        Why it matters: Higher DPI = sharper text but larger file size (critical for print vs. screen).
        """
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)  # Loads a font (size 80) for displaying letters.
        draw = ImageDraw.Draw(img)  # The blank image canvas created earlier (Image.new()

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                """
                A list of two tuples [(x1, y1), (x2, y2)] defining the rectangle’s bounds.
                Top-Left Corner (x1, y1):
                j * cell_size → Left edge of the cell (column-based).
                + cell_border → Moves inward by the border width (to avoid overlapping borders).
                Same logic applies for y1 (row-based).

                Bottom-Right Corner (x2, y2):
                (j + 1) * cell_size → Right edge of the cell.
                cell_border → Moves inward by the border width.
                Ensures the rectangle stops before the adjacent cell’s border.
                """
                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    # Fills the rectangle with white color. Creates the blank/letter cells in the crossword grid 
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:  # If a letter exists in this cell
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),  # X-coordinate (centered)
                             rect[0][1] + ((interior_size - h) / 2) - 10),  # Y-coordinate (centered)
                            letters[i][j], fill="black", font=font  # The character to draw, color, uses the loaded OpenSans font
                        )

        img.save(filename)  # Exports the final image to filename (output.png)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency() # node consistency: ensure that every value in a variable’s domain satisfy the unary constraints
        self.ac3()  # arc consistency: ensure binary constraints
        return self.backtrack(dict())  # backtrack on an initially empty assignment (empty dict()) to try to calculate a solution to the problem.

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # var maps to a SET of values. So, cannot just do key: value
        # {value for value in self.domains[var] if var.length == len(value)} = inner loop
        # Since if clause always follows the for loop it applies to
        # for var in self.domains = outer loop
        self.domains = {var: {value for value in self.domains[var] 
                              if var.length == len(value)}
                        for var in self.domains}

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Replace is faster than remove
        overlap = self.crossword.overlaps[x, y]  # Overlapping index of x and y
        valid = set()
        if not overlap:
            return False
        for wordx in self.domains[x]:  # compares one value of x with all possible values of y
            for wordy in self.domains[y]:
                # if a value of var x matches at least 1 value of var y at their overlapping index, that value of x is valid
                if wordx[overlap[0]] == wordy[overlap[1]]:
                    valid.add(wordx)
                    break
        if len(self.domains[x]) != len(valid):
            self.domains[x] = valid
            return True
        return False


    def ac3(self, arcs=None):  # None by default
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            queue = deque((var1, var2) 
                    for var1 in self.crossword.variables 
                    for var2 in self.crossword.neighbors(var1))
        else:
            queue = deque(arcs)

        while queue:
            x, y = queue.popleft()  # deque is fast for retrieving elements
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x)-{y}:
                    queue.append((z, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return len(assignment) == len(self.crossword.variables)
        
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # not all variables will necessarily be present in the assignment
        if len(assignment.values()) != len(set(assignment.values())):  # Distinct values
            return False
        for key, value in assignment.items():
            if len(value) != key.length:  # Length same
                return False
    
        for (var1, var2) in self.crossword.overlaps.keys():
            if self.crossword.overlaps[var1, var2]:  # self.crossword.overlaps[var1, var2] can be None
                i, j = self.crossword.overlaps[var1, var2]
                if var1 in assignment and var2 in assignment:  # Check
                    if assignment[var1][i] != assignment[var2][j]:
                        return False
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # If var was assigned this word, count how many words in the neighbor's domain can be eliminated
        elimination_count = self.count_elimination(var, assignment)
        return sorted(self.domains[var], key=lambda var: elimination_count[var])


    def count_elimination(self, var, assignment):
        elimination_count = {key: 0 for key in self.domains[var]}
        overlap = self.crossword.overlaps
        for val in self.domains[var]:  # Values of var
            for neighbor in self.crossword.neighbors(var):  # Neighboring variables of var
                if neighbor in assignment: 
                    continue
                i, j  = overlap[var, neighbor]
                for val_n in self.domains[neighbor]: # Values of the neighbor variable
                    if val[i] != val_n[j]:  # If the current value's overlapping index with value of neighbor is not the same letter
                        elimination_count[val] += 1  # Can eliminate this word

        return elimination_count


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = []
        for var in self.crossword.variables:
            if var not in assignment:
                # Variable, length of values (ascending), size of neighbors (descending)
                unassigned.append((var, len(self.domains[var]), len(self.crossword.neighbors(var))))
        unassigned.sort(key=lambda x: (x[1], -x[2]))
        return unassigned[0][0]


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment): 
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result != None:
                    return result
                else:
                    assignment.pop(var)
        return None
    

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
