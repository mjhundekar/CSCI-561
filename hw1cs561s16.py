import copy
import sys
import decimal

board_value = []
init_board = []
sym_choice = ''
opp_choice = ''
alg_choice = ''
cut_off_p1 = 0
cut_off_p2 = 0

logfile = open('log.txt', 'w')


class Board:
    def __init__(self, curr_state, player, opponent, move, i, j, depth, next_p1_eval, next_p2_eval):
        """

        :rtype: Board
        """
        self.brd_state = copy.deepcopy(curr_state)
        self.brd_p1 = player
        self.brd_p2 = opponent
        self.brd_raid_flag = False
        self.brd_move = move
        self.brd_curr_p1_eval, self.brd_curr_p2_eval = \
            self.brd_eval_function(move, next_p1_eval, next_p2_eval)
        self.brd_name = assign_node_name(i, j)
        self.brd_depth = depth
        # self.cut_off = cut_off
        self.alpha = decimal.Decimal('-Infinity')  # max
        self.beta = decimal.Decimal('Infinity')    # min
        self.val_min_max = decimal.Decimal('-Infinity')  # max

    def __str__(self):
        # TODO
        pass

    def __repr__(self):
        # DONE
        return self.__str__()

    def brd_to_string(self):
        str_board = []
        for t in range(5):
            str_board.append(("".join(map(str, self.brd_state[t]))))
        str_board[:] = ['\n'.join(str_board[:])]
        str_board[0] += '\n'
        return str(str_board[0])
        pass

    def brd_eval_function(self, move, next_p1_eval, next_p2_eval):
        init_p1_eval = 0
        init_p2_eval = 0
        init_b_eval = 0

        if move == 'i':  # Root node need to evaluate from scratch
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
        else:
            evaluated = [next_p1_eval, next_p2_eval]

        return evaluated

    def end_game(self):
        for i in range(5):
            for j in range(5):
                if self.brd_state[i][j] == '*':
                    return False
        return True

    def brd_sneak(self, i, j, depth):
        next_board_state = copy.deepcopy(self.brd_state)
        next_board_state[i][j] = self.brd_p1

        next_p2_eval = self.brd_curr_p1_eval
        next_p1_eval = self.brd_curr_p2_eval

        next_p2_eval += board_value[i][j]
        next_p1_eval -= board_value[i][j]

        # in the next board p1 and p2 will swap
        next_sneak_node = \
            Board(next_board_state, self.brd_p2, self.brd_p1, 's', i, j, depth, next_p1_eval, next_p2_eval)

        # Retain block for debugging
        # logfile.write('\n\nSneak')
        # logfile.write(('\ni, j: ' + str(i) + ' ' + str(j)))
        # logfile.write(next_sneak_node.brd_to_string())
        # logfile.write(('\nNew_P1, Curr_P1:' + str(next_sneak_node.brd_curr_p1_eval) + ' ' + str(self.brd_curr_p1_eval)))
        # logfile.write(('\nNew_P2, Curr_P2:' + str(next_sneak_node.brd_curr_p2_eval) + ' ' + str(self.brd_curr_p2_eval)))
        # for t in range(5):
        #     logfile.write(("".join(map(str, next_sneak_node.brd_state[t]))))

        return next_sneak_node

    def brd_raid(self, i, j, depth):
        p1 = self.brd_p1
        p2 = self.brd_p2

        next_board_state = copy.deepcopy(self.brd_state)
        next_board_state[i][j] = self.brd_p1

        next_p1_eval = self.brd_curr_p2_eval
        next_p2_eval = self.brd_curr_p1_eval

        next_p2_eval += board_value[i][j]
        next_p1_eval -= board_value[i][j]

        # P1 and P2 are previous state p1 p2
        if i - 1 > 0:  # check back move
            if next_board_state[i - 1][j] == p2:
                next_board_state[i - 1][j] = p1
                next_p1_eval -= 2 * board_value[i - 1][j]
                next_p2_eval += 2 * board_value[i - 1][j]
                # print 'Back Captured', curr_p1_eval, curr_p2_eval

        if i + 1 < 5:  # check front move
            if next_board_state[i + 1][j] == p2:
                next_board_state[i + 1][j] = p1
                next_p1_eval -= 2 * board_value[i + 1][j]
                next_p2_eval += 2 * board_value[i + 1][j]
                # print 'Front Captured', curr_p1_eval, curr_p2_eval

        if j + 1 < 5:  # check right move
            if next_board_state[i][j + 1] == p2:
                next_board_state[i][j + 1] = p1
                next_p1_eval -= 2 * board_value[i][j + 1]
                next_p2_eval += 2 * board_value[i][j + 1]
                # print 'Right Captured', curr_p1_eval, curr_p2_eval

        if j - 1 > 0:  # check left move
            if next_board_state[i][j - 1] == p2:
                next_board_state[i][j - 1] = p1
                next_p1_eval -= 2 * board_value[i][j - 1]
                next_p2_eval += 2 * board_value[i][j - 1]
                # print 'Left Captured', curr_p1_eval, curr_p2_eval

        next_raid_node = Board(next_board_state, self.brd_p2, self.brd_p1, 'r', i, j, depth, next_p1_eval, next_p2_eval)

        # Retain block for debugging
        # logfile.write('\n\nRaid')
        # logfile.write(('\ni, j: ' + str(i) + ' ' + str(j)))
        # logfile.write(('\nNew_P1, Curr_P1:' + str(next_raid_node.brd_curr_p1_eval) + ' ' + str(self.brd_curr_p1_eval)))
        # logfile.write(('\nNew_P2, Curr_P2:' + str(next_raid_node.brd_curr_p2_eval) + ' ' + str(self.brd_curr_p2_eval)))

        return next_raid_node

    def brd_greedy_best_first_search(self):
        all_moves = []
        for i in range(5):
            for j in range(5):
                if self.brd_state[i][j] == '*':
                    if self.brd_check_sneak(i, j):
                        sneak_node = self.brd_sneak(i, j, 1)
                        logfile.write(
                            '\n\nNext SNEAK i, j : ' + str(i) + ' ' + str(j) + '\n' + sneak_node.brd_to_string())
                        logfile.write('P1 : P2 : ' + sneak_node.brd_p1 + ' ' + sneak_node.brd_p2)
                        logfile.write('\n Evaluation P1 : P2 : ' + str(sneak_node.brd_curr_p1_eval) + ' ' + str(
                            sneak_node.brd_curr_p2_eval))
                        all_moves.append(sneak_node)
                    else:  # sneak not possible then its raid
                        raid_node = self.brd_raid(i, j, 1)
                        logfile.write(
                            '\n\nNext Raid i, j : ' + str(i) + ' ' + str(j) + '\n' + raid_node.brd_to_string())
                        logfile.write('P1 : P2 : ' + raid_node.brd_p1 + ' ' + raid_node.brd_p2)
                        logfile.write('\n Evaluation P1 : P2 : ' + str(raid_node.brd_curr_p1_eval) + ' ' + str(
                            raid_node.brd_curr_p2_eval))
                        all_moves.append(raid_node)

        all_moves_desc = sorted(all_moves, key=get_curr_p2_eval, reverse=True)
        next_brd = all_moves_desc[0]

        print '\n\nFinal Move'
        # for t in range(5):
        #     print ("".join(map(str, next_brd.brd_state[t])))
        print next_brd.brd_to_string()
        print next_brd.brd_p1
        print 'P1 INIT,  P2 INIT', next_brd.brd_curr_p1_eval, next_brd.brd_curr_p2_eval
        return next_brd

    def brd_min_max(self, depth, cut_off, player):
        logfile.write('\nInside MIN_MAX\n Depth : ' + str(depth) + '\n' + self.brd_to_string())
        logfile.write('\n Evaluation P1 : P2 : ' + str(self.brd_curr_p1_eval) + ' ' + str(self.brd_curr_p2_eval))
        next_move = self.max_move(depth, cut_off, player)
        print next_move.brd_to_string()
        return next_move

    def max_move(self, depth, cut_off, player):
        # check if game has ended or if we have reached the cut off depth
        if self.end_game() or depth == cut_off:
            logfile.write('\nInside cut off MAX_MOVE\n Depth : ' + str(depth) + '\n' + self.brd_to_string())
            logfile.write('\n Evaluation P1 : P2 : ' + str(self.brd_curr_p1_eval) + ' ' + str(self.brd_curr_p2_eval))
            self.val_min_max = self.brd_curr_p1_eval
            return self
        else:
            depth += 1
            temp_max = decimal.Decimal('-Infinity')
            all_moves = []

            # generate all moves for self
            logfile.write('\nGenerating all moves MAX_MOVE: ' + str(self.brd_p1) + '\n Depth : ' + str(
                depth) + '\n' + self.brd_to_string())
            logfile.write('\n Evaluation P1 : P2 : ' + str(self.brd_curr_p1_eval) + ' ' + str(self.brd_curr_p2_eval))

            for i in range(5):
                for j in range(5):
                    if self.brd_state[i][j] == '*':
                        # next move either be sneak or raid
                        if self.brd_check_sneak(i, j):
                            sneak_node = self.brd_sneak(i, j, depth)
                            next_move = sneak_node
                            t = depth

                            logfile.write(
                                '\n\nNext SNEAK MAX_MOVE \n Depth : ' + str(t) + ' i, j: ' + str(i) + ' ' + str(
                                    j) + '\n' + sneak_node.brd_to_string())
                            logfile.write('P1 : P2 : ' + sneak_node.brd_p1 + ' ' + sneak_node.brd_p2)
                            logfile.write('\n Evaluation P1 : P2 : ' + str(sneak_node.brd_curr_p1_eval) + ' ' + str(
                                sneak_node.brd_curr_p2_eval))

                        else:  # sneak not possible then its raid
                            raid_node = self.brd_raid(i, j, depth)
                            next_move = raid_node
                            t = depth

                            logfile.write(
                                '\n\nNext RAID MAX_MOVE \n Depth :  ' + str(t) + ' i, j: ' + str(i) + ' ' + str(
                                    j) + '\n' + raid_node.brd_to_string())
                            logfile.write('P1 : P2 : ' + raid_node.brd_p1 + ' ' + raid_node.brd_p2)
                            logfile.write('\n Evaluation P1 : P2 : ' + str(raid_node.brd_curr_p1_eval) + ' ' + str(
                                raid_node.brd_curr_p2_eval))

                        # Call the min move on next move
                        next_min_move = next_move.min_move(depth, cut_off, player)

                        if next_min_move.val_min_max > temp_max:
                            temp_max = next_min_move.val_min_max
                            next_move.val_min_max = temp_max

                        all_moves.append(next_move)

            all_moves = sorted(all_moves, key=get_val_min_max, reverse=True)
            best_move = all_moves[0]

        logfile.write('\n\nBEST MAX_MOVE at depth : ' + str(depth) + '\n' + best_move.brd_to_string())
        logfile.write(
            '\nCheck Here Evaluation P1 : P2 : ' + str(best_move.brd_curr_p1_eval) + ' ' + str(best_move.brd_curr_p2_eval))
        return best_move

    def min_move(self, depth, cut_off, player):
        if self.end_game() or depth == cut_off:
            logfile.write('\nInside cut off MIN_MOVE\n Depth : ' + str(depth) + '\n' + self.brd_to_string())
            logfile.write('\n Evaluation P1 : P2 : ' + str(self.brd_curr_p1_eval) + ' ' + str(self.brd_curr_p2_eval))
            self.val_min_max = self.brd_curr_p1_eval
            return self
        else:
            # generate all moves
            depth += 1
            temp_min = decimal.Decimal('Infinity')
            all_moves = []

            logfile.write('\nGenerating all moves MIN_MOVE \n Depth : ' + str(depth) + '\n' + self.brd_to_string())
            logfile.write('\n Evaluation P1 : P2 : ' + str(self.brd_curr_p1_eval) + ' ' + str(self.brd_curr_p2_eval))

            for i in range(5):
                for j in range(5):
                    if self.brd_state[i][j] == '*':
                        if self.brd_check_sneak(i, j):
                            sneak_node = self.brd_sneak(i, j, depth)
                            next_move = sneak_node
                            t = depth

                            (logfile.write('\n\nNext SNEAK MIN_MOVE \n Depth : ' + str(t) + ' i, j: ' +
                                           str(i) + ' ' + str(j) + '\n' + sneak_node.brd_to_string()))
                            logfile.write('P1 : P2 : ' + sneak_node.brd_p1 + ' ' + sneak_node.brd_p2)
                            (logfile.write('\n Evaluation P1 : P2 : ' + str(sneak_node.brd_curr_p1_eval) +
                                           ' ' + str(sneak_node.brd_curr_p2_eval)))
                        else:  # sneak not possible then its raid
                            raid_node = self.brd_raid(i, j, depth)
                            next_move = raid_node
                            t = depth
                            (logfile.write('\n\nNext RAID MIN_MOVE \n Depth :  ' + str(t) + ' i, j: ' +
                                           str(i) + ' ' + str(j) + '\n' + raid_node.brd_to_string()))
                            logfile.write('P1 : P2 : ' + raid_node.brd_p1 + ' ' + raid_node.brd_p2)
                            (logfile.write('\n Evaluation P1 : P2 : ' + str(raid_node.brd_curr_p1_eval) +
                                           ' ' + str(raid_node.brd_curr_p2_eval)))

                        next_max_move = next_move.max_move(depth, cut_off, player)
                        if next_max_move.val_min_max < temp_min:
                            temp_min = next_max_move.val_min_max
                            next_move.val_min_max = temp_min

                        all_moves.append(next_move)

            all_moves = sorted(all_moves, key=get_val_min_max, reverse=False)
            best_move = all_moves[0]

        logfile.write('\n\nBEST MIN_MOVE at depth : ' + str(depth) + '\n' + best_move.brd_to_string())
        logfile.write(
            '\n Evaluation P1 : P2 : ' + str(best_move.brd_curr_p1_eval) + ' ' + str(best_move.brd_curr_p2_eval))

        return best_move

    def brd_check_sneak(self, i, j):
        # check if any adjacent square contains sym_choice
        if i - 1 >= 0:  # check back move
            if self.brd_state[i - 1][j] == self.brd_p1:
                return False
        if i + 1 < 5:  # check front move
            if self.brd_state[i + 1][j] == self.brd_p1:
                return False
        if j + 1 < 5:  # check right move
            if self.brd_state[i][j + 1] == self.brd_p1:
                return False
        if j - 1 >= 0:  # check left move
            if self.brd_state[i][j - 1] == self.brd_p1:
                return False
        return True


