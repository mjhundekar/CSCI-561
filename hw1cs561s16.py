board_value = []
init_board = []
sym_choice = ''
opp_choice = ''
alg_choice = ''
cut_off = 0
max_i = 0
max_j = 0
max_x_eval = 0
max_o_eval = 0
import sys


def process_input(fn):
    file_handle = open(fn, "r")
    line_counter = 0

    global board_value
    global init_board
    global sym_choice
    global opp_choice
    global alg_choice
    global cut_off
    # i = "a"
    # j = "a"
    # board_value ={}
    # curr_board = {}
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


            # print board_value
            # print init_board
            # l= curr_board['a']
            # print l[2]


def eval_function(curr_state):
    init_x_eval = 0
    init_o_eval = 0
    init_b_eval = 0
    for (bvl, cbl) in zip(board_value, curr_state):
        # print key
        for (bvi, cbi) in zip(bvl, cbl):
            init_b_eval += bvi
            if (cbi == 'X'):
                init_x_eval += bvi
            elif (cbi == 'O'):
                init_o_eval += bvi

    curr_x_eval = init_x_eval - init_o_eval
    curr_o_eval = init_o_eval - init_x_eval

    # print init_b_eval
    # print init_x_eval
    # print init_o_eval

    # print curr_x_eval
    # print curr_o_eval
    evaluated = [curr_x_eval, curr_o_eval]
    return evaluated


def check_sneak(curr_state, i, j):
    if (i - 1 > 0):  # check back move
        if curr_state[i - 1][j] == sym_choice:
            return False
    if (i + 1 < 5):  # check front move
        # temp = curr_state[i + 1][j]
        # print temp
        if curr_state[i + 1][j] == sym_choice:
            return False
    if j + 1 < 5:  # check right move
        if curr_state[i][j + 1] == sym_choice:
            return False
    if j - 1 > 0:  # check left move
        if curr_state[i][j - 1] == sym_choice:
            return False
    else:
        return True


def sneak(curr_state, i, j):
    curr_state[i][j] = sym_choice
    global max_j
    global max_i
    global max_x_eval
    global max_o_eval
    # max_i = i
    # max_j = j
    [curr_x_eval, curr_o_eval] = eval_function(curr_state)
    if sym_choice=='X':
        if curr_x_eval > max_x_eval:  # if eval function is higher remember change
            max_i = i
            max_j = j
            max_x_eval = curr_x_eval
    else:
        if curr_o_eval > max_o_eval:  # if eval function is higher remember change
            max_i = i
            max_j = j
            max_o_eval = curr_o_eval
    curr_state[i][j] = '*'  # revert the change made at i,j
    # sneak_return = [max_i, max_j]  #since golobal noneed to return i think
    # return sneak_return
    # else:
    #     curr_state[i][j] = '*'  # revert the change made at i,j
    #     return [i, j, max_x_eval]


def raid(curr_state, i, j):
    global max_j
    global max_i
    global max_x_eval
    global max_o_eval
    # max_i = i
    # max_j = j
    back_flip = False
    front_flip = False
    right_flip = False
    left_flip = False
    curr_state[i][j] = sym_choice
    if (i - 1 > 0):  # check back move
        if curr_state[i - 1][j] == opp_choice:
            curr_state[i - 1][j] = sym_choice
            back_flip = True
    if i + 1 < 5:  # check front move
        if curr_state[i + 1][j] == opp_choice:
            curr_state[i + 1][j] = sym_choice
            front_flip = True
    if j + 1 < 5:  # check right move
        if curr_state[i][j + 1] == opp_choice:
            curr_state[i][j + 1] = sym_choice
            right_flip = True
    if j - 1 > 0:  # check left move
        if curr_state[i][j - 1] == opp_choice:
            curr_state[i][j - 1] = sym_choice
            left_flip = True
    [curr_x_eval, curr_o_eval] = eval_function(curr_state)
    if sym_choice=='X':
        if curr_x_eval > max_x_eval:  # if eval function is higher remember change
            max_i = i
            max_j = j
            max_x_eval = curr_x_eval
    else:
        if curr_o_eval > max_o_eval:  # if eval function is higher remember change
            max_i = i
            max_j = j
            max_o_eval = curr_o_eval

    if front_flip:
        curr_state[i + 1][j] = opp_choice
    if right_flip:
        curr_state[i][j + 1] = opp_choice
    if back_flip:
        curr_state[i - 1][j] = opp_choice
    if left_flip:
        curr_state[i][j - 1] = opp_choice
    # raid_return = [max_i, max_j]
    # return raid_return


def greedy_best_first_search(curr_state):

    global max_i
    global max_j
    global  max_x_eval
    [max_x_eval, max_o_eval] = eval_function(curr_state)
    for i in range(5):
        for j in range(5):
            if curr_state[i][j] == '*':
                if (check_sneak(curr_state, i, j)):
                    # [max_i, max_j, max_x_eval] = sneak(curr_state, i, j)
                    sneak(curr_state, i, j)
                else:  # sneak not possible then its raid
                    # [max_i, max_j, max_x_eval] = raid(curr_state, i, j)
                    raid(curr_state, i, j)

    curr_state[max_i][max_j] = sym_choice
    f = open("output.txt", "w")
    s = ""
    for i in range(5):
        s += "".join(map(str, curr_state[i]))
        if i< 4:
            s += "\n"
    f.write(s)
    f.close()


def main():
    file_name = sys.argv[2]


    # process_input("input.txt")
    process_input(file_name)


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
    # print "symchoice in main is", sym_choice
    greedy_best_first_search(init_board)
    # eval_function(init_board)


if __name__ == '__main__':
    main()
