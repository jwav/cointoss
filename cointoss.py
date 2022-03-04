#!/usr/bin/python3

"""
cointoss: a program demonstrating how massive inequalities can emerge from the recurrent playing of a fair game among a population

"""

# defaults
NB_PLAYERS = 100
NB_ROUNDS = 10
STARTING_SCORE = 100
BETTING_AMOUNT = 10

import random
import numpy as np
import matplotlib.pyplot as plt

def gini(x):
    """Found on the internet. Lost the URL.
    (Warning: This is a concise implementation, but it is O(n**2)
    in time and memory, where n = len(x).  *Don't* pass in huge
    samples!)"""
    # Mean absolute difference
    mad = np.abs(np.subtract.outer(x, x)).mean()
    # Relative mean absolute difference
    rmad = mad/np.mean(x)
    # Gini coefficient
    g = 0.5 * rmad
    return g

class GameRecorder:
    """Container class for easy recording of Game variables.
    Meant to be instanciated once in a Game object.
    """
    def __init__(self):
        self.scores = []
        self.nb_alive_players = []
        self.ginis = []

    def get(self, varname):
        """returns the value of `varname` within the instance's __dict__, or None if it cannot be found"""
        try: return self.__dict__[varname]
        except: return None

    def set(self, varname, value):
        """sets the value of `varname` within the instance's __dict__. returns True if successful, False if not"""
        try:
            self.__dict__[varname] = value
            return True
        except:
            return False

class Player:
    """Holds params and util functions relative to individual Players.
    Used in Game objects as an array of Players"""
    def __init__(self, id, score=STARTING_SCORE):
        self.id = id
        self.score = score

    @property
    def is_alive(self):
        return self.score > 0

class Game:
    """main object, meant to be run() in __main__"""
    def __init__(self, nb_players=NB_PLAYERS):
        # ensure parity of nb_players
        assert nb_players % 2 == 0
        # populate self.players
        self.players = [Player(id=i) for i in range(nb_players)]
        self.round = 0
        self.betting_amount = BETTING_AMOUNT
        self.rec = GameRecorder()

    @property
    def scores(self):
        return [p.score for p in self.players]

    @property
    def nb_players(self):
        return len(self.players)

    @property
    def nb_alive_players(self):
        return len([p for p in self.players if p.is_alive])

    @property
    def percent_alive_players(self):
        return 100.0 * (self.nb_alive_players / self.nb_players)
    
    def iterate(self):
        """iterates one round and increments self.round"""
        # pair players into random `duel` tuples
        ids = [i for i in range(self.nb_players)]
        random.shuffle(ids)
        # duels is a list of tuples, each tuple containing (a,b)
        # (a,b) will duel in this round
        duels = []
        for i in range(self.nb_players//2):
            duels.append((ids[i], ids[i+1]))

        # run duels
        for couple in duels:
            a,b = couple
            self.duel(a,b)

        self.rec.scores.append([p.score for p in self.players])
        self.rec.nb_alive_players.append(self.nb_alive_players)
        self.rec.ginis.append(gini(self.scores))
        self.round += 1

    def duel(self, playerid_1, playerid_2):
        """performs a coin toss, 0 or 1.
        if 0, player1 has its score incremented by 1 and player2 has its score decremented by 1.
        if 1, the opposite is performed.
        if one of the players has a score of 0, the duel is cancelled.
        """
        # check if zero score for either player, in which case cancel duel
        if self.players[playerid_1].score <= 0 or self.players[playerid_2].score <= 0:
            return

        result = random.randint(0,1)
        if result == 0:
            self.players[playerid_1].score += self.betting_amount
            self.players[playerid_2].score -= self.betting_amount
        else:
            self.players[playerid_1].score -= self.betting_amount
            self.players[playerid_2].score += self.betting_amount

    def plot_game(self):
        """plots the current state of the game"""
        close = False
        def on_keypress(event):
            global close
            if event.key == 'n':
                plt.clf()
            elif event.key == 'a':
                exit(1)

        plt.style.use("dark_background")
        x = np.array(range(len(self.players)))
        y = np.array(self.scores)
        # fig,ax = plt.subplots()
        # fig.canvas.mpl_connect('key_press_event', on_keypress)
        # ax.bar(x, y)
        # ax.set_title(f"player scores for round {self.round}. Press any key for next iteration")
        plt.title(f"player scores for round {self.round}. Press any key for next iteration")
        plt.bar(x, y)
        # plt.show()
        plt.draw()
        plt.pause(0.001)
        plt.waitforbuttonpress()
        plt.clf()


    def display(self, step=1, rounds:list=None, plot=True):
        """displays the current scores
        step: displays the game's status only for every `step`th round
        rounds: specify whch rounds to display
        plot: if True, plots game stats on a graph
        """
        if rounds is None:
            rounds=[]
        if self.round % step == 0 or self.round in rounds:
            scores = [player.score for player in self.players]
            print("round {} : ".format(self.round), end="")
            print(scores)
            g = gini(np.sort(np.array(scores)))
            print("gini:", g)
            print("nb alive:", self.nb_alive_players)

            if plot is True:
                self.plot_game()

    def display_summary(self, print_summary=True):
        """called at the end.
        displays the evolution of game variables across the played rounds
        """
        # 1. GENERAL CONFIG
        # game variables to display
        variables = [
                "ginis",
                "nb_alive_players",
                ]
        nb_subplots = len(variables)
        plt.close()
        # use dark mode. To be called before any other matplotlib function
        plt.style.use("dark_background")
        fig,axs = plt.subplots(nb_subplots)

        if print_summary:
            for i,varname in enumerate(variables):
                values = self.rec.get(varname)
                if not values:
                    print(f"could not find variable {varname} in recordings")
                    continue
                x = np.array([i for i in range(len(values))])
                axs[i].plot(x, np.array(values))
                # axs[i].set_title(varname)
                axs[i].set(ylabel=varname)

        # ginis = np.array([gini(s) for s in self.rec.scores])
        # plt.plot(x,ginis)
        # plt.title("gini")
        # plt.show()
        # alives = np.array(self.rec.nb_alive_players)
        # x = np.array(range(len(alives)))
        # plt.plot(x,alives)
        # plt.title("nb alive players")

        # fig.show()
        plt.show()


if __name__ == "__main__":
    game = Game()
    print("GAME_RUN")
    game.display()
    for round in range(1000):
        game.iterate()
        game.display(step=100, rounds=[0,1])
    print("GAME_END")
    game.display_summary()
