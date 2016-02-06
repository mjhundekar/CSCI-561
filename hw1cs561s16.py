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
game_flag = False
answer = 0
pointsMatrix = [[] for x in range(5)]
inputState = []
inputCounter = 0
playerScore = 0
opponentScore = 0
score = {}
play = ''
d = 0

logfile = open('log.txt', 'w')
traverse_log = open('traverse_log.txt', 'w')



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
        self.brd_name = assign_node_name(move, i, j)
        self.brd_depth = depth
        # self.cut_off = cut_off
        self.alpha = decimal.Decimal('-Infinity')  # max
        self.beta = decimal.Decimal('Infinity')  # min
        if self.brd_depth % 2 == 1:
            self.val_min_max = decimal.Decimal('Infinity')  # max
        elif self.brd_depth == 0:
            self.val_min_max = decimal.Decimal('-Infinity')  # max
        else:
            self.val_min_max = decimal.Decimal('Infinity')  # max

        self.v = decimal.Decimal('-Infinity')

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
        if i - 1 >= 0:  # check back move
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

        if j - 1 >= 0:  # check left move
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

        # print '\n\nFinal Move'
        # print next_brd.brd_to_string()
        # print next_brd.brd_p1
        # print 'P1 INIT,  P2 INIT', next_brd.brd_curr_p1_eval, next_brd.brd_curr_p2_eval
        return next_brd

    def brd_min_max(self, depth, cut_off, player):
        logfile.write('\nInside MIN_MAX\n Depth : ' + str(depth) + '\n' + self.brd_to_string())
        logfile.write('\n Evaluation P1 : P2 : ' + str(self.brd_curr_p1_eval) + ' ' + str(self.brd_curr_p2_eval))
        traverse_log.write(self.brd_name + ',' + str(self.brd_depth) + ',' + str(self.val_min_max) + '\n')
        next_move = self.max_move(depth, cut_off, player)
        # print next_move.brd_to_string()
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
                            sneak_node = self.brd_sneak(i, j, self.brd_depth + 1)
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
                        if depth % 2 == 1 and not depth == cut_off:
                            traverse_log.write(next_move.brd_name + ',' + str(next_move.brd_depth) + ',' + str(
                                next_move.val_min_max) + '\n')
                        # Call the min move on next move
                        next_min_move = next_move.min_move(depth, cut_off, player)
                        if depth == cut_off:
                            traverse_log.write(next_move.brd_name + ',' + str(next_move.brd_depth) + ',' + str(
                                next_move.val_min_max) + '\n')

                        if next_min_move.val_min_max > temp_max:
                            temp_max = next_min_move.val_min_max
                            next_move.val_min_max = temp_max
                            self.val_min_max = temp_max

                        if depth > 1:
                            traverse_log.write(next_move.brd_name + ',' + str(next_move.brd_depth) + ',' + str(
                                next_move.val_min_max) + '\n')

                        traverse_log.write(
                            self.brd_name + ',' + str(self.brd_depth) + ',' + str(self.val_min_max) + '\n')
                        all_moves.append(next_move)

            all_moves = sorted(all_moves, key=get_val_min_max, reverse=True)
            best_move = all_moves[0]

        logfile.write('\n\nBEST MAX_MOVE at depth : ' + str(depth) + '\n' + best_move.brd_to_string())
        logfile.write(
            '\nCheck Here Evaluation P1 : P2 : ' + str(best_move.brd_curr_p1_eval) + ' ' + str(
                best_move.brd_curr_p2_eval))

        return best_move

    def min_move(self, depth, cut_off, player):
        if self.end_game() or depth == cut_off:
            logfile.write('\nInside cut off MIN_MOVE\n Depth : ' + str(depth) + '\n' + self.brd_to_string())
            logfile.write('\n Evaluation P1 : P2 : ' + str(self.brd_curr_p1_eval) + ' ' + str(self.brd_curr_p2_eval))
            self.val_min_max = -self.brd_curr_p1_eval  # Important Fix
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
                            self.val_min_max = temp_min
                        if depth > 1:
                            traverse_log.write(next_move.brd_name + ',' + str(next_move.brd_depth) + ',' + str(
                                next_move.val_min_max) + '\n')
                        traverse_log.write(
                            self.brd_name + ',' + str(self.brd_depth) + ',' + str(self.val_min_max) + '\n')
                        all_moves.append(next_move)

            all_moves = sorted(all_moves, key=get_val_min_max, reverse=False)
            best_move = all_moves[0]

        logfile.write('\n\nBEST MIN_MOVE at depth : ' + str(depth) + '\n' + best_move.brd_to_string())
        logfile.write(
            '\n Evaluation P1 : P2 : ' + str(best_move.brd_curr_p1_eval) + ' ' + str(best_move.brd_curr_p2_eval))
        return best_move

    #######################################################################################################

    def brd_alpha_beta(self, depth, cut_off, player):
        logfile.write('\nInside MIN_MAX\n Depth : ' + str(depth) + '\n' + self.brd_to_string())
        logfile.write('\n Evaluation P1 : P2 : ' + str(self.brd_curr_p1_eval) + ' ' + str(self.brd_curr_p2_eval))
        (traverse_log.write(self.brd_name + ',' + str(self.brd_depth) + ',' + str(self.val_min_max) +
                            ',' + str(self.val_min_max) + ',' + str(self.alpha) +
                            ',' + str(self.beta) + '\n'))
        next_move = self.alpha_max_move(depth, cut_off, player)
        # print next_move.brd_to_string()
        return next_move

    def alpha_max_move(self, depth, cut_off, player):
        # check if game has ended or if we have reached the cut off depth
        if self.end_game() or depth == cut_off:
            logfile.write('\nInside cut off alpha_max_move\n Depth : ' + str(depth) + '\n' + self.brd_to_string())

            self.val_min_max = self.brd_curr_p1_eval
            self.v = self.brd_curr_p1_eval
            self.alpha = self.brd_curr_p1_eval
            # self.beta = self.brd_curr_p1_eval
            (logfile.write('\n Evaluation P1 : P2 : ' + str(self.brd_curr_p1_eval) + ' ' + str(self.brd_curr_p2_eval) +
                           ' ' + str(self.alpha) + ' ' + str(self.beta)))

            return self
        else:
            depth += 1
            temp_max = decimal.Decimal('-Infinity')
            all_moves = []

            # generate all moves for self
            logfile.write('\nGenerating all moves alpha_max_move: ' + str(self.brd_p1) + '\n Depth : ' + str(
                depth) + '\n' + self.brd_to_string())
            (logfile.write('\n Evaluation P1 : P2 : ' + str(self.brd_curr_p1_eval) + ' ' + str(self.brd_curr_p2_eval) +
                           ' ' + str(self.alpha) + ' ' + str(self.beta)))

            for i in range(5):
                for j in range(5):
                    if self.brd_state[i][j] == '*':
                        # next move either be sneak or raid
                        if self.brd_check_sneak(i, j):
                            sneak_node = self.brd_sneak(i, j, self.brd_depth + 1)
                            next_move = sneak_node
                            t = depth

                            logfile.write(
                                '\n\nNext SNEAK alpha_max_move \n Depth : ' + str(t) + ' i, j: ' + str(i) + ' ' + str(
                                    j) + '\n' + sneak_node.brd_to_string())
                            logfile.write('P1 : P2 : ' + sneak_node.brd_p1 + ' ' + sneak_node.brd_p2)
                            logfile.write('\n Evaluation P1 : P2 : ' + str(sneak_node.brd_curr_p1_eval) + ' ' + str(
                                sneak_node.brd_curr_p2_eval))

                        else:  # sneak not possible then its raid
                            raid_node = self.brd_raid(i, j, depth)
                            next_move = raid_node
                            t = depth

                            logfile.write(
                                '\n\nNext RAID alpha_max_move \n Depth :  ' + str(t) + ' i, j: ' + str(i) + ' ' + str(
                                    j) + '\n' + raid_node.brd_to_string())
                            logfile.write('P1 : P2 : ' + raid_node.brd_p1 + ' ' + raid_node.brd_p2)
                            logfile.write('\n Evaluation P1 : P2 : ' + str(raid_node.brd_curr_p1_eval) + ' ' + str(
                                raid_node.brd_curr_p2_eval))
                        next_move.alpha = self.alpha
                        next_move.beta = self.beta
                        logfile.write('\nBefore min Alpha : Beta: ' + str(next_move.alpha) + ' ' + str(next_move.beta))
                        next_beta_min_move = next_move.beta_min_move(depth, cut_off, player)
                        next_move.alpha = next_beta_min_move.beta
                        next_move.v = next_move.alpha
                        all_moves.append(next_move)
                        logfile.write('\nAfter min Alpha : Beta: ' + str(next_move.alpha) + ' ' + str(next_move.beta))

                        if next_beta_min_move.v > next_move.v:
                            # temp_max = next_min_move.val_min_max
                            next_move.v = next_beta_min_move.v
                            self.v = next_move.v

                        if next_move.beta <= next_move.alpha:
                            logfile.write(
                                '\n\nNext PRUNE alpha_max_move \n Depth :  ' + str(t) + ' i, j: ' + str(i) + ' ' + str(
                                    j) + '\n' + next_move.brd_to_string())
                            logfile.write('\nAlpha : Beta: ' + str(next_move.alpha) + ' ' + str(next_move.beta))
                            all_moves = sorted(all_moves, key=get_v, reverse=False)
                            best_move = all_moves[0]
                            return best_move
                        else:

                            if depth % 2 == 1 and not depth == cut_off:
                                (traverse_log.write(next_move.brd_name + ',' + str(next_move.brd_depth) + ',' +
                                                    str(next_move.v) + ',' + str(next_move.alpha) + ',' +
                                                    str(next_move.beta) + '\n'))
                            # Call the min move on next move

                            if depth == cut_off:
                                (traverse_log.write(next_move.brd_name + ',' + str(next_move.brd_depth) + ',' +
                                                    str(next_move.v) + ',' + str(next_move.alpha) + ',' +
                                                    str(next_move.beta) + '\n'))

                                # if next_beta_min_move.v > next_move.alpha:
                                #     temp_max = next_beta_min_move.v
                                #     next_move.alpha = temp_max
                                # best_move = next_move
                                # all_moves.append(next_move)
                                # self.val_min_max = temp_max

                                if depth > 1:
                                    (traverse_log.write(next_move.brd_name + ',' + str(next_move.brd_depth) +
                                                        ',' + str(next_move.v) + ',' + str(next_move.alpha) +
                                                        ',' + str(next_move.beta) + '\n'))

                                (traverse_log.write(self.brd_name + ',' + str(self.brd_depth) +
                                                    ',' + str(self.v) + ',' + str(self.alpha) +
                                                    ',' + str(self.beta) + '\n'))

                                # if next_move.alpha >= next_move.beta:
                                #     all_moves = sorted(all_moves, key=get_v, reverse=False)
                                #     best_move = all_moves[0]
                                #     return best_move

            all_moves = sorted(all_moves, key=get_v, reverse=True)
            best_move = all_moves[0]

        # logfile.write('\n\nBEST alpha_max_move at depth : ' + str(depth) + '\n' + best_move.brd_to_string())
        # logfile.write(
        #     '\nCheck Here Evaluation P1 : P2 : ' + str(best_move.brd_curr_p1_eval) + ' ' + str(best_move.brd_curr_p2_eval))
        # self.beta = best_move.alpha
        return best_move

    def beta_min_move(self, depth, cut_off, player):
        if self.end_game() or depth == cut_off:
            logfile.write('\nInside cut off beta_min_move\n Depth : ' + str(depth) + '\n' + self.brd_to_string())

            self.val_min_max = -self.brd_curr_p1_eval  # Important Fix
            self.v = -self.brd_curr_p1_eval
            self.beta = -self.brd_curr_p1_eval
            # self.alpha = -self.brd_curr_p1_eval
            (logfile.write('\n Evaluation P1 : P2 : ' + str(self.brd_curr_p1_eval) + ' ' + str(self.brd_curr_p2_eval)) +
             ' ' + str(self.alpha) + ' ' + str(self.beta))
            return self
        else:
            # generate all moves
            first_child = True
            depth += 1
            temp_min = decimal.Decimal('Infinity')
            all_moves = []

            logfile.write('\nGenerating all moves beta_min_move \n Depth : ' + str(depth) + '\n' + self.brd_to_string())
            (logfile.write('\n Evaluation P1 : P2 : ' + str(self.brd_curr_p1_eval) + ' ' + str(self.brd_curr_p2_eval) +
                           ' ' + str(self.alpha) + ' ' + str(self.beta)))

            for i in range(5):
                for j in range(5):
                    if self.brd_state[i][j] == '*':
                        if self.brd_check_sneak(i, j):
                            sneak_node = self.brd_sneak(i, j, depth)
                            next_move = sneak_node
                            t = depth

                            (logfile.write('\n\nNext SNEAK beta_min_move \n Depth : ' + str(t) + ' i, j: ' +
                                           str(i) + ' ' + str(j) + '\n' + sneak_node.brd_to_string()))
                            logfile.write('P1 : P2 : ' + sneak_node.brd_p1 + ' ' + sneak_node.brd_p2)
                            (logfile.write('\n Evaluation P1 : P2 : ' + str(sneak_node.brd_curr_p1_eval) +
                                           ' ' + str(sneak_node.brd_curr_p2_eval)))
                        else:  # sneak not possible then its raid
                            raid_node = self.brd_raid(i, j, depth)
                            next_move = raid_node
                            t = depth
                            (logfile.write('\n\nNext RAID beta_min_move \n Depth :  ' + str(t) + ' i, j: ' +
                                           str(i) + ' ' + str(j) + '\n' + raid_node.brd_to_string()))
                            logfile.write('P1 : P2 : ' + raid_node.brd_p1 + ' ' + raid_node.brd_p2)
                            (logfile.write('\n Evaluation P1 : P2 : ' + str(raid_node.brd_curr_p1_eval) +
                                           ' ' + str(raid_node.brd_curr_p2_eval)))
                        # logfile.write('\nAlpha : Beta: ' + next_move.alpha + ' ' + next_move.beta)
                        next_move.alpha = self.alpha
                        next_move.beta = self.beta
                        logfile.write(
                            '\nBefore alpha_max_move Alpha : Beta: ' + str(next_move.alpha) + ' ' + str(next_move.beta))
                        # if next_move.alpha == decimal.Decimal('-Infinity'):
                        #     first_child = False
                        next_alpha_max_move = next_move.alpha_max_move(depth, cut_off, player)
                        next_move.beta = next_alpha_max_move.alpha
                        # next_move.k = next_move.beta
                        all_moves.append(next_move)
                        logfile.write(
                            '\nAfter alpha_max_move Alpha : Beta: ' + str(next_move.alpha) + ' ' + str(next_move.beta))

                        if next_alpha_max_move.v < next_move.v:
                            next_move.v = next_alpha_max_move.v
                            self.v = next_move.v

                        if next_move.beta <= next_move.alpha:  # prune
                            logfile.write(
                                '\n\nNext PRUNE alpha_max_move \n Depth :  ' + str(t) + ' i, j: ' + str(i) + ' ' + str(
                                    j) + '\n' + next_move.brd_to_string())
                            logfile.write('\nAlpha : Beta: ' + str(next_move.alpha) + ' ' + str(next_move.beta))
                            all_moves = sorted(all_moves, key=get_v, reverse=False)
                            best_move = all_moves[0]
                            return best_move
                        else:  # process current node
                            # temp_min = next_alpha_max_move.v
                            # # next_move.beta = next_alpha_max_move.alpha
                            # next_move.v = temp_min
                            best_move = next_move
                            # all_moves.append(next_move)
                            if depth > 1:
                                (traverse_log.write(next_move.brd_name + ',' + str(next_move.brd_depth) + ',' +
                                                    str(next_move.v) + ',' + str(next_move.alpha) + ',' +
                                                    str(next_move.beta) + '\n'))
                            (traverse_log.write(self.brd_name + ',' + str(self.brd_depth) + ',' + str(self.v) +
                                                ',' + str(next_move.alpha) + ',' +
                                                str(next_move.beta) + '\n'))
                            # all_moves.append(next_move)

                            # all_moves = sorted(all_moves, key=get_v, reverse=False)
                            # best_move = all_moves[0]
                            # return best_move

            all_moves = sorted(all_moves, key=get_v, reverse=False)
            best_move = all_moves[0]

        logfile.write('\n\nBEST beta_min_move at depth : ' + str(depth) + '\n' + best_move.brd_to_string())
        logfile.write(
            '\n Evaluation P1 : P2 : ' + str(best_move.brd_curr_p1_eval) + ' ' + str(best_move.brd_curr_p2_eval))
        self.alpha = best_move.beta
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


