# Author: Manas Bhatt
# Contact: manas.bh4tt@gmail.com
# Date:May 2022

#extract option expiries, option chains and price using tradier API
#https://documentation.tradier.com/index.html
import requests
import json

from datetime import datetime

sandboxurl = "https://sandbox.tradier.com/v1/"
requesturl = "https://api.tradier.com/v1/"
streamurl  = "https://stream.tradier.com/v1/"


"""
#response = requests.get('https://sandbox.tradier.com/v1/markets/options/expirations',
#    params={'symbol': 'VXX', 'includeAllRoots': 'true', 'strikes': 'true'},
#    headers={'Authorization': 'Bearer LXVkmzoytEbdiNQc6gcmOkF1rMxH', 'Accept': 'application/json'}
#)

response = requests.get('https://sandbox.tradier.com/v1/markets/options/expirations',
    params={'symbol': 'SPX', 'includeAllRoots': 'true', 'strikes': 'true'},
    headers={'Authorization': 'Bearer LXVkmzoytEbdiNQc6gcmOkF1rMxH', 'Accept': 'application/json'}
)
json_response = response.json()
print(response.status_code)
print(json_response)

response.close()

response = requests.get('https://sandbox.tradier.com/v1/markets/options/chains',
                        params={'symbol': 'SPX', 'expiration': '2022-05-11', 'greeks': 'false'},
                        headers={'Authorization': 'Bearer LXVkmzoytEbdiNQc6gcmOkF1rMxH', 'Accept': 'application/json'}
)

json_response = response.json()
print(response.status_code)
print(json_response)

response.close()
"""

def optionChain(optExpiry, symbol = 'SPX', AuthToken = 'LXVkmzoytEbdiNQc6gcmOkF1rMxH', url = sandboxurl):
    getUrl = url + 'markets/options/chains'
    #print(url)
    header = {
        'Authorization' : 'Bearer ' + AuthToken,
        'Accept' : 'application/json'
        }
    #print(header)
    param = {
        'symbol' : symbol,
        'expiration': optExpiry,
        'greeks': 'false'
        }
    #print(param)
    settings = {
        'params' : param,
        'headers' : header
        }
    #print(settings)
    response = requests.get(getUrl, **settings)
    json_response = response.json()

    #options = json_response['options']
    #for i in options['option']:
    #    print(i)
    #response.close()
    return json_response

def optionChainFile(filePath, optExpiry, symbol = 'SPX', AuthToken = 'LXVkmzoytEbdiNQc6gcmOkF1rMxH', url = sandboxurl):
    getUrl = url + 'markets/options/chains'
    #print(url)
    header = {
        'Authorization' : 'Bearer ' + AuthToken,
        'Accept' : 'application/json'
        }
    #print(header)
    param = {
        'symbol' : symbol,
        'expiration': optExpiry,
        'greeks': 'false'
        }
    #print(param)
    settings = {
        'params' : param,
        'headers' : header
        }
    #print(settings)
    response = requests.get(getUrl, **settings)
    json_response = response.json()

    with open(filePath + 'data.json', 'w', encoding='utf-8') as f:
        json.dump(json_response, f, ensure_ascii=False, indent=4)
        
    response.close()

    return str(len(json_response['options']['option'])) + ' lines written ' + datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

def optionExpiries(AuthToken = 'LXVkmzoytEbdiNQc6gcmOkF1rMxH', symbol = 'SPX', url = sandboxurl):
    getUrl = url + 'markets/options/expirations'
    #print(url)
    header = {
        'Authorization' : 'Bearer ' + AuthToken,
        'Accept' : 'application/json'
        }
    #print(header)
    param = {
        'symbol' : symbol,
        'includeAllRoots': 'true',
        'strikes': 'false'
        }
    #print(param)
    settings = {
        'params' : param,
        'headers' : header
        }
    #print(settings)
    response = requests.get(getUrl, **settings)
    json_response = response.json()

    dates = json_response['expirations']
    
    #for i in dates['date']:
    #    print(i)
    #print(response.status_code)
    #print(json_response)

    response.close()
    return dates['date']

def spotPrice(AuthToken = 'LXVkmzoytEbdiNQc6gcmOkF1rMxH', symbol = 'SPX', url = sandboxurl):
    getUrl = url + 'markets/quotes'
    #print(url)
    header = {
        'Authorization' : 'Bearer ' + AuthToken,
        'Accept' : 'application/json'
        }
    #print(header)
    param = {
        'symbols' : symbol,
        'greeks': 'false'
        }
    #print(param)
    settings = {
        'params' : param,
        'headers' : header
        }
    #print(settings)
    response = requests.get(getUrl, **settings)
    json_response = response.json()
    #print(json_response)

    last = json_response['quotes']['quote']['last']

    response.close()

    return last

    
    
