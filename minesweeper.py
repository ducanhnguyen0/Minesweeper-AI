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
        return self.cells if len(self.cells) == self.count and self.count != 0 else None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.cells if self.count == 0 else None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
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
        # Mark a cell as a move that has been made
        self.moves_made.add(cell)

        # Mark a cell as safe
        self.mark_safe(cell)

        # Create new set to store undetermined cells
        undetermined_cells = set()

        # Add a new sentence to the AI's knowledge based on the value of `cell` and `count`
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself and the marked safe cells
                if (i, j) == cell or (i, j) in self.safes:
                    continue

                # Check if cell is mine and update count
                if (i, j) in self.mines:
                    count -= 1
                    continue

                # Update set of undetermined cells
                if 0 <= i < self.height and 0 <= j < self.width:
                    undetermined_cells.add((i, j))

        # Create new knowledge sentence
        new_knowledge_sentence = Sentence(undetermined_cells, count)

        # Add new knowledge sentence to knowledge base
        self.knowledge.append(new_knowledge_sentence)

        # Mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        # Loop through each sentence in knowledge base
        for sentence in self.knowledge:

            # Check if all cells in sentence are known to be safe
            if sentence.known_safes():

                # Loop through all cells in the copy of set then marked it
                for cell in sentence.known_safes().copy():
                    self.mark_safe(cell)

            # Check if all cells in sentence are known to be mines
            if sentence.known_mines():

                # Loop through all cells in the copy of set then marked it
                for cell in sentence.known_mines().copy():
                    self.mark_mine(cell)

        # Add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
        # Loop through each sentence in knowledge base
        for sentence in self.knowledge:

            # Remove if it is an empty sentence
            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)

            # Check if sentences is different
            if new_knowledge_sentence.cells != sentence.cells:

                # Check if new sentence is a subset of existing sentence in knowleage base
                if new_knowledge_sentence.cells.issubset(sentence.cells) and sentence.count > 0 and new_knowledge_sentence.count > 0:

                    # Get the subset cells
                    new_subset_cells = sentence.cells - new_knowledge_sentence.cells

                    # Get the subset count
                    new_subset_count = sentence.count - new_knowledge_sentence.count

                    # Create new sentence of subset for knowledge base
                    new_subset_sentence = Sentence(new_subset_cells, new_subset_count)

                    # Add new subset sentence if it is not in knowledge base
                    if new_subset_sentence not in self.knowledge:
                        self.knowledge.append(new_subset_sentence)

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
        # Create a dictionary to store all possible moves with its probability to be a mine
        possible_moves = {}

        # Calcualte number of mines left on the board
        num_mines_left = 8 - len(self.mines)

        # Calculate number of possible moves left on the board
        num_possible_moves = (self.height * self.width) - (len(self.moves_made) + len(self.mines))

        # Check if there is any possible moves available
        if num_possible_moves == 0:
            return None

        # Calculate the probability of a cell to be a mine without knowledge base
        cells_to_mines_prob = num_mines_left / num_possible_moves

        # Get all possible moves to the dictionary with its probability to be a mine
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    possible_moves[(i, j)] = cells_to_mines_prob

        # Make a move without knowledge base
        if not self.knowledge:
            return random.choice(list(possible_moves))

        # Make better move with knowledge base to decrease the probality to be a mine
        # Loop through each sentence in our knowledge base
        for sentence in self.knowledge:

            # Get number of cells in each sentence
            num_cells = len(sentence.cells)

            # Check if sentence has no cells then remove it
            if num_cells == 0:
                self.knowledge.remove(sentence)
                continue

            # Get number of mines in that sentence
            num_mines = sentence.count

            # Calculate probability of cells in that sentence to be a mine
            cell_to_mine_prob = num_mines / num_cells

            # Loop through each cell in that sentence
            for cell in sentence.cells:

                # Update probability of that cell to the dictionary
                possible_moves[cell] = cell_to_mine_prob

        # Get the lowest probability
        lowest_prob = min(possible_moves.values())

        # Get the list of best possible moves with lowest probability to be mines
        best_possible_moves = [move for move in possible_moves if possible_moves[move] == lowest_prob]

        # Return move with lowest probability to be mines
        return random.choice(best_possible_moves)
