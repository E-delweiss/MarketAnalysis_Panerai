import pandas as pd
import numpy as np
from datetime import datetime

from forex_python.converter import get_rate


def change_currency(year:int, month:int, day:int) -> dict:
    """
    Get the exange rate 'currency to EUR' at a specific date.
    Using the forex_python module which get its rate from the 
    European Central Bank.

    Args:
        year (int) : year of exange rate with YYYY format
        month (int) : month of exange rate with mm format
        day (int) : day of exange rate with dd format

    Returns:
        dict: currency to EUR rates on YYYY:mm:dd
    """
    exchanger = {"change_USD":[], "change_GBP":[], "change_JPY":[]}
    t = datetime(year, month, day)
    exchanger['change_USD'].append(get_rate("USD", "EUR", t))
    exchanger['change_GBP'].append(get_rate("GBP", "EUR", t))
    exchanger['change_JPY'].append(get_rate("JPY", "EUR", t))
    exchanger = {key:exchanger[key] for key,v in exchanger.items()}
    return exchanger

def set_to_euros(df:pd.DataFrame, exchanger:dict) -> pd.DataFrame:
    """
    Set prices to euros regarding exange rates of the respective year.

    Args:
        df (pd.DataFrame): Panerai data
        exchanger (dict): dict of currency to EUR rates

    Returns:
        pd.DataFrame: Panerai data with prices in EUR
    """
    mask_JPN = df['country'] == 'Japan'
    mask_USA = df['country'] == 'USA'
    mask_UK = df['country'] == 'UK'
    df.loc[mask_JPN, 'price_exclTax'] *= exchanger['change_JPY']
    df.loc[mask_USA, 'price_exclTax'] *= exchanger['change_USD']
    df.loc[mask_UK, 'price_exclTax'] *= exchanger['change_GBP']
    return df


def compute_exclTax_prices(df:pd.DataFrame) -> pd.DataFrame:
    """
    Add excluded tax prices to Panerai data.
    France and UK have a 20% VAT and Japan has a 10% VAT.

    Args:
        df (pd.DataFrame): Panerai data

    Returns:
        pd.DataFrame: Panera data with excluded tax prices.
    """
    conditions = [
        (df['country'] == 'France'),
        (df['country'] == 'UK'),
        (df['country'] == 'Japan'),
        (df['country'] == 'USA')]
    choices = [0.2, 0.2, 0.1, 0]
    df['sales_tax'] = np.select(conditions, choices, default=0)
    df['price_exclTax'] = df['price'] * (1-df['sales_tax'])

    return df