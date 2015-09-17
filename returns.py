import numpy as np
import matplotlib.pyplot as plt
import math

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

def Percent(p, bet_percent, years, cons):
    ''' This is a simulation of what our returns would look like if we bet on all
    games each week, we bet evenly on all games, our returns are independent, and 
    we follow a strategy such that we bet a percent of our total investment each 
    week.  The histogram plot is of the log returns.  Values are final money for 
    an investment of 1'''    
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