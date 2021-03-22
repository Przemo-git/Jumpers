import pygame
from .constants import BLACK, ROWS, GREEN, SQUARE_SIZE, COLS, WHITE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.green_left = self.white_left = 8
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, GREEN, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)


    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row <= 1:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row >= 6:
                        self.board[row].append(Piece(row, col, GREEN))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    
    def winner(self):
        if self.green_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return GREEN
        
        return None
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left,right))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right,left))
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left,right))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right,left))
        if piece.color:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left,right))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right,left))
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left,right))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right,left))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,right+1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,right-1,skipped=last))
                    moves.update(self._traverse_left(r + step, row, step, color, right - 1,left+1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, right + 1,left-1, skipped=last))
                break

            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right,left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,left+1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,left-1,skipped=last))
                    moves.update(self._traverse_left(r + step, row, step, color, left - 1, right + 1, skipped=last))
                    moves.update(self._traverse_right(r + step, row, step, color, left + 1, right - 1, skipped=last))
                break

            else:
                last = [current]

            right += 1
        
        return moves