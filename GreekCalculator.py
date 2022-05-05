import xlwings as xw
import pandas as pd
import yfinance as yf
import datetime as dt
import blackscholes as bs
import Tradier as TAPI

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


#if __name__ == "__main__":
#    xw.Book("myproject.xlsm").set_mock_caller()
#    main()