def get_val_min_max(a_board):
    return a_board.val_min_max


def get_curr_p1_eval(a_board):
    return a_board.brd_curr_p1_eval


def get_curr_p2_eval(a_board):
    return a_board.brd_curr_p2_eval


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
            alg_choice = int(line.strip('\n'))
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


def assign_node_name(i, j):
    if i == j == 0:
        name = 'root'
    else:
        alpha = chr(0 + ord('A'))
        name = alpha + str(j)
    return name


def main():
    file_name = sys.argv[2]
    process_input(file_name)
    global cut_off_p1
    global alg_choice

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
    input_board = Board(init_board, sym_choice, opp_choice, 'i', 0, 0, 0, 0, 0)
    #   0, 0, 0, 0, 0)
    if alg_choice == 1:
        next_board = input_board.brd_greedy_best_first_search()
        write_next_state(next_board.brd_state)
        print '\n\n\nMAIN NEXT BOARD'
        # print next_board.alpha
        # print next_board.beta
        # res = next_board.brd_to_string()
        # test_file = open('Test.txt','w')
        # test_file.write(res)
        # test_file.write(res)
        # test_file.write(res)
        # test_file.write(res)
    if alg_choice == 2:
        print cut_off_p1
        next_board = input_board.brd_min_max(0, cut_off_p1, input_board.brd_p1)
        write_next_state(next_board.brd_state)


if __name__ == '__main__':
    main()