###################################################################################################################


class AB_Game_State:
    def __init__(self, inputState, play, d, parent, scores={}, alpha=-9999, beta=9999):
        self.parent = parent
        self.inputState = list(inputState)
        self.play = play
        self.scores = scores
        self.d = d
        self.alpha = alpha
        self.beta = beta
        self.value = -9999
        if self.play == "X":
            self.opponent = "O"
        else:
            self.opponent = "X"


def check_sneak_raid(icounter, curr_game_state):
    row = icounter / 5
    column = icounter % 5
    if row + 1 < 5 and curr_game_state.inputState[row + 1][column] == curr_game_state.play:
        return "R"
    elif row - 1 >= 0 and curr_game_state.inputState[row - 1][column] == curr_game_state.play:
        return "R"
    elif column - 1 >= 0 and curr_game_state.inputState[row][column - 1] == curr_game_state.play:
        return "R"
    elif column + 1 < 5 and curr_game_state.inputState[row][column + 1] == curr_game_state.play:
        return "R"
    else:
        return "S"


def compute_raid_score(icounter, opp_score, curr_game_state):
    global pointsMatrix
    row = icounter / 5
    column = icounter % 5
    raid_score = int(pointsMatrix[row][column])
    # Forward
    if row + 1 < 5 and curr_game_state.inputState[row + 1][column] == curr_game_state.opponent:
        raid_score += int(pointsMatrix[row + 1][column])
        opp_score -= int(pointsMatrix[row + 1][column])
    # Back
    if row - 1 >= 0 and curr_game_state.inputState[row - 1][column] == curr_game_state.opponent:
        raid_score += int(pointsMatrix[row - 1][column])
        opp_score -= int(pointsMatrix[row - 1][column])
    # Left
    if column - 1 >= 0 and curr_game_state.inputState[row][column - 1] == curr_game_state.opponent:
        raid_score += int(pointsMatrix[row][column - 1])
        opp_score -= int(pointsMatrix[row][column - 1])
    # Right
    if column + 1 < 5 and curr_game_state.inputState[row][column + 1] == curr_game_state.opponent:
        raid_score += int(pointsMatrix[row][column + 1])
        opp_score -= int(pointsMatrix[row][column + 1])
        
    if play == curr_game_state.play:
        return raid_score + playScore - opp_score
    else:
        return (-1 * (raid_score + playScore - opp_score))


