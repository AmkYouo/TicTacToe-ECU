#Yousef Mahmoud Anis 192100029
#Yousef Gabr 192100069 

import matplotlib.pyplot as plt
import numpy as np
from queue import Queue, PriorityQueue
import random

class TicTacToe:
    def __init__(self):
        self.board = np.full((3, 3), ' ')
        self.current_player = 'X'

    #check for winner
    def is_winner(self, player):
        for i in range(3):
            if all(self.board[i, j] == player for j in range(3)):
                return True
            if all(self.board[j, i] == player for j in range(3)):
                return True
        if all(self.board[i, i] == player for i in range(3)) or all(self.board[i, 2 - i] == player for i in range(3)):
            return True
        return False
    #to draw empty spaces on board
    def is_draw(self):
        return np.all(self.board != ' ')

    #to check if there is any available moves
    def get_available_moves(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == ' ']

    #makes the move
    def make_move(self, row, col, player):
        if self.board[row, col] == ' ':
            self.board[row, col] = player
            return True
        return False

    #uses to create a new game
    def clone(self):
        new_game = TicTacToe()
        new_game.board = self.board.copy()
        return new_game

    # No random cost generation, all moves have a constant cost of 1
    def get_move_costs(self):
        return {move: 1 for move in self.get_available_moves()}

    #Lower than Function used in UCS  
    def __lt__(self, other):
        for i in range(3):
            for j in range(3):
                if self.board[i, j] != other.board[i, j]:
                    return self.board[i, j] < other.board[i, j]
        return False


class TicTacToeGame:
    def __init__(self):
        self.game = TicTacToe()
        self.search_agent = TicTacToeSearchAgent(self.game)
        self.fig, self.ax = plt.subplots()
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.update_board()
        self.strategy = self.choose_strategy()  # Select strategy for computer
        plt.show()

    def choose_strategy(self):
        # Strategy selection
        print("Select the computer's strategy:")
        print("1: BFS")
        print("2: DFS")
        print("3: UCS")
        choice = input("Enter your choice (1/2/3): ")
        if choice == '1':
            return 'bfs'
        elif choice == '2':
            return 'dfs'
        elif choice == '3':
            return 'ucs'
        else:
            print("Invalid choice, defaulting to BFS.")
            return 'bfs'

    def update_board(self):
        self.ax.clear()
        for i in range(1, 3):
            self.ax.plot([i, i], [0, 3], color="black", lw=2)
            self.ax.plot([0, 3], [i, i], color="black", lw=2)
            
        # Get the costs for available moves
        move_costs = self.game.get_move_costs()

        for i in range(3):
            for j in range(3):
                if self.game.board[i, j] == 'X':
                    self.ax.text(j + 0.5, 2.5 - i, 'X', ha='center', va='center', fontsize=40, color="blue")
                elif self.game.board[i, j] == 'O':
                    self.ax.text(j + 0.5, 2.5 - i, 'O', ha='center', va='center', fontsize=40, color="red")

                # Display the cost if the move is available
                if (i, j) in move_costs:
                    cost_text = str(move_costs[(i, j)])  # Get the cost for the move
                    self.ax.text(j + 0.5, 2.5 - i, cost_text, ha='center', va='center', fontsize=20, color="black")

        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xlim(0, 3)
        self.ax.set_ylim(0, 3)
        plt.draw()

        
    def on_click(self, event):
        if event.xdata is None or event.ydata is None:
            return

        col = int(event.xdata)
        row = 2 - int(event.ydata)

        if self.game.make_move(row, col, 'X'):
            if self.game.is_winner('X'):
                self.update_board()
                plt.title("Player X wins!")
                plt.show()
                return
            elif self.game.is_draw():
                self.update_board()
                plt.title("It's a draw!")
                plt.show()
                return

            self.update_board()
            self.computer_move(strategy=self.strategy)  # Use the selected strategy

    def computer_move(self, strategy):
        move = None
        if strategy == 'bfs':
            move = self.search_agent.bfs()
        elif strategy == 'dfs':
            move = self.search_agent.dfs()
        elif strategy == 'ucs':
            move = self.search_agent.ucs()

        if move:
            row, col = move
            self.game.make_move(row, col, 'O')
            if self.game.is_winner('O'):
                self.update_board()
                plt.title("Computer O wins!")
                plt.show()
                return
            elif self.game.is_draw():
                self.update_board()
                plt.title("It's a draw!")
                plt.show()
                return

            self.update_board()

#Search Agent Functions
class TicTacToeSearchAgent:
    def __init__(self, game):
        self.game = game

    def bfs(self):
        queue = Queue()
        queue.put((self.game.clone(), None))
        while not queue.empty():
            current_game, initial_move = queue.get()
            if current_game.is_winner('O'):
                return initial_move
            for move in current_game.get_available_moves():
                new_game = current_game.clone()
                new_game.make_move(move[0], move[1], 'O')
                queue.put((new_game, move if initial_move is None else initial_move))
        return random.choice(self.game.get_available_moves())

    def dfs(self):
        stack = [(self.game.clone(), None)]
        while stack:
            current_game, initial_move = stack.pop()
            if current_game.is_winner('O'):
                return initial_move
            for move in current_game.get_available_moves():
                new_game = current_game.clone()
                new_game.make_move(move[0], move[1], 'O')
                stack.append((new_game, move if initial_move is None else initial_move))
        return random.choice(self.game.get_available_moves())

    def ucs(self):
        pq = PriorityQueue()
        pq.put((0, self.game.clone(), None))  # Initial state with cost 0
        while not pq.empty():
          cost, current_game, initial_move = pq.get()
          if current_game.is_winner('O'):
            return initial_move
          for move in current_game.get_available_moves():
            new_game = current_game.clone()
            new_game.make_move(move[0], move[1], 'O')
        # Use a constant cost (e.g., 1) for new moves
            new_cost = cost + 1
            pq.put((new_cost, new_game, move if initial_move is None else initial_move))
        return random.choice(self.game.get_available_moves())

TicTacToeGame()
