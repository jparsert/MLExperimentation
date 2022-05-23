

from games.find_cheese1d import FindCheese1DGame
import random

GAME_SIZE = 20


class QLearningPlayer:
    def __init__(self):

        self.lr = 0.2
        self.discount = 0.9
        self.epsilon = 0.9

        self.q_table = [[0.0, 0.0]] * GAME_SIZE
        for i in range(0, GAME_SIZE):
            self.q_table[i] = [float(random.uniform(0,1)), float(random.uniform(0,1))]


learner = QLearningPlayer()

for i in range(50):

    game = FindCheese1DGame(GAME_SIZE)
    #game.render()

    old_score = game.game_score
    old_state = game.get_state().index("#")
    action_index = random.randint(0, 1)

    for _ in range(500):

        reward = 0.0
        if old_score < game.game_score:
            reward = 1.0
        elif old_score > game.game_score:
            reward = -1.0

        # Game state/i.e. position in board
        state = game.get_state().index("#")
        # update table
        learner.q_table[old_state][action_index] = learner.q_table[old_state][action_index] + learner.lr * \
                                                   (reward + learner.discount * max(learner.q_table[state]) -
                                                    learner.q_table[old_state][action_index])

        # save current state
        old_score = game.game_score
        old_state = state

        if random.uniform(0,1) > learner.epsilon:
            # random action/exploration
            action_index = random.randint(0, 1)
        else:
            action_index = learner.q_table[state].index(max(learner.q_table[state]))

        game.apply_action(action_index)


        #game.render()

    #print(learner.q_table)
    print("Generation {}\t score {}".format(i, game.game_score))

