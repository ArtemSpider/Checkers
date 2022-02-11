from Board import *
from Graphics import *

class Game(object):
    def _set_selected(self, selected : Position):
        self.selected = selected
        self.graphics.selected = selected
        self.graphics.redraw = True
    def _reset_selected(self):
        self.selected = None
        self.graphics.selected = None
        self.graphics.redraw = True

    def _set_result_text(self, text: str):
        self.game_ended = True
        self.graphics.result_str = text
    def _reset_result_text(self):
        self.game_ended = False
        self.graphics.result_str = None
        
    def _set_new_board(self):
        self.graphics.board = self.board
        self._reset_selected()

    def _restart(self):
        self.selected = None
        self.game_ended = False
        self._reset_result_text()
        self.board = Board()
        self._set_new_board()
        self.__all_moves = self.board.get_all_moves()

    def _move(self, pos1 : Position, pos2 : Position):
        self.board.move(pos1, pos2)
        
        di = (pos2[0] - pos1[0], pos2[1] - pos1[1])
        di = (di[0] // abs(di[0]), di[1] // abs(di[1]))
        pp = (pos2[0] - di[0], pos2[1] - di[1])

        if abs(pos1[0] - pos2[0]) > 1 and self.board.grid[pp[1]][pp[0]] == 3 - self.board.grid[pos2[1]][pos2[0]]:
            self.board.remove(pp)
            self._set_selected(pos2)

            if not self.board.can_take(pos2):
                self._reset_selected()
                self.board.turn = 3 - self.board.turn
        else:
            self._reset_selected()
            self.board.turn = 3 - self.board.turn

        self.__all_moves = self.board.get_all_moves()

        if len(self.__all_moves) == 0:
            self._set_result_text("Black won" if self.board.turn == 1 else "White won")

        self.graphics.redraw = True

    def __click_handler(self, event):
        pos = (event.x // 64, 9 - event.y // 64)

        if Board.in_bounds(pos):
            if self.board.grid[pos[1]][pos[0]] == self.board.turn:
                self._set_selected(pos)
            elif self.selected != None:
                if pos in self.__all_moves[self.selected]:
                    self._move(self.selected, pos)
    def __key_press_handler(self, event):
        if event.keysym == "space" and self.game_ended:
            self._restart()

    def __init__(self):
        self.selected = None
        self.game_ended = False

        self.board = Board()
        self.graphics = Graphics(self.board)
        
        self.graphics.win.bind_all('<Button-1>', self.__click_handler)
        self.graphics.win.bind_all('<KeyPress>', self.__key_press_handler)

        self.__all_moves = self.board.get_all_moves()

    def step(self) -> bool:
        self.graphics.draw()
        return True

    def run(self):
        while self.step(): pass