import copy
import sys

board_value = []
init_board = []
sym_choice = ''
opp_choice = ''
alg_choice = ''
cut_off_p1 = 0
cut_off_p2 = 0


class Board:
    def __init__(self, curr_state, player, opponent):
        self.brd_state = copy.deepcopy(curr_state)
        self.brd_p1 = player
        self.brd_p2 = opponent
        self.brd_curr_p1_eval, self.brd_curr_p2_eval = self.brd_eval_function()
        self.brd_raid_flag = False
        # self.cut_off = cut_off

    def brd_eval_function(self):
        init_p1_eval = 0
        init_p2_eval = 0
        init_b_eval = 0

        for i in range(5):
            # print key
            for j in range(5):
                init_b_eval += board_value[i][j]
                if self.brd_state[i][j] == self.brd_p1:
                    init_p1_eval += board_value[i][j]
                elif self.brd_state[i][j] == self.brd_p2:
                    init_p2_eval += board_value[i][j]

        curr_p1_eval = init_p1_eval - init_p2_eval
        curr_p2_eval = init_p2_eval - init_p1_eval
        evaluated = [curr_p1_eval, curr_p2_eval]

        return evaluated

    def end_game(self):
        for i in range(5):
            for j in range(5):
                if self.brd_state[i][j] == '*':
                    return False
        return True

    def brd_eval_fun(self, move, i, j, front, right, back, left):
        if move == 's':
                self.brd_curr_p1_eval += board_value[i][j]
                self.brd_curr_p2_eval -= board_value[i][j]
        elif move == 'r':
            # empty place
            self.brd_curr_p1_eval += board_value[i][j]
            self.brd_curr_p2_eval -= board_value[i][j]

            # check which neighbour contain O and then add those values in X and reduce twice that value from O
            if front:  # check front move
                self.brd_curr_p1_eval += 2*board_value[i + 1][j]
                self.brd_curr_p2_eval -= 2*board_value[i + 1][j]

            if right:  # check right move
                self.brd_curr_p1_eval += 2*board_value[i][j + 1]
                self.brd_curr_p2_eval -= 2*board_value[i][j + 1]

            if back:  # check back move
                self.brd_curr_p1_eval += 2*board_value[i - 1][j]
                self.brd_curr_p2_eval -= 2*board_value[i - 1][j]

            if left:  # check left move
                self.brd_curr_p1_eval += 2*board_value[i][j - 1]
                self.brd_curr_p2_eval -= 2*board_value[i][j - 1]

    def brd_sneak(self, i, j):
        next_board_state = copy.deepcopy(self.brd_state)
        next_board_state[i][j] = self.brd_p1
        next_sneak_node = Board(next_board_state, self.brd_p1, self.brd_p2)

        # Retain block for debugging
        print '\n\nSneak'
        print 'i, j:', i, j
        for t in range(5):
            print ("".join(map(str, next_sneak_node.brd_state[t])))
        print '\nNew_P1,Curr_P1:', next_sneak_node.brd_curr_p1_eval, self.brd_curr_p1_eval
        print '\nNew_P2, Curr_P2:', next_sneak_node.brd_curr_p2_eval, self.brd_curr_p2_eval

        return next_sneak_node

    def brd_raid(self, i, j):
        p1 = self.brd_p1
        p2 = self.brd_p2

        next_board_state = copy.deepcopy(self.brd_state)
        next_board_state[i][j] = self.brd_p1

        if i - 1 > 0:  # check back move
            if next_board_state[i - 1][j] == p2:
                next_board_state[i - 1][j] = p1

        if i + 1 < 5:  # check front move
            if next_board_state[i + 1][j] == p2:
                next_board_state[i + 1][j] = p1

        if j + 1 < 5:  # check right move
            if next_board_state[i][j + 1] == p2:
                next_board_state[i][j + 1] = p1

        if j - 1 > 0:  # check left move
            if next_board_state[i][j - 1] == p2:
                next_board_state[i][j - 1] = p1

        next_raid_node = Board(next_board_state, self.brd_p1, self.brd_p2)

        # Retain block for debugging
        print 'Raid'
        print 'i, j:', i, j
        for t in range(5):
            print ("".join(map(str, next_raid_node.brd_state[t])))
        print '\nNew_P1,Curr_P1:', next_raid_node.brd_curr_p1_eval, self.brd_curr_p1_eval
        print '\nNew_P2, Curr_P2:', next_raid_node.brd_curr_p2_eval, self.brd_curr_p2_eval

        return next_raid_node

    def brd_greedy_best_first_search(self):
        all_moves = []
        for i in range(5):
            for j in range(5):
                if self.brd_state[i][j] == '*':
                    if check_sneak(self.brd_state, i, j):
                        sneak_node = self.brd_sneak(i, j)
                        all_moves.append(sneak_node)
                    else:  # sneak not possible then its raid
                        raid_node = self.brd_raid(i, j)
                        all_moves.append(raid_node)

        all_moves_desc = sorted(all_moves, key=get_curr_p_eval, reverse=True)
        next_brd = all_moves_desc[0]

        print '\n\nFinal Move'
        for t in range(5):
            print ("".join(map(str, next_brd.brd_state[t])))
        print next_brd.brd_p1
        print 'P1 INIT,  P2 INIT', next_brd.brd_curr_p1_eval, next_brd.brd_curr_p2_eval
        return next_brd


