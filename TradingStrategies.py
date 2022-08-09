# Author: Manas Bhatt
# Contact: manas.bh4tt@gmail.com
# Date : Jun 2022

#functions to implement trading strategies like butterfly
import datetime as dt
import blackscholes as bs
import pandas as pd
import numpy as np

def butterfly(deltas, #3 deltas to be provided
              lots, #3 lots to be provided
              file):
    if len(deltas) != len(lots) or len(deltas) != 3:
        return f("Butterfly Strategy requires 3 deltas and 3 lots")

    #create a dataframe using csv file
    df = pd.read_csv(file)

    df.drop(['Option Type'], axis =1, inplace=True)

    #add the deltas in the frame
    df.loc[-1] = [np.NaN, np.NaN, deltas[0], np.NaN, np.NaN, np.NaN, np.NaN, np.NaN]
    df.loc[-2] = [np.NaN, np.NaN, deltas[1], np.NaN, np.NaN, np.NaN, np.NaN, np.NaN]
    df.loc[-3] = [np.NaN, np.NaN, deltas[2], np.NaN, np.NaN, np.NaN, np.NaN, np.NaN]
    #sort in ascending order
    df = df.sort_values(by="Delta")
    df = df.interpolate()
    #extract the relevant rows
    df = df[df.Delta.isin(deltas)]

    #add lots column to the fram
    df["Lots"] = lots

    df.index.name = "Leg"

    #scale the lots to one unit
    alots = [x/lots[0] for x in lots]
    
    #butterfly prices and greek in one lot
    df.loc["B/Lot"] = [ alots[0]*df.at[-1, 'Option Price'] + alots[1]*df.at[-2, 'Option Price'] + alots[2]*df.at[-3, 'Option Price'],
                        alots[0]*df.at[-1, 'Implied Vol'] + alots[1]*df.at[-2, 'Implied Vol'] + alots[2]*df.at[-3, 'Implied Vol'],
                        alots[0]*df.at[-1, 'Delta'] + alots[1]*df.at[-2, 'Delta'] + alots[2]*df.at[-3, 'Delta'],
                        alots[0]*df.at[-1, 'Gamma'] + alots[1]*df.at[-2, 'Gamma'] + alots[2]*df.at[-3, 'Gamma'],
                        alots[0]*df.at[-1, 'Vega'] + alots[1]*df.at[-2, 'Vega'] + alots[2]*df.at[-3, 'Vega'],
                        alots[0]*df.at[-1, 'Theta'] + alots[1]*df.at[-2, 'Theta'] + alots[2]*df.at[-3, 'Theta'],
                        alots[0]*df.at[-1, 'Rho'] + alots[1]*df.at[-2, 'Rho'] + alots[2]*df.at[-3, 'Rho'],
                        alots[0]*df.at[-1, 'Strikes'] + alots[1]*df.at[-2, 'Strikes'] + alots[2]*df.at[-3, 'Strikes'],
                        sum(alots) ]
    
    #create a row based on the weighted sum of lots
    df.loc["Butterfly"] = [ lots[0]*df.at[-1, 'Option Price'] + lots[1]*df.at[-2, 'Option Price'] + lots[2]*df.at[-3, 'Option Price'],
                            lots[0]*df.at[-1, 'Implied Vol'] + lots[1]*df.at[-2, 'Implied Vol'] + lots[2]*df.at[-3, 'Implied Vol'],
                            lots[0]*df.at[-1, 'Delta'] + lots[1]*df.at[-2, 'Delta'] + lots[2]*df.at[-3, 'Delta'],
                            lots[0]*df.at[-1, 'Gamma'] + lots[1]*df.at[-2, 'Gamma'] + lots[2]*df.at[-3, 'Gamma'],
                            lots[0]*df.at[-1, 'Vega'] + lots[1]*df.at[-2, 'Vega'] + lots[2]*df.at[-3, 'Vega'],
                            lots[0]*df.at[-1, 'Theta'] + lots[1]*df.at[-2, 'Theta'] + lots[2]*df.at[-3, 'Theta'],
                            lots[0]*df.at[-1, 'Rho'] + lots[1]*df.at[-2, 'Rho'] + lots[2]*df.at[-3, 'Rho'],
                            lots[0]*df.at[-1, 'Strikes'] + lots[1]*df.at[-2, 'Strikes'] + lots[2]*df.at[-3, 'Strikes'],
                            sum(lots) ]

    #save the file to be reused
    #pd.save_csv(file)

    return df

