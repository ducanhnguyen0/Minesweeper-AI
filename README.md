# Minesweeper: A Minesweeper knowledge-based AI agent

Harvard CS50AI Project

## Description:

An AI program to play classic Windows "Minesweeper" game using Propositional Logic represents AI knowledge to help AI make decisions by considering their knowledge base, and making inferences based on that knowledge to generate new knowledge about the game state.

## Tech Stack:

* Python

## Background:
Minesweeper is a puzzle game that consists of a grid of cells, where some of the cells contain hidden “mines.” Clicking on a cell that contains a mine detonates the mine, and causes the user to lose the game. Clicking on a “safe” cell (i.e., a cell that does not contain a mine) reveals a number that indicates how many neighboring cells – where a neighbor is a cell that is one square to the left, right, up, down, or diagonal from the given cell – contain a mine.

In this 3x3 Minesweeper game, for example, the three 1 values indicate that each of those cells has one neighboring cell that is a mine. The four 0 values indicate that each of those cells has no neighboring mine.

Given this information, a logical player could conclude that there must be a mine in the lower-right cell and that there is no mine in the upper-left cell, for only in that case would the numerical labels on each of the other cells be accurate.

The goal of the game is to flag (i.e., identify) each of the mines. In many implementations of the game, including the one in this project, the player can flag a mine by right-clicking on a cell (or two-finger clicking, depending on the computer).

## Project Specification:

### Sentence class.
* The known_mines function should return a set of all of the cells in self.cells that are known to be mines.
* The known_safes function should return a set of all the cells in self.cells that are known to be safe.
* The mark_mine function should first check to see if cell is one of the cells included in the sentence.
* The mark_safe function should first check to see if cell is one of the cells included in the sentence.
  
### MinesweeperAI class.
* add_knowledge should accept a cell (represented as a tuple (i, j)) and its corresponding count, and update self.mines, self.safes, self.moves_made, and self.knowledge with any new information that the AI can infer, given that cell is known to be a safe cell with count mines neighboring it.
* make_safe_move should return a move (i, j) that is known to be safe.
* make_random_move should return a random move (i, j) if a safe move is not possible: if the AI doesn’t know where to move, it will choose to move randomly instead.


## How to run

1. Clone this project
2. Install requirements package:
   ```
   pip install -r requirements.txt
   ```
3. Run the Minesweeper game:
   ```
   python runner.py
   ```
   (You can play by yourself or let AI play for you by clicking `AI Move`)