def get_state_name(x):
    if x == "root":
        return x
    if x % 5 == 0:
        return "A" + str((x / 5) + 1)
    elif x % 5 == 1:
        return "B" + str((x / 5) + 1)
    elif x % 5 == 2:
        return "C" + str((x / 5) + 1)
    elif x % 5 == 3:
        return "D" + str((x / 5) + 1)
    elif x % 5 == 4:
        return "E" + str((x / 5) + 1)


def formatOutput(x):
    if x == -9999:
        return "-Infinity"
    elif x == 9999:
        return "Infinity"
    else:
        return str(x)


def init_board_score(curr_game_state):
    global playScore
    global opponentScore
    global pointsMatrix
    playScore = 0
    opponentScore = 0
    for y in range(25):
        if curr_game_state.inputState[y / 5][y % 5] == curr_game_state.play:
            playScore += int(pointsMatrix[y / 5][y % 5])
        elif curr_game_state.inputState[y / 5][y % 5] == curr_game_state.opponent:
            opponentScore += int(pointsMatrix[y / 5][y % 5])


def get_next_board(position, gameState):
    inputState = list(gameState.inputState)
    inputState[position / 5] = inputState[position / 5][:position % 5] + gameState.play + inputState[position / 5][
                                                                                          position % 5 + 1:]
    if position % 5 - 1 >= 0 and inputState[position / 5][(position % 5) - 1] == gameState.opponent:
        inputState[position / 5] = inputState[position / 5][:position % 5 - 1] + gameState.play + inputState[
                                                                                                      position / 5][
                                                                                                  position % 5:]
    if position % 5 + 1 < 5 and inputState[position / 5][position % 5 + 1] == gameState.opponent:
        inputState[position / 5] = inputState[position / 5][:position % 5 + 1] + gameState.play + inputState[
                                                                                                      position / 5][
                                                                                                  position % 5 + 2:]
    if position / 5 - 1 >= 0 and inputState[position / 5 - 1][position % 5] == gameState.opponent:
        inputState[position / 5 - 1] = inputState[position / 5 - 1][:position % 5] + gameState.play + inputState[
                                                                                                          position / 5 - 1][
                                                                                                      position % 5 + 1:]
    if position / 5 + 1 < 5 and inputState[position / 5 + 1][position % 5] == gameState.opponent:
        inputState[position / 5 + 1] = inputState[position / 5 + 1][:position % 5] + gameState.play + inputState[
                                                                                                          position / 5 + 1][
                                                                                                      position % 5 + 1:]
    return inputState


