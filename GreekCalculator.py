import xlwings as xw
import datetime as dt
import blackscholes as bs
import Tradier as TAPI
import pandas as pd

from datetime import datetime

today = dt.date.today()

#test in python before exposing in excel
def main():
    #expiries = optionExpiries("MSFT")
    #diff = map(str, map(maturity, expiries))
    #print(list(diff))
    wb = xw.Book.caller()
    sheet = wb.sheets[0]
    if sheet["A1"].value == "Hello xlwings!":
        sheet["A1"].value = "Bye xlwings!"
    else:
        sheet["A1"].value = "Hello xlwings!"


@xw.func
def hello(name):
    return f"Hello {name}!"

@xw.func
def helloString(str):
    return "hello " + str

@xw.func
def optionExpiries(Authcode, tickerStr, url):
     return TAPI.optionExpiries(Authcode, tickerStr, url)
     
@xw.func
def optionChainFile(filePath, optExpiry, symbol, AuthToken, url):
    return TAPI.optionChainFile(filePath, optExpiry, symbol, AuthToken, url)

@xw.func
def optionChain( optExpiry, symbol, AuthToken, url):
    return TAPI.optionChain(optExpiry, symbol, AuthToken, url)

@xw.func
def bsPrice(opt, S, K, r, t, sigma, div = 0):
    return bs.price(opt, S, K, r, t, sigma, div)

@xw.func
def bsGreeks(optType, S, K, r, T, sigma, div = 0, cntSize = 100):
    return bs.getGreeks(optType, S, K, r, T, sigma, div, cntSize)

@xw.func
def maturity(expiry):
    return expiry - today

@xw.func
def impliedVol(opt, S, K, C, r, T, div = 0):
    return bs.impliedVol(opt, S, K, C, r, T, div)

@xw.func
def spotPrice(Authcode, symbol, url):
    return TAPI.spotPrice(Authcode, symbol, url)

@xw.func
@xw.arg('strikes', doc="Array of Strikes")
@xw.arg('optTypes', doc="Array of option Types ie c or p")
@xw.ret(index=False, expand='table')
def optionChainGreeks(spot, strikes, optTypes, cntPrices, r, T , div, cntSize = 100):
    """
    print(len(strikes))
    print(len(optTypes))
    print(len(cntPrices))
    """
    if (len(strikes) != len(optTypes) or len(optTypes) != len(cntPrices)):
        return "Please enter same lenght array for Stikes, Option Types and Option Prices"

    sigmas = []
    #calculate implied vols for all the options
    for (K, opt, C) in zip(strikes, optTypes, cntPrices):
        sigmas.append(bs.impliedVol(opt, spot, K, C, r, T, div))

    #print(sigmas)
    prices = []
    deltas = []
    gammas = []
    vegas  = []
    thetas  = []
    rhos = []
    retDic = { }
    #calculate prices for all the options
    for (K, opt, sigma) in zip(strikes, optTypes, sigmas):
        bsprice = 0
        delta = 0
        gamma = 0
        vega = 0
        theta = 0
        rho = 0
        
        if (isinstance(sigma, (int, float))):
            bsprice = bs.price(opt, spot, K, r, T, sigma, div)
            (delta, gamma, vega, theta, rho) = bs.getGreeks(opt, spot, K, r, T, sigma, div, cntSize) #if opt == 'c' else [bs.getGreeks(opt, spot, K, r, T, sigma, div, cntSize)].reverse()

        prices.append(bsprice)
        deltas.append(delta)
        gammas.append(gamma)
        vegas.append(vega)
        thetas.append(theta)
        rhos.append(rho)
        #greeks.append(bsgreeks)
        """
        if K in retDic:
            if opt == 'p':
               retDic[K] = retDic[K].append([bsgreeks, sigma, bsprice, retDic[K]])
            else:
               retDic[K] = retDic[K].append([retDic[K], bsprice, sigma, bsgreeks]) 
        else:
            if opt == 'p':
               retDic[K] = [bsgreeks, sigma, bsprice, K]
            #retDic[K] = [bsgreeks, bsprice]
            else:
               retDic[K] = [K, bsprice, sigma, bsgreeks]
        """
        #retData.append(bsprice)
        
    #xw.Range('greeksPosition').value = "Implied Vol calculated"
    """          
    print(greeks)
    print(len(prices))
    print(len(optTypes))
    print(len(sigmas))
    print(len(deltas))
    print(len(gammas))
    print(len(vegas))
    print(len(thetas))
    print(len(rhos))
    """
    
    
    #return str(len(strikes)) + ' lines written ' + datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    retData = pd.DataFrame({ 'Option Price' : prices,
                             'Option Type'  : optTypes,
                             'Implied Vol'  : sigmas,
                             'Delta'        : deltas,
                             'Gamma'        : gammas,
                             'Vega'         : vegas,
                             'Theta'        : thetas,
                             'Rho'          : rhos
                           })
    print(retData)
    return retData
    #return prices, optTypes, sigmas, deltas, gammas, vegas, thetas, rhos


#if __name__ == "__main__":
#    xw.Book("myproject.xlsm").set_mock_caller()
#    main()