def get_curr_p_eval(a_board):
        return a_board.brd_curr_p1_eval


def process_input(fn):
    file_handle = open(fn, "r")
    line_counter = 0

    global board_value
    global init_board
    global sym_choice
    global opp_choice
    global alg_choice
    global cut_off_p1
    # global cut_off_p2

    for line in file_handle:
        if line_counter == 0:
            alg_choice = line.strip('\n')
            line_counter += 1
        elif line_counter == 1:
            sym_choice = line.strip('\n')
            if sym_choice == 'X':
                opp_choice = 'O'
            else:
                opp_choice = 'X'
            line_counter += 1
        elif line_counter == 2:
            cut_off_p1 = int(line.strip('\n'))
            line_counter += 1
        elif line_counter > 2 and line_counter < 8:
            board_line = map(int, line.strip('\n').split())
            board_value.append(board_line)
            # i= chr(ord(i) + 1)
            line_counter += 1
        else:
            curr_line = list(line.strip('\n'))
            init_board.append(curr_line)
            # j = chr(ord(j) + 1)
            line_counter += 1


def check_sneak(curr_state, i, j):
    # check if any adjacent square contains sym_choice
    if i - 1 >= 0:  # check back move
        if curr_state[i - 1][j] == sym_choice:
            return False
    if i + 1 < 5:  # check front move
        if curr_state[i + 1][j] == sym_choice:
            return False
    if j + 1 < 5:  # check right move
        if curr_state[i][j + 1] == sym_choice:
            return False
    if j - 1 >= 0:  # check left move
        if curr_state[i][j - 1] == sym_choice:
            return False
    return True


# oop version not needed
def write_next_state(a_next_state):
    f = open("output.txt", "w")
    s = ""
    for i in range(5):
        s += "".join(map(str, a_next_state[i]))
        if i < 4:
            s += "\n"
    f.write(s)
    f.close()


def main():
    file_name = sys.argv[2]
    process_input(file_name)

    # process_input("input1.txt")
    # print "Algo choice", alg_choice
    # print "Symbol Choice", sym_choice
    # print "Cutoff", cut_off_p1
    # print "VALUE BOARD"
    # for key in board_value:
    #     print key
    # print "CURRENT BOARD"
    # for key in init_board:
    #     print key
    # if init_board[0][2] == sym_choice: print init_board[0][2]
    # print "sym_choice in main is", sym_choice

    # for alternating players reverse sym and opp in parameters
    input_board = Board(init_board, sym_choice, opp_choice)
    next_board = input_board.brd_greedy_best_first_search()
    write_next_state(next_board.brd_state)

    # eval_function(init_board)


if __name__ == '__main__':
    main()
