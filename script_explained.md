# Explain script

Three modules are used:
* scraping.py
* plot_module.py
* utils.py


## Scraping module
```
                      scraping.py
                          |
                          |
             ___________________________
            |                           |
  scraping_panerai_2023          read_panerai2021
```

* `scraping_panerai_2023`\
Uses the framework `BeautifulSoup` to scrap data from the France, USA, Japan and UK Panerai website. After inspecting the website of each collection, I figured out that prices, references and collections are available into the `base-checkout-addtocart base-component` class and under the button attributs called `data-tracking-products`. Then I used a loop and key/value references to retrieve Panerai 2023 data. 


* `read_panerai2021`\
Simple function to read xlsx Panerai 2021 data. Notice that it computes also the excluded tax prices.

## Plot module

```
                      plot_module.py
                            |
                            |
             _____________________________
            |               |             |
     plot_piecharts    plot_boxplot    plot_hist
```

* `plot_piecharts`\
Uses the framework `Pandas` to display the number of product by collection. It display the percentage of each collection and the number of product.


* `plot_boxplot`\
Uses the framework `Seaborn` to make boxplots of all four market prices. The prices are converted in euros with the exange rate of the associated month/year.

* `plot_hist`\
Uses the framework `Pandas` to plot histograms of prices (excl.Tax) for each collection for a country `country` between 2021 and 2023. Subplots are set to handle multiple `x_lim` and legends.


## Utils module 
```
                          utils.py
                              |
                              |
             _________________________________
            |                 |               |
     change_currency     set_to_euros   compute_exclTax_prices
```
* `change_currency`\
Module used to create a dictionnary containing the changing rate "currency to euros" (handle USD, GBP and JPY currencies)

* `set_to_euros`\
Using a mask to convert all prices in euros regarding the currency. Return a DataFrame with the prices in euros.

* `compute_exclTax_prices`\
Add a price_exclTax column to a dataset regarding the country (20% VAT for France and UK and 10% VAT for Japan)