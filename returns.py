import numpy as np
import matplotlib.pyplot as plt
import math
''' This is a simulation of what our returns would look like if we bet on all
games each week, we bet evenly on all games, our returns are independent, and 
we follow a strategy such that we bet a percent of our total investment each 
week.  The histogram plot is of the log returns.  Values are final money for 
an investment of 1'''

def simulateReturns(p, bet_percent, years):
    # p = Success rate
    # bet_percent = amount of money to bet each week as a percent of total.  
    # number of simulations 
    simulations = 10000
    payoff = []
    final_payoff = np.array([])
    count = 0
    for i in range(simulations):
        bet = 1
        for i in range(17 * years):
            wins = np.random.binomial(15, p)
            losses = 15 - wins
            bet += bet_percent * bet * (wins * 10/11.0 - losses) / 15.0
            if bet <= 0:
                count += 1
                print 'Ran out of money %i times!' %count
            payoff.append(bet)
        final_payoff = np.append(final_payoff, payoff[-1])
    # plotting the log of the payoff because it is gaussian
    plt.hist(np.log(final_payoff))
    print 'min', final_payoff.min(), 'mean', final_payoff.mean(), 'std', final_payoff.std()


def pEst(wins, losses):
    '''Estimates the distribution of p given a number of wins and losses.  
    This is correct up to a normalization constant'''
    x = np.linspace(0, 1, 100)
    norm = math.factorial(wins + losses + 1) / (math.factorial(wins) * math.factorial(losses))
    out = [norm * ((1 - p) ** losses) * (p ** wins) for p in x]
    plt.plot(x, out)