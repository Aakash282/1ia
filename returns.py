import numpy as np
import matplotlib.pyplot as plt

''' This is a simulation of what our returns would look like if we bet on all
games each week, we bet evenly on all games, our returns are independent, and 
we follow a strategy such that we bet a percent of our total investment each 
week.  The histogram plot is of the log returns.  Values are final money for 
an investment of 1'''

# Success rate
p = 0.6
# amount of money to bet each week as a percent of total.  
bet_percent = 0.4
# number of simulations 
simulations = 10000
# number of years we run the betting through
years = 1
payoff = []
final_payoff = np.array([])
count = 0
for i in range(simulations):
    bet = 1
    for i in range(17*years):
        wins = np.random.binomial(15, p)
        losses = 15 - wins
        bet += bet_percent * bet * (wins * 10/11.0 - losses) / 15.0
        if bet <= 0:
            count += 1
            print 'Ran out of money %i times!' %count
        payoff.append(bet)
    final_payoff = np.append(final_payoff, payoff[-1])
# plotting the log of the payoff
plt.hist(np.log(final_payoff))
print 'min', final_payoff.min(), 'mean', final_payoff.mean(), 'std', final_payoff.std()