def butterflyStickyStrike(strikes, #3 strikes to be provided
                          lots, #3 lots to be provided
                          file):
    if len(strikes) != len(lots) or len(deltas) != 3:
        return f("Butterfly Strategy requires 3 deltas and 3 lots")

    #create a dataframe using csv file
    df = pd.read_csv(file)

    df.drop(['Option Type'], axis =1, inplace=True)

    #add the deltas in the frame
    df.loc[-1] = [np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, strikes[0]]
    df.loc[-2] = [np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, strikes[1]]
    df.loc[-3] = [np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, strikes[2]]
    #sort in ascending order
    df = df.sort_values(by="Strikes")
    df = df.interpolate()
    #extract the relevant rows
    df = df[df.Strikes.isin(strikes)]

    #add lots column to the fram
    df["Lots"] = lots

    df.index.name = "Leg"

    #scale the lots to one unit
    alots = [x/lots[0] for x in lots]
    
    #butterfly prices and greek in one lot
    df.loc["B/Lot"] = [ alots[0]*df.at[-1, 'Option Price'] + alots[1]*df.at[-2, 'Option Price'] + alots[2]*df.at[-3, 'Option Price'],
                        alots[0]*df.at[-1, 'Implied Vol'] + alots[1]*df.at[-2, 'Implied Vol'] + alots[2]*df.at[-3, 'Implied Vol'],
                        alots[0]*df.at[-1, 'Delta'] + alots[1]*df.at[-2, 'Delta'] + alots[2]*df.at[-3, 'Delta'],
                        alots[0]*df.at[-1, 'Gamma'] + alots[1]*df.at[-2, 'Gamma'] + alots[2]*df.at[-3, 'Gamma'],
                        alots[0]*df.at[-1, 'Vega'] + alots[1]*df.at[-2, 'Vega'] + alots[2]*df.at[-3, 'Vega'],
                        alots[0]*df.at[-1, 'Theta'] + alots[1]*df.at[-2, 'Theta'] + alots[2]*df.at[-3, 'Theta'],
                        alots[0]*df.at[-1, 'Rho'] + alots[1]*df.at[-2, 'Rho'] + alots[2]*df.at[-3, 'Rho'],
                        alots[0]*df.at[-1, 'Strikes'] + alots[1]*df.at[-2, 'Strikes'] + alots[2]*df.at[-3, 'Strikes'],
                        sum(alots) ]
    
    #create a row based on the weighted sum of lots
    df.loc["Butterfly"] = [ lots[0]*df.at[-1, 'Option Price'] + lots[1]*df.at[-2, 'Option Price'] + lots[2]*df.at[-3, 'Option Price'],
                            lots[0]*df.at[-1, 'Implied Vol'] + lots[1]*df.at[-2, 'Implied Vol'] + lots[2]*df.at[-3, 'Implied Vol'],
                            lots[0]*df.at[-1, 'Delta'] + lots[1]*df.at[-2, 'Delta'] + lots[2]*df.at[-3, 'Delta'],
                            lots[0]*df.at[-1, 'Gamma'] + lots[1]*df.at[-2, 'Gamma'] + lots[2]*df.at[-3, 'Gamma'],
                            lots[0]*df.at[-1, 'Vega'] + lots[1]*df.at[-2, 'Vega'] + lots[2]*df.at[-3, 'Vega'],
                            lots[0]*df.at[-1, 'Theta'] + lots[1]*df.at[-2, 'Theta'] + lots[2]*df.at[-3, 'Theta'],
                            lots[0]*df.at[-1, 'Rho'] + lots[1]*df.at[-2, 'Rho'] + lots[2]*df.at[-3, 'Rho'],
                            lots[0]*df.at[-1, 'Strikes'] + lots[1]*df.at[-2, 'Strikes'] + lots[2]*df.at[-3, 'Strikes'],
                            sum(lots) ]

    #save the file to be reused
    #pd.save_csv(file)

    return df

#data dict containing deltas, lots, filename
def structure(optdatas):

    df = pd.DataFrame()
    
    for optdata in optdatas:
        (deltas, lots, file) = optdata

        if len(deltas) != len(lots):
            return f("Structure requires deltas and lots of same size for a given maturity")
        
        df.append(structureImpl(deltas, lots, file), ignore_index = True)

    #summarize the data in dataframe
    return df

#combination of option type, delta and maturity
def structureImpl(deltas,
                  lots,
                  file):
    return

