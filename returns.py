import numpy as np
import matplotlib.pyplot as plt
import math
from numpy.random import normal
from scipy.special import betainc
import random as rand

def returnsFromData(results, bet_percent, cons):
    '''Returns the final amount returned basaed on a given betting strategy.  
    Input is a list of dictionaries, float, and a boolean'''
    bet = 1
    win_lst = []
    loss_lst = []    
    for week in results:
        # If not constant betting strategy, use 'smartP'
        if not cons:
            bet_percent = betPercent(sum(win_lst), sum(loss_lst), bet_percent)
        win_lst.append(week['wins'])
        loss_lst.append(week['losses'])
        bet += bet_percent * bet * (win_lst[-1] * 10/11.0 - loss_lst[-1]) / \
            (win_lst[-1] + loss_lst[-1])
    return bet

def Percent(p, bet_percent, years, cons, output, simulations):
    ''' This is a simulation of what our returns would look like if we bet on all
    games each week, we bet evenly on all games, our returns are independent, and 
    we follow a strategy such that we bet a percent of our total investment each 
    week.  The histogram plot is of the log returns.  Values are final money for 
    an investment of 1.  Output is a boolean that should be set to false, so 
    that futureReturns can be used instead'''    
    # p = Success rate
    # bet_percent = amount of money to bet each week as a percent of total.  
    # number of simulations 
    # cons is a boolean that states if the betting percent is constant
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
    if not output:
        return final_payoff
    # plotting the log of the payoff because it is gaussian
    plt.hist(np.log(final_payoff), int(simulations ** (1 / 3.0)))
    print '%1 worst', final_payoff[simulations / 100], 'mean', final_payoff.mean(), 'std', final_payoff.std()
    
def betPercent(wins, losses, betting_percent):
    '''Function used to optimize the betting strategy given the current
    estimates of p.  No theoretical motivation for this function besides a 
    penalty for large uncertainties'''
    total = float(wins + losses)
    if total == 0:
        return betting_percent
    pest = wins / total
    # variance of a binomial distribution
    error = pest * (1 - pest) / (total ** .5)
    if error == 0:
        if wins == 0:
            pest_err = 1 / (total + 1.0)
        elif losses == 0:
            pest_err = wins / (total + 1.0)
        error = pest_err * (1 - pest_err) / (total ** .5)
    out = (pest - 11 / 21.0) / (11 * 21.0) / error ** 2
    # maximum amount bet
    sigmoid_scale = ((pest + error ** .5) - 11 / 21.0)
    return logistic(out) * sigmoid_scale

def logistic(x):
    '''Logistic function'''
    return 1/(1 + math.exp(-x))

def pEstGraph(wins, losses):
    '''Estimates the distribution of p given a number of wins and losses.  
    This is correct up to a normalization constant'''
    x = np.linspace(.3, .8, 1000)
    norm = math.factorial(wins + losses) / (math.factorial(wins) * math.factorial(losses))
    out = [norm * ((1 - p) ** losses) * (p ** wins) for p in x]
    plt.xlabel('probability of success')
    plt.ylabel('relative probability of p being this value')
    plt.title('Estimation of p based on results')
    plt.plot(x, out)
    plt.show()

def randP(wins, losses, size):
    '''This function generates random values of p according to pdf of 
    the MLE function. Size is the number of p values generated'''
    x = np.linspace(0, 1, 1000)
    # The integral of the pdf function from 0 to p is simply the incomplete beta
    # function of wins+1, losses+1, p
    cdf = [betainc(wins+1, losses+1, p) for p in x]
    #plt.plot(x, cdf)
    convert = {}
    # create a dict so that we can invert this cdf
    for elem in range(len(x)):
        convert[x[elem]] = cdf[elem]
    lst = []
    for elem in range(size):
        val = rand.random()
        # finds the closest value to approximate an inversion function
        key, value = min(convert.items(), key=lambda (_, v): abs(v - val))
        lst.append(key)
    return lst

def futureReturns(wins, losses, bet_percent, cons):
    '''gives a full estimation of the likely returns given some data.  Assumes
    no change in week-week p.  This should be the function to use for simulating
    returns.  I believe we should set cons to false.'''
    # Generates p vals according to the MLE pdf
    pvals = randP(wins, losses, 10000)
    returns = []
    # for each of the random p vals generated, we run a simulation
    for elem in pvals:
        returns.append(Percent(elem, bet_percent, 1, cons, False, 10))
    # flatten the list of lists to a single list
    returns = [item for sublist in returns for item in sublist]
    returns.sort()
    return returns



