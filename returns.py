import numpy as np
import matplotlib.pyplot as plt
import math
''' This is a simulation of what our returns would look like if we bet on all
games each week, we bet evenly on all games, our returns are independent, and 
we follow a strategy such that we bet a percent of our total investment each 
week.  The histogram plot is of the log returns.  Values are final money for 
an investment of 1'''

def Percent(p, bet_percent, years, cons):
    # p = Success rate
    # bet_percent = amount of money to bet each week as a percent of total.  
    # number of simulations 
    # cons is a boolean that states if the betting percent is constant
    simulations = 100000
    payoff = []
    final_payoff = np.array([])
    count = 0
    for i in range(simulations):
        bet = 1
        win_list = []
        loss_list = []
        for i in range(17 * years):
            if not cons:
                bet_percent = betPercent(sum(win_list), sum(loss_list), bet_percent)
            wins = np.random.binomial(15, p)
            losses = 15 - wins
            win_list.append(wins)
            loss_list.append(losses)
            bet += bet_percent * bet * (wins * 10/11.0 - losses) / 15.0
            if bet <= 0:
                count += 1
                print 'Ran out of money %i times!' %count
            payoff.append(bet)
        final_payoff = np.append(final_payoff, payoff[-1])
    final_payoff.sort()    
    # plotting the log of the payoff because it is gaussian
    plt.hist(np.log(final_payoff), int(simulations ** (1 / 3.0)))
    print '%1 worst', final_payoff[simulations / 100], 'mean', final_payoff.mean(), 'std', final_payoff.std()
    
def betPercent(wins, losses, betting_percent):
    total = float(wins + losses)
    if total == 0:
        return betting_percent
    pest = wins / total
    error = pest * (1 - pest) / (total ** .5)
    if error == 0:
        error = .1 / (total ** .5)
    out = (pest - 11 / 21.0) / (11 * 21.0) / error ** 2
    sigmoid_scale = pest ** .5 - error
    return logistic(out) * sigmoid_scale

def logistic(x):
    return 1/(1 + math.exp(-x))

def pEstGraph(wins, losses):
    '''Estimates the distribution of p given a number of wins and losses.  
    This is correct up to a normalization constant'''
    x = np.linspace(0, 1, 100)
    norm = math.factorial(wins + losses + 1) / (math.factorial(wins) * math.factorial(losses))
    out = [norm * ((1 - p) ** losses) * (p ** wins) for p in x]
    plt.plot(x, out)