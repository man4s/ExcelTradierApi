import xlwings as xw
import datetime as dt
import blackscholes as bs
import Tradier as TAPI
import pandas as pd
import TradingStrategies as ts

from datetime import datetime

today = dt.date.today()

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
@xw.ret(expand='table')
def createButterfly(optType,
                    maturity,
                    sym,
                    deltas,
                    lots,
                    filepath):
    deltas = list(map(lambda x:x/100, deltas))
    fileName = filepath + sym + "_" + maturity + "_" + optType + ".csv"
    return ts.butterfly(deltas, lots, fileName)
                    
@xw.func
@xw.arg('strikes', doc="Array of Strikes")
@xw.arg('optTypes', doc="Array of option Types ie c or p")
@xw.ret(index=False, expand='table')
def optionChainGreeks(spot,
                      strikes,
                      optTypes,
                      cntPrices,
                      r,
                      T ,
                      div,
                      cntSize = 100,
                      filePath = '',
                      optMat = '',
                      sym=''):
    """
    returns Option Prices and greeks for a given option chain
    """

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
                             'Rho'          : rhos,
                          })
    print(retData)


    if (filePath != ''):
        retData['Strikes'] = strikes
        cleanData = retData[retData['Implied Vol'] != 'Calculation Error : Vega is Zero']
        cleanData[cleanData['Option Type'] == 'p'].to_csv(filePath + sym + '_' + optMat + '_put.csv', index=False)
        cleanData[cleanData['Option Type'] == 'c'].to_csv(filePath + sym + '_' + optMat + '_call.csv', index=False)
        retData.drop(['Strikes'], axis= 1, inplace=True)   
        
     
    return retData
    #return prices, optTypes, sigmas, deltas, gammas, vegas, thetas, rhos

@xw.func
@xw.ret(index=False, expand='table')
def optionChainScenarioGreeks(spot,
                              strikes,
                              optTypes,
                              cntPrices,
                              r,
                              T ,
                              div,
                              cntSize = 100,
                              spotDevalue = 0.2,
                              timeDecrease = 60/365):
    """
    1. calculates price and greeks due to spot decrease
    2. calculates price due to increase maturity
    """

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
    sSprices = []
    sSdeltas = []
    sSgammas = []
    sSvegas  = []
    sSthetas  = []
    sSrhos = []
    sTprices = []
    retDic = { }
    impliedFwdDic = { }
    #calculate prices for all the options
    for (K, opt, sigma) in zip(strikes, optTypes, sigmas):

        sbsprice = 0
        sdelta = 0
        sgamma = 0
        svega = 0
        stheta = 0
        srho = 0
        tbsprice = 0
        #scenario calculation
        if (isinstance(sigma, (int, float))):
            #spot up/down by spotDevalue
            dspot = spot*(1.0-spotDevalue)
            sbsprice = bs.price(opt, dspot, K, r, T, sigma, div)

            #reusing values 
            (sdelta, sgamma, svega, stheta, srho) = bs.getGreeks(opt, dspot, K, r, T, sigma, div, cntSize)
            
            #time value increase by timeIncrease
            tbsprice = bs.price(opt, spot, K, r, (T - timeDecrease) if (T - timeDecrease) > 0.0 else 0.0, sigma, div)

        sSprices.append(sbsprice)
        sSdeltas.append(sdelta)
        sSgammas.append(sgamma)
        sSvegas.append(svega)
        sSthetas.append(stheta)
        sSrhos.append(srho)
        sTprices.append(tbsprice)
        
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
        

    deValueSpot = spot*(1.0-spotDevalue)
    sixtyDaysAhead = dt.date.today() + dt.timedelta(timeDecrease*365)
    
    #return str(len(strikes)) + ' lines written ' + datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    retData = pd.DataFrame({ str(1- spotDevalue) + ' Spot Price' : sSprices,
                             'Price at ' + str(sixtyDaysAhead)   : sTprices,
                             str(1- spotDevalue) + ' Spot Delta'        : sSdeltas,
                             str(1- spotDevalue) + ' Spot Gamma'        : sSgammas,
                             str(1- spotDevalue) + ' Spot Vega'         : sSvegas,
                             str(1- spotDevalue) + ' Spot Theta'        : sSthetas,
                             str(1- spotDevalue) + ' Spot Rho'          : sSrhos     
                           })
    print(retData)
    return retData


