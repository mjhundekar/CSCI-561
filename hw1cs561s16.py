import copy
import sys

board_value = []
init_board = []
sym_choice = ''
opp_choice = ''
alg_choice = ''
cut_off = 0


class Board:
    def __init__(self, curr_state, player, opponent):
        self.brd_state = copy.deepcopy(curr_state)
        self.brd_p1 = player
        self.brd_p2 = opponent
        self.brd_x_eval, self.brd_o_eval = eval_function(self.brd_state)
        self.brd_max_i = 0
        self.brd_max_j = 0
        self.brd_max_x_eval = 0
        self.brd_max_o_eval = 0
        self.brd_raid_flag = False

    def end_game(self):
        for i in range(5):
            for j in range(5):
                if self.brd_state[i][j] == '*':
                    return False
        return True

    def brd_sneak(self, i, j):
        self.brd_state[i][j] = sym_choice
        [curr_x_eval, curr_o_eval] = eval_function(self.brd_state)
        p1 = self.brd_p1
        # p2 = self.brd_p2

        # Retain block for debugging
        print 'Sneak'
        print 'i, j:', i, j
        for t in range(5):
            print ("".join(map(str, self.brd_state[t])))
        print '\nMax_X, X:', self.brd_max_x_eval, curr_x_eval
        print '\nMax_O, O:', self.brd_max_o_eval, curr_o_eval
        print self.brd_raid_flag
        print 'max_i, max_j:', self.brd_max_i, self.brd_max_j

        if p1 == 'X':
            if curr_x_eval > self.brd_max_x_eval:  # if eval function is higher remember change
                self.brd_max_i = i
                self.brd_max_j = j
                self.brd_max_x_eval = curr_x_eval
                self.brd_raid_flag = False
        else:
            if curr_o_eval > self.brd_max_o_eval:  # if eval function is higher remember change
                self.brd_max_i = i
                self.brd_max_j = j
                self.brd_max_o_eval = curr_o_eval
                self.brd_raid_flag = False
        self.brd_state[i][j] = '*'  # revert the change made at i,j

        # Retain block for debugging
        print '\nSneak after revert'
        for t in range(5):
            print ("".join(map(str, self.brd_state[t])))

    def brd_raid(self, i, j):
        back_flip = False
        front_flip = False
        right_flip = False
        left_flip = False

        p1 = self.brd_p1
        p2 = self.brd_p2

        self.brd_state[i][j] = p1

        if i - 1 > 0:  # check back move
            if self.brd_state[i - 1][j] == p2:
                self.brd_state[i - 1][j] = p1
                back_flip = True

        if i + 1 < 5:  # check front move
            if self.brd_state[i + 1][j] == p2:
                self.brd_state[i + 1][j] = p1
                front_flip = True

        if j + 1 < 5:  # check right move
            if self.brd_state[i][j + 1] == p2:
                self.brd_state[i][j + 1] = p1
                right_flip = True

        if j - 1 > 0:  # check left move
            if self.brd_state[i][j - 1] == p2:
                self.brd_state[i][j - 1] = p1
                left_flip = True

        [curr_x_eval, curr_o_eval] = eval_function(self.brd_state)

        # Retain block for debugging
        print 'Raid'
        print 'i, j:', i, j
        for t in range(5):
            print ("".join(map(str, self.brd_state[t])))
        print 'Max_X, X:', self.brd_max_x_eval, curr_x_eval
        print 'Max_O, O:', self.brd_max_o_eval, curr_o_eval
        print self.brd_raid_flag
        print 'self.brd_max_i, self.brd_max_j:', self.brd_max_i, self.brd_max_j

        if p1 == 'X':
            if curr_x_eval > self.brd_max_x_eval:  # if eval function is higher remember change
                self.brd_max_i = i
                self.brd_max_j = j
                self.brd_max_x_eval = curr_x_eval
                self.brd_raid_flag = True
        else:
            if curr_o_eval > self.brd_max_o_eval:  # if eval function is higher remember change
                self.brd_max_i = i
                self.brd_max_j = j
                self.brd_max_o_eval = curr_o_eval
                self.brd_raid_flag = True

        # revert changes
        self.brd_state[i][j] = '*'
        if front_flip:
            self.brd_state[i + 1][j] = p2
        if right_flip:
            self.brd_state[i][j + 1] = p2
        if back_flip:
            self.brd_state[i - 1][j] = p2
        if left_flip:
            self.brd_state[i][j - 1] = p2

        # Retain block for debugging
        print '\nRaid after revert'
        print 'i, j:', i, j
        for t in range(5):
            print ("".join(map(str, self.brd_state[t])))

    def brd_make_move(self):
        next_brd_state = copy.deepcopy(self.brd_state)
        p1 = self.brd_p1
        p2 = self.brd_p2
        # change i,j
        i = self.brd_max_i
        j = self.brd_max_j
        next_brd_state[i][j] = p1

        # print 'Make Move:',i, j, self.brd_raid_flag

        if self.brd_raid_flag:
            self.brd_raid_flag = False
            if i - 1 > 0:  # change back move
                if next_brd_state[i - 1][j] == p2:
                    next_brd_state[i - 1][j] = p1

            if i + 1 < 5:  # change front move
                if next_brd_state[i + 1][j] == p2:
                    next_brd_state[i + 1][j] = p1

            if j + 1 < 5:  # check right move
                if next_brd_state[i][j + 1] == p2:
                    next_brd_state[i][j + 1] = p1

            if j - 1 > 0:  # check left move
                if next_brd_state[i][j - 1] == p2:
                    next_brd_state[i][j - 1] = p1
        # write_next_state(next_brd_state)
        return next_brd_state

    def brd_greedy_best_first_search(self):
        [self.brd_max_x_eval, self.brd_max_o_eval] = eval_function(self.brd_state)
        for i in range(5):
            for j in range(5):
                if self.brd_state[i][j] == '*':
                    if check_sneak(self.brd_state, i, j):
                        self.brd_sneak(i, j)
                    else:  # sneak not possible then its raid
                        self.brd_raid(i, j)
        next_brd_state = self.brd_make_move()
        next_brd = Board(next_brd_state, self.brd_p1, self.brd_p2)
        return next_brd


