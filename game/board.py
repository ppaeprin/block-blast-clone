#? board.py tracks the state of the grid, handles line clears, and validates game over states
import config

class Board:
    def __init__(self):
        self.grid=[[{"tile":False,"color":None} for _ in range(config.GRID_COLS)] for _ in range(config.GRID_ROWS)]

    def can_place(self,piece,x,y): # checks if a piece matrix can fit on the board at the given top-left offset
        p_rows=len(piece)
        p_cols=len(piece[0])

        for r in range(p_rows):
            for c in range(p_cols):
                if piece[r][c]["tile"]:
                    target_x=x+r
                    target_y=y+c

                    if not (0<=target_x<config.GRID_ROWS and 0<=target_y<config.GRID_COLS):
                        return False

                    if self.grid[target_x][target_y]["tile"]:
                        return False
        return True

    def place_piece(self,piece,x,y,color_hex): # commits the piece blocks to the grid state using the provided color string
        p_rows=len(piece)
        p_cols=len(piece[0])

        for r in range(p_rows):
            for c in range(p_cols):
                if piece[r][c]["tile"]:
                    target_x=x+r
                    target_y=y+c
                    self.grid[target_x][target_y]["tile"]=True
                    self.grid[target_x][target_y]["color"]=color_hex

    def check_and_clear_lines(self): # scans rows and columns simultaneously to flag and wipe complete lines, then returns total num cleared
        rows_to_clear=[]
        cols_to_clear=[]

        for row in range(config.GRID_ROWS):
            if all(self.grid[row][col]["tile"] for col in range(config.GRID_COLS)):
                rows_to_clear.append(row)

        for col in range(config.GRID_COLS):
            if all(self.grid[row][col]["tile"] for row in range(config.GRID_ROWS)):
                cols_to_clear.append(col)

        for row in rows_to_clear:
            for col in range(config.GRID_COLS):
                self.grid[row][col]={"tile":False,"color":None}
        for col in cols_to_clear:
            for row in range(config.GRID_ROWS):
                self.grid[row][col]={"tile":False,"color":None}

        return len(rows_to_clear)+len(cols_to_clear)

    def is_completely_clear(self): # checks if the entire board is empty
        for r in range(config.GRID_ROWS):
            for c in range(config.GRID_COLS):
                if self.grid[r][c]["tile"]:
                    return False
        return True

    def can_any_piece_fit(self,active_buffer): # returns false if no available pieces in the buffer can fit anywhere on the current board grid
        for piece in active_buffer:
            if piece is None:
                continue
            for r in range(config.GRID_ROWS):
                for c in range(config.GRID_COLS):
                    if self.can_place(piece,r,c):
                        return True
        return False

    def print_board(self): # quick terminal debug helper to view the current engine status
        for r in range(config.GRID_ROWS):
            row_str=""
            for c in range(config.GRID_COLS):
                if self.grid[r][c]["tile"]:
                    row_str+="# "
                else:
                    row_str+=". "
            print(row_str)
        print()