import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
import requests


def fetch_profile(symbol, api_key = "e486d28474b4514036542a26b3c88b9d"):
    URL = "https://financialmodelingprep.com/api/v3/profile/{}?apikey={}".format(symbol, api_key)
    r = requests.get(URL)
    profile = r.json()
    profile_df = pd.DataFrame(profile)
    return profile_df

def fetch_fundementals(symbol, api_key = "THTFAMKBYWWOSDJO"):
    URL = "https://www.alphavantage.co/query?function=OVERVIEW&symbol={}&apikey={}".format(symbol, api_key)
    r = requests.get(URL)
    r = r.json()
    df = pd.DataFrame(r, index=[0])
    return df

def fetch_stock_list(api_key = "e486d28474b4514036542a26b3c88b9d"):
    URL = "https://financialmodelingprep.com/api/v3/stock/list?apikey={}".format(api_key)
    r = requests.get(URL)
    profile = r.json()
    df = pd.DataFrame(profile)
    return df