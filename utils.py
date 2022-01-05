# Import libraries
# yfinance offers a reliable, threaded, and Pythonic way to download historical market data from Yahoo! finance
# Please check out its official doc for details: https://pypi.org/project/yfinance/

from numpy import empty
import yfinance as yf
import pandas as pd
import json
import os, sys
from pathlib import Path

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

def make_abspath(filename=''):
    # expanduser (if '~' in path) 
    filename = os.path.expanduser(filename)
    print('Debug - after expanduser : {}'.format(filename))

    # get absolute path
    filename = os.path.abspath(filename)
    print('Debug - after absolute path : {}'.format(filename))

    return filename

# read all stock names from excel sheet
def get_symbols(filename='', skiprows=0, usecols='', outfile=''):
    
    # convert to absolute path
    filename = make_abspath(filename=filename)

    # check if the file exists 
    # read the file with user-specified arguments
    if Path(filename).exists():
        df = pd.read_excel(filename, skiprows=skiprows, usecols=usecols)
    else:
        sys.exit('File {} does not exist!'.format(filename))
    
    # print the pandas dataframe
    print(df.head())

    # drop all columns except Symbol
    df = df[['Symbol']]
    print(df.head())
    
    write_csv(df, outname=outfile)

# remove symbols that are not listed on NS
def remove_symbols(filename='', outfile=''):
    
    # convert to absolute path
    df = pd.read_csv(filename)
    df = df[['Symbol']]
    
    # print the pandas dataframe
    non_ns = []
    for s in df['Symbol']:
        ticker = yf.Ticker(s + '.NS')
        stock = ticker.history(period='1d')
        if stock.empty:
            # print('{} not listed on NS'.format(s))
            ind = df[df['Symbol'] == s].index
            non_ns.append(ind)
    
    # drop non-ns cols
    # print(non_ns)
    for ind in non_ns:
        df.drop(ind, axis=0, inplace=True)
        
    # write as csv
    write_csv(df, outname='./data/symbols_ns.csv')


if __name__ == '__main__':
    # # read and write single stock
    # symbol = 'ADANIPORTS'
    # df = read_single_stock(symbol + '.NS')
    # write_csv(df, outname='./data/sample_stock.csv')

    # # read and write multiple stocks
    # symbol = ['ADANIPORTS', 'ALKEM', 'ASHOKA',
    #         'ASHOKLEY', 'ASIANPAINT', 'BAJFINANCE',
    #         'BRITANNIA', 'CAMS', 'COALINDIA']
    # for i in range(len(symbol)):
    #     symbol[i] +='.NS'

    # read_multiple_stocks(symbol, period='1y', save=True, outdir='./data/')


    # # get all symbols
    # filename = '~/Downloads/holdings-SY9025.xlsx'
    # skiprows = 22
    # usecols = 'B:M'
    # get_symbols(filename=filename, skiprows=skiprows, usecols=usecols, outfile='./data/symbols.csv')

    # remove non-NS symbols
    remove_symbols('./data/symbols.csv')


