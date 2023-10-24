import time
import tkinter as tk
from algorithms import AStar, Dfs, Bfs, IDAStar
from taquin import Taquin, board_solution
from board import generate_board, loag_image_and_segment
from matplotlib import pyplot as plt

algorithmMap = {
    1: (AStar, 'A* Search'),
    2: (Dfs, 'Depth First Search'),
    3: (IDAStar, 'IDA* Search'),
    # 4: (Bfs, 'Breadth First Search'),
}

class MenuGUI:

    algorithm_radio = {
        "A*" :  1,
        "DFS" : 2,
        "IDA*" : 3,
        # "BFS" : 4
    } 

    def __init__(self):
        self.size=3
        self.shuffleCount = 20
        self.algorithm = algorithmMap[1]
        self.taquin = None
        self._root = tk.Tk()
        self.board = None
        self.result_group = None
        self._root.title("Taquin Solver")

    def show_form(self):
        form_container = tk.Frame(master=self._root, padx=20, pady=20)
        radioGroup = tk.Frame(master=form_container)
        radioLabel = tk.Label(master=radioGroup, text= "Select a search Algorithm")
        selectedAlgo = tk.IntVar(radioGroup, 1) 
        
        algorithm_radio = self.algorithm_radio
        algoRadios = []
        for (algo, value) in algorithm_radio.items(): 
            algoRadios.append(tk.Radiobutton(radioGroup, text = algo, variable = selectedAlgo, value = value))

        sizeGroup = tk.Frame(master= form_container)
        sizeLabel = tk.Label(master=sizeGroup, text= "Select a board size")
        selectedSize = tk.IntVar(sizeGroup, 3)
        sizeValues = {
            "3x3" : 3, 
            "4x4" : 4, 
            "5x5" : 5, 
            "6x6" : 6,
            "7x7" : 7,
        }
        sizeRadios = []
        for (size, value) in sizeValues.items(): 
            sizeRadios.append(tk.Radiobutton(sizeGroup, text = size, variable = selectedSize, value = value))

        shuffleGroup = tk.Frame(master=form_container)
        shuffleLabel = tk.Label(master=shuffleGroup, text= "Select a shuffle count")
        # slider for shuffle count
        shuffleInput = tk.Scale(shuffleGroup, from_=0, to=100, orient=tk.HORIZONTAL)


        buttonGroup = tk.Frame(master=form_container)

        shuffleButton = tk.Button(
            master=buttonGroup, 
            text="Shuffle", 
            command=lambda: self.shuffle(selectedAlgo.get(), selectedSize.get(), shuffleInput.get()))
      
        startButton = tk.Button( 
            master=buttonGroup, 
            text="Start", 
            command=lambda: self.start())
        

        radioLabel.pack(side=tk.LEFT, pady=20)
        for button in algoRadios: 
           button.pack(side = tk.LEFT, ipady = 2)

        sizeLabel.pack(side=tk.LEFT, pady=20)
        for button in sizeRadios: 
           button.pack(side = tk.LEFT, ipady = 5) 

        shuffleLabel.pack(side=tk.TOP, pady=20)
        shuffleInput.pack(side=tk.TOP, pady=10)

        radioGroup.pack(side=tk.TOP, padx=20)
        sizeGroup.pack(side=tk.TOP, padx=20)
        shuffleGroup.pack( side=tk.TOP, padx=20)

        form_container.pack()
        buttonGroup.pack(side=tk.BOTTOM, pady=20)
        shuffleButton.pack(side=tk.LEFT, padx=20)
        startButton.pack(side=tk.RIGHT, padx=20)

    def show_board(self, tile_size=100, show_blank=True):
        if self.taquin is None:
            return
        board_width = 350
        board_size = self.size 
        board_state = self.taquin.get_state()
        images = loag_image_and_segment(board_width//board_size, board_size)
        gen_board = generate_board(board_state, self._root, images, tile_size, show_blank=show_blank)
        if self.board is not None: 
            self.board.destroy()
        self.board = gen_board

    def shuffle(self, algo, size, shuffle):
        self.size = size
        self.shuffleCount = shuffle
        self.algorithm = algorithmMap[algo]
        if self.taquin.size != size: 
            self.taquin = Taquin(size)
        shufflePath = self.taquin.shuffle_board(shuffle)
        self.show_path(shufflePath, 0.01)

    def show_path(self, path, sleepTime=0.01):
        for state, i in zip(path, range(len(path))): 
            self.taquin.set_state(state)
            self.show_board(show_blank=(state!=board_solution(self.size)))
            self._root.update()
            time.sleep(sleepTime)

    def show_footer_text(self, *args):
        if self.result_group is not None:  
            self.result_group.destroy()
        self.result_group = tk.Frame(master=self._root)
        self.result_group.pack(side=tk.BOTTOM, pady=20)
        for text in args: 
            result_label = tk.Label(master=self.result_group, text=text)
            result_label.pack() 
        
    def start(self):
        if self.taquin is None: 
            return
    
        self.show_footer_text("Solving with " + self.algorithm[1] + "...")
        
        solver = self.algorithm[0](self.taquin)
        taquin_list_path = solver.get_path()
        if taquin_list_path is None:
            self.show_footer_text("No solution found")
            return
            
        path = [ t.get_state() for t in taquin_list_path ]

        stats = solver.get_stats()

        if len(path) == 0: 
            self.show_footer_text("No solution found")
        else:      
            self.show_footer_text(
                "Solved in " + str(len(path)) + " steps", 
                "Explored: " + str(stats["closed_count"]) + " states",
                "Max open count: " + str(stats["max_open_count"]),
            )
        self.show_path(path, 0.01)

    def display(self):
        self.show_form()
        self.taquin = Taquin(3)
        self.show_board(show_blank=False)
        self._root.mainloop()

def main():
    menu = MenuGUI()
    menu.display()
if __name__ == "__main__":
    main()