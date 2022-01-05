# Import libraries
# yfinance offers a reliable, threaded, and Pythonic way to download historical market data from Yahoo! finance
# Please check out its official doc for details: https://pypi.org/project/yfinance/

import yfinance as yf
import pandas as pd
import json

# Load historical data in the past 10 years
def read_single_stock(symbol='RELIANCE.NS', period='1y'):
    '''
    Read a single stock history data for specified period as dataframe
    
    Input parameters
    ----------------
    symbol : str, symbol for stock
    period : str, time period ('1d', '1m', '1y'... )

    Output
    ------
    stock dataframe  
    '''
    symbol
    ticker = yf.Ticker(symbol)
    stock = ticker.history(period=period)
    return stock

def write_csv(dataframe, outname='./data/sample_stock.csv'):
    '''
    Write a dataframe as csv
    
    Input parameters
    ----------------
    dataframe : dataframe to write
    outname : file to save the data
    
    Output
    ------
    None
    '''
    print('Write {}'.format(outname))
    dataframe.to_csv(outname)

def write_json(in_dict, outname='./data/multiple_stocks.json'):
    '''
    Write a dict as json
    
    Input parameters
    ----------------
    in_dict : dictionary to write
    outname : file to save the data
    
    Output
    ------
    None
    '''
    print('Write {}'.format(outname))
    with open(outname, 'w') as outfile:
        json.dump(in_dict, outfile)

    
def read_multiple_stocks(symbol=['RELIANCE.NS'], period='1y', save=True, outdir='./data/'):
    '''
    Read multiple stocks history data for specified period as dataframe
    and save it (optional)
    
    Input parameters
    ----------------
    symbol : str, symbol for stock
    period : str, time period ('1d', '1m', '1y'... )
    save   : bool, write the df as csv or not
    outdir : directory to save the data

    Output
    ------
    write individual stock as dataframes (csv)
    return multiple stocks as dict
    '''

    stock_dict = {}
    for s in symbol:
        ticker = yf.Ticker(s)
        stock = ticker.history(period=period)
        stock_dict[s] = stock

        if save:
            write_csv(stock, outname=outdir + s)

    return stock_dict

if __name__ == '__main__':
    # read and write single stock
    symbol = 'ADANIPORTS'
    df = read_single_stock(symbol + '.NS')
    write_csv(df, outname='./data/sample_stock.csv')

    # read and write multiple stocks
    symbol = ['ADANIPORTS', 'ALKEM', 'ASHOKA',
            'ASHOKLEY', 'ASIANPAINT', 'BAJFINANCE',
            'BRITANNIA', 'CAMS', 'COALINDIA']
    for i in range(len(symbol)):
        symbol[i] +='.NS'

    read_multiple_stocks(symbol, period='1y', save=True, outdir='./data/')


