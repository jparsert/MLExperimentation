
class FindCheese1DGame:

    def __init__(self, size):
        self.size = size
        self.init_board()
        self.game_score = 0

    def init_board(self):
        self.board = (["="] * self.size)
        self.board[0] = "0"
        self.board[-1] = "C"
        self.board[len(self.board)//2] = "#"

    def get_state(self):
        return self.board

    def get_actions(self):
        return [0,1]

    def apply_action(self, action):


        index = self.board.index("#")
        self.board[index] = "="
        if action == 0:
            self.board[index - 1] = "#"
        elif action == 1:
            self.board[index + 1] = "#"

        if self.board.index("#") == 0:
            self.game_score -= 1
            self.init_board()
        if self.board.index("#") == len(self.board) - 1:
            self.game_score += 1
            self.init_board()

        return self.game_score

    def render(self):
        print("{}\t score: {}".format("".join(self.board), self.game_score))