def final_alpha_beta(curr_game_state, cut_off):
    global pointsMatrix
    if curr_game_state.d < cut_off - 1:
        for x in range(25):
            # trial check
            if curr_game_state.inputState[x / 5][x % 5] == "*":
                move = check_sneak_raid(x, curr_game_state)
                input1 = list(curr_game_state.inputState)
                if move == "S":
                    input1[x / 5] = curr_game_state.inputState[x / 5][:x % 5] + curr_game_state.play + curr_game_state.inputState[x / 5][
                                                                                           x % 5 + 1:]
                else:
                    input1 = get_next_board(x, curr_game_state)
                if curr_game_state.d % 2 == 1:
                    (traverse_log.write(str(get_state_name(x)) + "," + str(curr_game_state.d + 1) + ",-Infinity" + "," +
                                          formatOutput(curr_game_state.alpha) + "," + formatOutput(curr_game_state.beta) + '\n'))
                else:
                    (traverse_log.write(str(get_state_name(x)) + "," + str(curr_game_state.d + 1) + ",Infinity" + "," + formatOutput(
                        curr_game_state.alpha) + "," + formatOutput(curr_game_state.beta) + '\n'))
                newcurr_game_state = AB_Game_State(input1, curr_game_state.opponent, curr_game_state.d + 1, x, {}, curr_game_state.alpha,
                                         curr_game_state.beta)
                answer, curr_game_state.scores[x] = final_alpha_beta(newcurr_game_state, cut_off)
                if curr_game_state.alpha >= curr_game_state.beta:
                    break
                if curr_game_state.d % 2 == 1:
                    curr_game_state.value = curr_game_state.scores[min(curr_game_state.scores, key=curr_game_state.scores.get)]
                    curr_game_state.beta = curr_game_state.value
                    (traverse_log.write(str(get_state_name(curr_game_state.parent)) + "," + str(curr_game_state.d) + "," + str(
                        curr_game_state.value) + "," + formatOutput(curr_game_state.alpha) + "," + formatOutput(curr_game_state.beta) + '\n'))

                else:
                    curr_game_state.value = curr_game_state.scores[max(curr_game_state.scores, key=curr_game_state.scores.get)]
                    curr_game_state.alpha = curr_game_state.value
                    (traverse_log.write(str(get_state_name(curr_game_state.parent)) + "," + str(curr_game_state.d) + "," + str(
                        curr_game_state.value) + "," + formatOutput(curr_game_state.alpha) + "," + formatOutput(curr_game_state.beta) + '\n'))

    elif curr_game_state.d == cut_off - 1:
        init_board_score(curr_game_state)
        prev_alpha = "-Infinity"
        prev_beta = "Infinity"
        for x in range(25):
            if curr_game_state.inputState[x / 5][x % 5] == "*":
                move = check_sneak_raid(x, curr_game_state)
                if move == "S":
                    if play == curr_game_state.play:
                        curr_game_state.scores[x] = (int(pointsMatrix[x / 5][x % 5]) + (playScore - opponentScore))
                    else:
                        curr_game_state.scores[x] = -1 * (int(pointsMatrix[x / 5][x % 5]) + (playScore - opponentScore))
                else:
                    curr_game_state.scores[x] = (compute_raid_score(x, opponentScore, curr_game_state))
                (traverse_log.write(str(get_state_name(x)) + "," + str(curr_game_state.d + 1) + "," + str(curr_game_state.scores[x]) + "," + formatOutput(
                    curr_game_state.alpha) + "," + formatOutput(curr_game_state.beta) + '\n'))
                prev_alpha = curr_game_state.alpha
                prev_beta = curr_game_state.beta
                if curr_game_state.d % 2 == 1:
                    val = curr_game_state.scores[min(curr_game_state.scores, key=curr_game_state.scores.get)]
                    if curr_game_state.beta > val:
                        curr_game_state.beta = val
                else:
                    val = curr_game_state.scores[max(curr_game_state.scores, key=curr_game_state.scores.get)]
                    if curr_game_state.alpha < val:
                        curr_game_state.alpha = val
                curr_game_state.value = val
                if curr_game_state.alpha >= curr_game_state.beta:
                    (traverse_log.write(str(get_state_name(curr_game_state.parent)) + "," + str(curr_game_state.d) + "," + str(val) + "," + formatOutput(
                        prev_alpha) + "," + formatOutput(prev_beta) + '\n'))
                    break
                (traverse_log.write(str(get_state_name(curr_game_state.parent)) + "," + str(curr_game_state.d) + "," + str(val) + "," + formatOutput(
                    curr_game_state.alpha) + "," + formatOutput(curr_game_state.beta) + '\n'))
    if curr_game_state.d % 2 == 1:
        return min(curr_game_state.scores, key=curr_game_state.scores.get), curr_game_state.scores[
            min(curr_game_state.scores, key=curr_game_state.scores.get)]
    else:
        return max(curr_game_state.scores, key=curr_game_state.scores.get), curr_game_state.scores[
            max(curr_game_state.scores, key=curr_game_state.scores.get)]



