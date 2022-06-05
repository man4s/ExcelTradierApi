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

    #save the file to be reused
    #pd.save_csv(file)

    return df
