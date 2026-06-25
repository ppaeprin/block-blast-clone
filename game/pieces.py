#? pieces.py contains all pieces, can generate a random trio for the buffer (right under the board), and can simulate a cloned instance to check for every combination possible till it finds a playable combination
import config
import random    # for generating random trios for the buffer
import copy      # for cloning the board class obj (which is Board())
import itertools # for iterating through all the orders of the trio

PIECES=[
    [
        [1]
    ],
    [
        [1,1],
        [1,1],
    ],
    [
        [1,1,1],
        [1,1,1],
        [1,1,1],
    ],
    [
        [1,1],
    ],
    [
        [1,1,1]
    ],
    [
        [1,1,1,1],
    ],
    [
        [1,1,1,1,1],
    ],
    [
        [1,1,1],
        [1,1,1],
    ],
    [
        [1,1],
        [1,0],
        [1,0],
    ],
    [
        [1,1],
        [1,0],
    ],
    [
        [1,1,1],
        [1,0,0],
        [1,0,0],
    ],
    [
        [0,1,0],
        [1,1,1],
    ],
    [
        [1,1,0],
        [0,1,1],
    ]
]

def rot(piece,n): # rotates the matrix of tiles of the piece n times 90deg clockwise
    for _ in range(n):
        piece=[list(row) for row in zip(*piece[::-1])]
    return piece

def mirror(piece,axis): # mirrors piece horizontally (axis=1) or vertically (axis=2), or just doesnt mirror it in any way (axis=anything but 1 or 2)
    if axis==1:
        return [row[::-1] for row in piece] # horizontal axis rotation
    elif axis==2:
        return piece[::-1] # vertical axis rotation
    return piece # no mirror

def randrot(piece): # generates a random rotation of the piece
    return mirror(rot(piece,random.randint(0,3)),random.randint(0,2))

def randbuffer(): # generates 3 random pieces for the buffer with dict structures
    buffer=[]
    for _ in range(3):
        raw_piece=  randrot      (random.choice(PIECES)) # get a completely random piece (randomized raw matrix of 1s and 0s)
        piece_color=random.choice(config.TILES_CLRS    ) # pick a random color for this specific piece
        colored_piece=[ # convert the 1s and 0s into your target dictionary structure
            [
                {"tile":True,"color":piece_color} if cell==1 else {"tile":False,"color":None} for cell in row
            ]
            for row in raw_piece
        ]
        buffer.append(colored_piece)
    return buffer

def print_buffer(active_buffer): # pass the actual game state buffer here
    for idx,piece in enumerate(active_buffer):
        print(f"piece {idx+1}:")
        for row in piece:
            # check the dictionary "tile" key instead of the raw integer 1
            row_str=" ".join("#" if cell["tile"] else "." for cell in row)
            print(row_str)
        print()
    print()

# debugging randomizer and print_buffer
#buffer=randbuffer()
#print_buffer(buffer)

def clone_board(board_grid): # builds a brand new nested structure, copying the vals directly
    return [
        [
            {"tile":cell["tile"],"color":cell["color"]} # copies vals from board_grid to the instance
            for cell in row
        ]
        for row in board_grid
    ]

def simulate_clear(ghost_grid): # checks for full rows and cols, then clears them out
    # a row/col is full if every cell of that line has "tile":True
    full_rows=[row for row in range(8) if all(ghost_grid[row][col]["tile"] for col in range(8))]
    full_cols=[col for col in range(8) if all(ghost_grid[row][col]["tile"] for row in range(8))]

    # clear them out (turn them back to empty cells)
    for row in full_rows:
        for col in range(8):
            ghost_grid[row][col]={"tile":False,"color":None}

    for col in full_cols:
        for row in range(8):
            ghost_grid[row][col]={"tile":False,"color":None}

def is_trio_playable(board_obj, buffer_trio): # tests if the 3 pieces can fit in any order
    # try every possible sequence of the 3 pieces (6 combinations total because 3!=6)
    for order in itertools.permutations(buffer_trio):
        p1,p2,p3=order # unpacks the tuple order to p1 p2 and p3

        for row_p1 in range(8): # try to find a spot for p1 in grid1
            for col_p1 in range(8):
                if board_obj.can_place(p1,row_p1,col_p1):
                    grid1=copy.deepcopy(board_obj) # clone the entire board class instance safely
                    p1_clr=[cell["color"] for row in p1 for cell in row if cell["tile"]][0]
                    grid1.place_piece(p1,row_p1,col_p1,p1_clr) # places and triggers line clears auto

                    for row_p2 in range(8): # try to find a spot for p2 on the updated ghost board grid2
                        for col_p2 in range(8):
                            if grid1.can_place(p2,row_p2,col_p2):
                                grid2=copy.deepcopy(grid1) # clone the updated grid1 obj safely
                                p2_clr=[cell["color"] for row in p2 for cell in row if cell["tile"]][0]
                                grid2.place_piece(p2,row_p2,col_p2,p2_clr) # places and triggers line clears auto

                                for row_p3 in range(8): # try to find a spot for p3
                                    for col_p3 in range(8):
                                        if grid2.can_place(p3, row_p3, col_p3):
                                            return True # if it loops thru everything and all conditions work, this trio is valid
    return False # if it loops thru everything and nothing works, this trio is a dead end

def gen_valid_buffer(board_obj): # master loop that guarantees a playable trio
    while True:
        test_buffer=randbuffer()
        if is_trio_playable(board_obj,test_buffer):
            return test_buffer

# debugging how it checks for valid trios (credits to gemini)
#if __name__ == "__main__":
#    # 1. import your board class from board.py
#    from board import Board
#    
#    print("initializing a test board...")
#    test_board = Board()
#    
#    # 2. let's artificially jam the board grid to make it hard to place things
#    # we leave only a tiny 2x2 hole open in the top left corner (rows 0-1, cols 0-1)
#    # everything else gets filled up completely
#    for r in range(8):
#        for c in range(8):
#            if r > 1 or c > 1:
#                test_board.grid[r][c] = {"tile": True, "color": "#FFFFFF"}
#    
#    test_board.print_board()
#    
#    print("test board setup complete! (almost entirely full except for a 2x2 gap)")
#    print("running look-ahead generator...")
#    
#    # 3. trigger your loop. it should reject any combos that don't fit in that 2x2 space
#    valid_trio = gen_valid_buffer(test_board)
#    
#    print("\nSUCCESS! found a valid combination that doesn't trigger a game over:")
#    print_buffer(valid_trio)