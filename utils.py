# Import libraries
# yfinance offers a reliable, threaded, and Pythonic way to download historical market data from Yahoo! finance
# Please check out its official doc for details: https://pypi.org/project/yfinance/

import yfinance as yf
import pandas as pd

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
    dataframe.to_csv(outname)
    
if __name__ == '__main__':
    symbol = 'ADANIPORTS.NS'
    df = read_single_stock(symbol)
    write_csv(df)