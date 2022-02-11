from graphics import *

from Board import *

class Graphics(object):
    def __init__(self, board: Board):
        self.redraw = True
        self.board = board
        self.win = GraphWin("Checkers", 640, 640, autoflush = False)

        self.selected = None

        self.__squares = [[None for j in range(10)] for i in range(10)]
        for i in range(10):
            for j in range(10):
                self.__squares[i][j] = Rectangle(Point(j * 64, i * 64), Point(j * 64 + 64, i * 64 + 64))
                self.__squares[i][j].setFill("saddle brown" if (i + j) % 2 else "burlywood")
                self.__squares[i][j].setWidth(0)

        self.__pieces = [[None for j in range(10)] for i in range(10)]
        for i in range(10):
            for j in range(10):
                self.__pieces[i][j] = Circle(Point(j * 64 + 32, (9 - i) * 64 + 32), 30)
                self.__pieces[i][j].setWidth(0)

        self.__upg_circles = [[None for j in range(10)] for i in range(10)]
        for i in range(10):
            for j in range(10):
                self.__upg_circles[i][j] = Circle(Point(j * 64 + 32, (9 - i) * 64 + 32), 12)
                self.__upg_circles[i][j].setFill("red")
                self.__upg_circles[i][j].setWidth(0)

        self.__sel_circles = [[None for j in range(10)] for i in range(10)]
        for i in range(10):
            for j in range(10):
                self.__sel_circles[i][j] = Circle(Point(j * 64 + 32, (9 - i) * 64 + 32), 8)
                self.__sel_circles[i][j].setFill("yellow")
                self.__sel_circles[i][j].setWidth(0)
                
        self.result_str = None

        self.__result_window = Rectangle(Point(3 * 64 - 48, 4 * 64), Point(7 * 64 + 48, 6 * 64))
        self.__result_window.setFill("white")
        self.__result_window.setWidth(0)

        self.__result_text = Text(Point(5 * 64, 5 * 64 - 24), "")
        self.__result_text.setSize(28)

        self.__restart_text = Text(Point(5 * 64, 5 * 64 + 30), "Press Space to restart")
        self.__restart_text.setSize(16)

    def draw(self):
        if self.redraw:
            grid = self.board.grid

            for i in range(10):
                for j in range(10):
                    self.__squares[i][j].undraw()
                    
            for i in range(10):
                for j in range(10):
                    self.__squares[i][j].draw(self.win)
        
            for i in range(10):
                for j in range(10):
                    self.__pieces[i][j].undraw()
                    self.__upg_circles[i][j].undraw()
                    self.__sel_circles[i][j].undraw()

                    if grid[i][j] == 0:
                        continue

                    if grid[i][j] == 1:
                        self.__pieces[i][j].setFill("grey95")
                    else:
                        self.__pieces[i][j].setFill("grey5")
                    self.__pieces[i][j].draw(self.win)

                    if self.board.upgraded[i][j]:
                        self.__upg_circles[i][j].draw(self.win)

            if self.selected != None:
                sel = self.board.get_all_moves()[self.selected]

                for p in sel:
                    self.__sel_circles[p[1]][p[0]].draw(self.win)
                    
            self.__result_window.undraw()
            self.__result_text.undraw()
            self.__restart_text.undraw()
            if self.result_str != None:
                self.__result_text.setText(self.result_str)
                self.__result_window.draw(self.win)
                self.__result_text.draw(self.win)
                self.__restart_text.draw(self.win)

            self.redraw = False

        self.win.update()