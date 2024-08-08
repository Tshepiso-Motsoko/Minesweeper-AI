import random

class Sentence:
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
        if self.count == len(self.cells):
            return set(self.cells)
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return set(self.cells)
        else:
            return set()

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

class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []

    def mark_mine(self, cell):
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        self.moves_made.add(cell)
        self.mark_safe(cell)
        neighbors = self.get_neighbors(cell)
        unknown_neighbors = set()
        for neighbor in neighbors:
            if neighbor in self.safes:
                continue
            if neighbor in self.mines:
                count -= 1
                continue
            unknown_neighbors.add(neighbor)
        new_sentence = Sentence(unknown_neighbors, count)
        if new_sentence.cells:
            self.knowledge.append(new_sentence)
        self.update_knowledge()

    def make_safe_move(self):
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        while True:
            i = random.randint(0, self.height - 1)
            j = random.randint(0, self.width - 1)
            move = (i, j)
            if move not in self.moves_made and move not in self.mines:
                return move
            if len(self.moves_made) + len(self.mines) == self.height * self.width:
                return None

    def get_neighbors(self, cell):
        i, j = cell
        neighbors = [(x, y) for x in range(i - 1, i + 2) for y in range(j - 1, j + 2)
                     if 0 <= x < self.height and 0 <= y < self.width and (x, y) != (i, j)]
        return neighbors

    def update_knowledge(self):
        changed = True
        while changed:
            changed = False
            for sentence in self.knowledge:
                safes = sentence.known_safes()
                mines = sentence.known_mines()
                if safes:
                    changed = True
                    self.safes.update(safes)
                    for safe in safes:
                        self.mark_safe(safe)
                if mines:
                    changed = True
                    self.mines.update(mines)
                    for mine in mines:
                        self.mark_mine(mine)
            self.knowledge = [s for s in self.knowledge if s.cells]
            for sentence1 in self.knowledge:
                for sentence2 in self.knowledge:
                    if sentence1 != sentence2 and sentence1.cells.issubset(sentence2.cells):
                        diff_cells = sentence2.cells - sentence1.cells
                        diff_count = sentence2.count - sentence1.count
                        new_sentence = Sentence(diff_cells, diff_count)
                        if new_sentence not in self.knowledge and new_sentence.cells:
                            self.knowledge.append(new_sentence)
                            changed = True