def get_v(a_board):
    return a_board.v


def get_beta(a_board):
    return a_board.alpha


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

    global answer
    global pointsMatrix
    global inputState
    global inputCounter
    global playerScore
    global opponentScore
    global score
    global inputState
    global play
    global d
    global opponent
    global algorithm

    for line in file_handle:
        if line_counter == 0:
            alg_choice = int(line.strip('\n\r'))
            line_counter += 1
            algorithm = int(line.strip())
        elif line_counter == 1:
            sym_choice = line.strip('\n\r')
            play = line.strip()
            if sym_choice == 'X':
                opp_choice = 'O'
                opponent = "O"
            else:
                opp_choice = 'X'
                opponent = "X"
            line_counter += 1
        elif line_counter == 2:
            cut_off_p1 = int(line.strip('\n\r'))
            d = int(line.strip())
            line_counter += 1
        elif line_counter > 2 and line_counter < 8:
            board_line = map(int, line.strip('\n\r').split())
            board_value.append(board_line)
            pointsMatrix[line_counter - 3] = line.split()
            # i= chr(ord(i) + 1)
            line_counter += 1
        else:
            curr_line = list(line.strip('\n\r'))
            init_board.append(curr_line)
            inputState.append(line)
            # j = chr(ord(j) + 1)
            line_counter += 1


