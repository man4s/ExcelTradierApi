# ExcelTradierApi
Excel Tradier API sheet

First Release
Connects to tradier server using python function (excel python integration using xlwings addin) and retrieves option expiries for a given ticker
On selecting a specific expiry, retrieves option chain from Tradier.
Using black-scholes model (implemented in python), calculates greeks for all the options

SCOPE 1 - Option Trading Platform (Excel)
Items to deliver
  Implied Forward calculation
  Margin calculation (spot decreases by 20% scenario)
  Setup butterfly structure for given delta
  Implement trade execution via Tradier API
  Implement implied vol to maturity chart 
  Implement eod feature in the sheet to save
        EOD vols
        Trading position
        Historical option prices for various butterflies for a given maturity
  Calculation mean reversion, std dev and zscore for a given butterfly using SMA
