# Author: Manas Bhatt
# Contact: manas.bh4tt@gmail.com

# Option and Greek calculation using black scholes formula
# https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model

from scipy import stats
from numpy import sqrt, log, exp, pi

"""
N = scipy.stats.norm.cdf
d1 = (log(S/K) + (r+sigma**2/2)*t) / (sigma*sqrt(t))
d2 = d1 - sigma * sqrt(t)
"""
def helloWorld():
    return "hello world"

def d1d2(sigma, S, K, r, T):
    d1 = (1 / (sigma * sqrt(T))) * (log(S/K) + (r + sigma**2/2)* T)
    d2 = d1 - sigma * sqrt(T)
    return d1, d2

#calculate option price based on black scholes formula
def price(opt, S, K, r, t, sigma, div = 0):
    """
    opt : call/put
    S   : underlying spot price
    K   : Option contract strike
    t   : time to maturity in days
    r   : Current implied vol
    sigma: volatility of underlying asset
    div : dividend rate 
    """
    if opt == 'c':
        return priceCall(S, K, r - div, t, sigma)
    elif opt == 'p':
        return pricePut(S, K, r - div, t, sigma)
    else:
        return "Please specify call or put options."

def priceCall(S, K, r, T, sigma):
    d1, d2 = d1d2(sigma, S, K, r, T)
    return stats.norm.cdf(d1) * S - stats.norm.cdf(d2) * K * exp(-r * T)

def pricePut(S, K, r, T, sigma):
    return K * exp(-r * T) + priceCall(S, K, r, T, sigma) - S

def impliedVol(opt, S, K, C, r, T, div = 0):
    """
    opt : call/put
    S   : underlying spot price
    K   : Option contract strike
    C   : Option contract price
    t   : time to maturity in days
    r   : Current implied vol
    sigma: volatility of underlying asset
    div : dividend rate 
    """
    #Tolerances 1bp
    tol = 1e-4
    epsilon = 1

    #stopping criteria
    count = 0
    maxIter = 1000

    #initial guess
    vol = 0.5
    while epsilon > tol:
        count += 1
        if count > maxIter:
            return 'Max loops reached, no solution'
        
        origVol = vol
        
        diffPrice = (priceCall(S, K, r, T, vol) - C ) if (opt == 'c') else (pricePut(S, K, r, T, vol) - C )
        d1, d2 = d1d2(vol, S, K, r, T)
        
        vega = S * stats.norm.pdf(d1) * sqrt(T)
        if (vega == 0.0):
            return 'Calculation Error : Vega is Zero'
        vol =  - diffPrice / vega + vol

        epsilon = abs(vol - origVol)/origVol
        
    return vol

#calculate option greeks based on black scholes formula
def getGreeks(optType, S, K, r, T, sigma, div = 0, cntSize = 100):
    """
    optType : call/put
    S   : underlying spot price
    K   : Option contract strike
    t   : time to maturity in days
    r   : risk free rate
    sigma: volatility of underlying asset
    div : dividend rate
    cntSize : To normalize theta and vega as per the trading platforms
    """
    d1, d2 = d1d2(sigma, S, K, r - div, T)
    
    return  delta(d1, optType), gamma(d2, S, K, sigma, r, T),(vega(d1, S, T) / 100), (theta(optType, d1, d2, S, K, sigma, r - div, T) * cntSize / 365), rho(optType, d2, K, sigma, r, T)

def delta(d1, optType):
    optDelta = stats.norm.cdf(d1)
    
    if optType == 'p':
       optDelta = optDelta - 1
       
    return optDelta

def gamma(d2, S, K, sigma, r, T):
    return (K * exp( -r * T) * (stats.norm.pdf(d2) / (S**2 * sigma * sqrt(T) )))
             
#theta in unit year,
#for trading platform representation multiply by contract size and divide by 365
def theta(cntType, d1, d2, S, K, sigma, r, T):
    if cntType == 'c':
        theta = - S * sigma * stats.norm.pdf(d1) / (2* sqrt(T)) - r * K * exp( -r * T) * stats.norm.cdf(d2)

    if cntType == 'p':
        theta = - S * sigma * stats.norm.pdf(-d1) / (2* sqrt(T)) + r * K * exp( -r * T) * stats.norm.cdf(-d2)

    return theta

#vega in vol point
#for trading platform representation multiply by 100
def vega(d1, S, T):
    return S * stats.norm.pdf(d1) * sqrt(T)

def rho(cntType, d2, K, sigma, r, T):
    if cntType == 'c':
        theta = K * T * exp( -r * T) * stats.norm.cdf(d2)
    elif cntType == 'p':
        theta = - K * T * exp( -r * T) * stats.norm.cdf(-d2)

    return theta



    
    