# oop version not needed
def write_next_state(a_next_state):
    print a_next_state
    f = open("next_state.txt", "w")
    s = ""
    for i in range(5):
        s = "".join(map(str, a_next_state[i]))
        # if i < 4:
        #     s += "\n"
        s = s.strip('\n\r')
        if i < 4:
            s += "\n"
        # s += '\n'
        f.write(s)
    f.close()

    # f = open("next_state.txt", "r")
    # lines = f.readlines()
    # f.close()
    # write = open('next_state.txt', 'w')
    # write.writelines([item for item in lines[:-1]])
    # write.close()


def write_next_state_ab(a_next_state):
    print a_next_state
    f = open("next_state.txt", "w")
    s = ""
    for i in range(5):
        s = "".join(map(str, a_next_state[i]))
        # if i < 4:
        #     s += "\n"
        f.write(s)
    f.close()


def assign_node_name(move, i, j):
    if i == j == 0 and move == 'i':
        name = 'root'
    else:
        alpha = chr(j + ord('A'))
        name = alpha + str(i + 1)
    return name


def main():
    file_name = sys.argv[2]
    process_input(file_name)
    global cut_off_p1
    global alg_choice
    global inputState
    global play
    global d


    # process_input("input5.txt")
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
        # print '\n\n\nMAIN NEXT BOARD'
        # print next_board.alpha
        # print next_board.beta
        # res = next_board.brd_to_string()
        # test_file = open('Test.txt','w')
        # test_file.write(res)
        # test_file.write(res)
        # test_file.write(res)
        # test_file.write(res)
    if alg_choice == 2:
        # print cut_off_p1
        # traverse_log = open('traverse_log.txt', 'w')
        traverse_log.write('Node,Depth,Value\n')
        next_board = input_board.brd_min_max(0, cut_off_p1, input_board.brd_p1)
        write_next_state(next_board.brd_state)
        traverse_log.close()

        read_traverse_log = open('traverse_log.txt', 'r')
        lines = read_traverse_log.readlines()
        read_traverse_log.close()

        write = open('traverse_log.txt', 'w')
        # write = open('traverse_log.txt', 'w')
        write.writelines([item for item in lines[:-1]])
        item = lines[-1].rstrip()
        write.write(item)
        write.close()

    if alg_choice == 3:
        gs = AB_Game_State(inputState, play, 0, "root")
        # print pointsMatrix
        # traverse_log = open('traverse_log.txt', 'w')
        traverse_log.write('Node,Depth,Value,Alpha,Beta\n')
        traverse_log.write("root," + str(0) + ",-Infinity" + "," + formatOutput(gs.alpha) + "," + formatOutput(gs.beta) + '\n')
        answer, value = final_alpha_beta(gs, d)
        # print answer
        traverse_log.close()

        read_traverse_log = open('traverse_log.txt', 'r')
        lines = read_traverse_log.readlines()
        read_traverse_log.close()

        write = open('traverse_log.txt', 'w')
        write.writelines([item for item in lines[:-1]])
        item = lines[-1].rstrip()
        write.write(item)
        write.close()
        final = get_next_board(answer, gs)
        write_next_state_ab(final)
        # print final


if __name__ == '__main__':
    main()