def process_input(fn):
    file_handle = open(fn, "r")
    line_counter = 0

    global board_value
    global init_board
    global sym_choice
    global opp_choice
    global alg_choice
    global cut_off

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
            cut_off = int(line.strip('\n'))
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


def eval_function(curr_state):
    init_x_eval = 0
    init_o_eval = 0
    init_b_eval = 0
    for (bvl, csl) in zip(board_value, curr_state):
        # print key
        for (bvi, cbi) in zip(bvl, csl):
            init_b_eval += bvi
            if cbi == 'X':
                init_x_eval += bvi
            elif cbi == 'O':
                init_o_eval += bvi

    curr_x_eval = init_x_eval - init_o_eval
    curr_o_eval = init_o_eval - init_x_eval
    evaluated = [curr_x_eval, curr_o_eval]
    return evaluated


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
    # process_input("input.txt")
    # print "Algo choice", alg_choice
    # print "Symbol Choice", sym_choice
    # print "Cutoff", cut_off
    # print "VALUE BOARD"
    # for key in board_value:
    #     print key
    # print "CURRENT BOARD"
    # for key in init_board:
    #     print key
    # if init_board[0][2] == sym_choice: print init_board[0][2]
    # print "sym_choice in main is", sym_choice
    input_board = Board(init_board, sym_choice, opp_choice)
    next_board = input_board.brd_greedy_best_first_search()
    write_next_state(next_board.brd_state)

    # eval_function(init_board)


if __name__ == '__main__':
    main()
