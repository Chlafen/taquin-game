from tkinter import *
from PIL import Image, ImageTk

# a function that gets a board_size and board_state 
# and the parent window, then generates the board 
# and makes it visible within the parent window
def generate_board(board_state, parent, images, tile_size=100, show_blank=True):
    board = Frame(parent, bg="#e1c2ff")
    board_size = len(board_state)
    for i in range(board_size):
        for j in range(board_size):
            tile = board_state[i][j]
            if tile == 0 and show_blank :
                tile = -1 
            label = Label(board, image=images[tile], borderwidth=1, relief="solid")
            label.image = images[tile]
            label.grid(row=i, column=j, padx=2, pady=2)


    board.pack(side=TOP, pady=20, padx=20)

    return board        
    


def loag_image_and_segment(tile_size, board_size):
    board = Image.open('assets/board.png').convert('RGBA')
    board = board.resize((tile_size * board_size, tile_size * board_size))
    images = []
    for i in range(board_size):
        for j in range(board_size):
            imgij = board.crop(
                [
                    tile_size * j,
                    tile_size * i,
                    tile_size * (j+1),
                    tile_size * (i+1)
                ])
            images.append(ImageTk.PhotoImage(imgij))
    
    blank = Image.open('assets/blank.png').convert('RGBA')
    blank = blank.resize((tile_size, tile_size))
    images.append(ImageTk.PhotoImage(blank))
    return images

