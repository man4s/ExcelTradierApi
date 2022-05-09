# ExcelTradierApi
Excel Tradier API sheet

Connects to tradier server using python function (excel python integration using xlwings addin) and retrieves option expiries for a given ticker
On selecting a specific expiry, retrieves option chain from Tradier.
Using black-scholes model (implemented in python), calculates greeks for all the options
