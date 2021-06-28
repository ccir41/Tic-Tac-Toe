import sys

class TicTacToe:
    def __init__(self):
        self.__game_board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.__step = 0 # for tracking moves
        self.__turn = 0 # if 0 -> player first and if 1 -> cpu first
        self.__EMPTY_MARK = 0
        self.__PLAYER_MARK = 1
        self.__CPU_MARK = 2

    def __show_game_board(self):
        print("\n\t\t+-----------+")
        for i in range(3):
            row_print = '\t\t|'
            for j in range(3):
                if self.__game_board[i][j] == self.__EMPTY_MARK:
                    row_print += '   |'
                elif self.__game_board[i][j] == self.__PLAYER_MARK:
                    row_print += ' X |'
                elif self.__game_board[i][j] == self.__CPU_MARK:
                    row_print += ' O |'
                else:
                    print("something went wrong")
            print(row_print)
            print("\t\t+-----------+")
    
    def __validate_coordinate(self, coordinate):
        return (
            coordinate[0] > 0 and
            coordinate[1] > 0 and
            coordinate[0] <= 3 and
            coordinate[0] <= 3 and
            self.__game_board[coordinate[0]-1][coordinate[1]-1] == self.__EMPTY_MARK # check if place is empty represented by 0
        )
    
    def __read_coordinate(self):
        print("\n")
        inp = input("Provide a valid and empty position to place your mark: ")
        try:
            inp_split = inp.split(',')
            a = int(inp_split[0][1])
            b = int(inp_split[1][0])
            return [a, b]
        except:
            print("Invalid position!, Please enter a valid and empty position!")
            self.__read_coordinate()
        return None
    
    def __place_mark(self, mark, coordinate=None):
        if mark == self.__PLAYER_MARK:
            self.__user_move(coordinate)
        else:
            self.__program_move()
        
        self.__step += 1 # increment step
        self.__turn = 1 if self.__turn == 0 else 0 # toggle turn
        return self.__check_win(mark)

    def __user_move(self, coordinate):
        self.__game_board[coordinate[0]-1][coordinate[1]-1] = 1

    def __program_move(self):
        # place mark at center position if empty
        if self.__game_board[1][1] == self.__EMPTY_MARK:
            self.__game_board[1][1] = self.__CPU_MARK
            return
        
        # check if it can win in next move
        winning_coordinate = self.__next_winning_move(self.__CPU_MARK)
        if winning_coordinate:
            self.__game_board[winning_coordinate[0]][winning_coordinate[1]] = self.__CPU_MARK
            return
        
        # choose move that prevent oponent from winning
        for i in range(3):
            for j in range(3):
                if(self.__game_board[i][j] == self.__EMPTY_MARK):
                    self.__game_board[i][j] = self.__CPU_MARK
                    # check if opponent win at this position
                    opp_winning_coordinate = self.__next_winning_move(self.__PLAYER_MARK)
                    self.__game_board[i][j] = self.__EMPTY_MARK
                    if opp_winning_coordinate:
                        self.__game_board[opp_winning_coordinate[0]][opp_winning_coordinate[1]] = self.__CPU_MARK
                        return
        
        # choose available move
        for i in range(3):
            for j in range(3):
                if(self.__game_board[i][j] == self.__EMPTY_MARK):
                    self.__game_board[i][j] = self.__CPU_MARK
                    return

    def __next_winning_move(self, mark):
        for i in range(3):
            for j in range(3):
                if(self.__game_board[i][j] == self.__EMPTY_MARK):
                    self.__game_board[i][j] = mark
                    can_win = self.__check_win(mark)
                    self.__game_board[i][j] = self.__EMPTY_MARK
                    if can_win:
                        return [i, j]
        return None

    def __check_win(self, mark):
        reverse_game_board = list([row for row in reversed(self.__game_board)])
        if(
            self.__check_row_column(mark, row=True) or
            self.__check_row_column(mark) or
            self.__check_diagonal_win(mark) or
            self.__check_diagonal_win(mark, reverse_game_board)
        ):
            return mark
        return False
    
    def __check_row_column(self, mark, row=False):
        win_row_column = [0,0,0]
        for i in range(3):
            for j in range(3):
                if(self.__game_board[i][j] == mark):
                    if row:
                        win_row_column[i] += 1
                    else:
                        win_row_column[j] += 1
        
        for i in range(3):
            if win_row_column[i] == 3:
                return mark
        return False
    
    def __check_diagonal_win(self, mark, board=None):
        diag = 0
        if not board:
            board = self.__game_board
        for i in range(3):
            for j in range(3):
                if (i != j):
                    continue
                if(board[i][j] == mark):
                    diag += 1
        if diag == 3:
            return True
        return False

    def start_game(self):
        player_win = None
        cpu_win = None

        print("\n+-----------------------------------------------+")
        print("\t\tTic Tac Toe")
        print("\t+---------------------------+")
        print("\n    Valid empty position should be provided. ")
        print("    Position should be in form of [num,num] ")
        print("    and should be in the range of [1,3]. \n")
        print("    Any other invalid input other than the ")
        print("    provided range will again be prompted for ")
        print("    input.")
        print("\n+-----------------------------------------------+\n")
        
        while(self.__step < 9):
            self.__show_game_board()
            coordinate = self.__read_coordinate()
            try:
                valid = self.__validate_coordinate(coordinate)
                if not valid:
                    print("Invalid position!, Please enter a valid and empty position!")
                    coordinate = self.__read_coordinate()
            except:
                print("Invalid position!, Please enter a valid and empty position!")
                coordinate = self.__read_coordinate()
            
            player_win = self.__place_mark(self.__PLAYER_MARK, coordinate)
            cpu_win = self.__place_mark(self.__CPU_MARK)
            if player_win or cpu_win:
                break
        
        print("\n")
        print("\t+---------------------------+")
        print("\t\t  Final Board!")
        print("\t+---------------------------+")
        self.__show_game_board()
        if player_win == self.__PLAYER_MARK:
            print("\t+---------------------------+")
            print("\t\t  Player Wins!")
            print("\t+---------------------------+")
        elif cpu_win == self.__CPU_MARK:
            print("\t+---------------------------+")
            print("\t\t  CPU Wins!")
            print("\t+---------------------------+")
        else:
            print("\t+---------------------------+")
            print("\t\t  Its a Tie!")
            print("\t+---------------------------+")
        
        sys.exit()


if __name__ == '__main__':
    ttt = TicTacToe()
    ttt.start_game()
