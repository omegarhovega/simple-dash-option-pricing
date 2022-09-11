import scipy.stats
from numpy import sqrt, log, exp, maximum, errstate
import pandas as pd

# Black Scholes valuation ########################################################

errstate(divide='ignore') # included to address division by 0 when sigma is 0, option value defaults to 0

def div(n,d):
    try:
        return n/d
    except ZeroDivisionError:
        return 0


def bs_price(c_p, S, K, r, t, q, sigma):
    """
    c_p: 'c': Call, 'p': put
    S: current price of underlying
    K: strike price
    r: interest rate
    t: time to maturity (days/365)
    q: dividends
    sigma: volatility underlying
    """
    N = scipy.stats.norm.cdf
    d1 = div((log(div(S,K)) + (r-q+sigma**2/2)*t), (sigma*sqrt(t))) 
    d2 = d1 - sigma * sqrt(t)
    if c_p == 'c':
        return N(d1) * S * exp(-q*t) - N(d2) * K * exp(-r*t)
    elif c_p == 'p':
        return N(-d2) * K * exp(-r*t) - N(-d1) * S * exp(-q*t)
    else:
        return "Please specify call or put options."

# Create Pandas Data Frame with Option Prices ####################################

def create_data(min_range, max_range, c_p, K, r, T, q, sigma):
    rows = []
    step = maximum(int(K/20),1) # disable if you want prices at round numbers or go to 1 (very time consuming as many data points to be produced for larger numbers)
    for i in range(min_range, max_range, step):
      x = i
      y = bs_price(c_p, i, K, r, T, q, sigma)
      rows.append([x, y])
    
    df = pd.DataFrame(rows, columns=['Price Underlying', 'Option Price'])

    return df
