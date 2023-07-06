import pandas as pd
import requests
import numpy as np
import ast

from bs4 import BeautifulSoup

import utils

def scraping_panerai_2023() -> pd.DataFrame:
    """
    Get infos from France, USA, Japan and UK Panerai websites.
    Retrive collection, price, reference and country.
    The data are then formatted to fit with the 2021 data format.
    Compute and add excluded tax prices.

    Returns:
        pd.DataFrame: 2023 scrapped Panerai data.
    """
    websites = {
        "France" : "https://www.panerai.com/fr/fr/",
        "USA" : "https://www.panerai.com/us/en/",
        "Japan" : "https://www.panerai.com/jp/ja/",
        "UK" : "https://www.panerai.com/gb/en/"
        }

    head = ["collection", "price", "reference", "country"]
    collections = ["submersible", "luminor", "luminor-due", "radiomir"]
    watch_dict = {new_list: [] for new_list in head}

    ### Loop over websites
    for country in websites.keys():
        ### Loop over Panerai collections
        for collection in collections:
            website_country = websites.get(country)
            url = website_country + "collections/watch-collection/" + collection + ".html"
            
            # Request url and get html code
            page = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
            soup = BeautifulSoup(page.content, "html.parser")

            # Find specific class where watch infos are stored
            elements = soup.find_all("div", class_={"base-checkout-addtocart base-component"})

            ### Loop over elements stored in 'base-checkout-addtocart base-component' class
            for element in elements:
                ### All watch attributs are contained in the subclass 'button'
                watch = ast.literal_eval(element.find("button").attrs['data-tracking-products'])[0]
                watch_dict["collection"].append(watch.get("collection"))
                watch_dict["price"].append(watch.get("price"))
                watch_dict["reference"].append(watch.get("ref"))
                watch_dict["country"].append(country)

    data = pd.DataFrame(watch_dict)
    data['collection'][data['collection'] == 'Luminor Due'] = "Luminor-Due"
    data['price'].replace('N/A', np.nan, inplace=True)
    data.dropna(subset = ['price'], inplace=True) #droping watch without prices
    data['price'] = data['price'].astype('float') #convert text values to numerical

    data = utils.compute_exclTax_prices(data) #add excluded tax prices

    return data


def read_panerai_2021() -> pd.DataFrame:
    """
    Read .xlsx Panerai 2021 data file.
    Compute and add excluded tax prices.

    Returns:
        pd.DataFrame: 2021 Panerai data.
    """
    data = pd.read_excel("PANERAI_DATA_122021.xlsx")
    data = utils.compute_exclTax_prices(data)

    return data