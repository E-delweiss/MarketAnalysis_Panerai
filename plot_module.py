import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import utils

def plot_piecharts(data:pd.DataFrame, year:int) -> None:
    """
    Plot piecharts of the collection distribution for each market.

    Args:
        data (pd.DataFrame): Pandas DataFrame containing Panerai data
        year (int): year of the data for title
    """
    def my_fmt(x):
        """ Fonction using for adding number values to percentages.
        """
        return '{:.0f}%\n({:.0f})'.format(x, size*x/100)

    palette = sns.color_palette()
    cdict = {'RADIOMIR': palette[5], 'LUMINOR': palette[4], 'SUBMERSIBLE': palette[7], "LUMINOR-DUE" : palette[6]}

    fig = plt.figure(figsize = (24, 5),  dpi=250)
    fig.suptitle(year, fontsize=30, weight="bold")

    ax1 = fig.add_subplot(1, 4, 1)
    ax2 = fig.add_subplot(1, 4, 2)
    ax3 = fig.add_subplot(1, 4, 3)
    ax4 = fig.add_subplot(1, 4, 4)

    size = len(data[data["country"]=="France"])
    colors = [cdict.get(a.upper()) for a in data[data["country"]=="France"].collection.value_counts().index]
    data[data["country"]=="France"].collection.value_counts().plot(kind="pie", autopct=my_fmt, ax=ax1, colors=colors)
    ax1.set_ylabel('');
    ax1.set_title('France', fontsize=14, fontweight='bold')

    size = len(data[data["country"]=="UK"])
    colors = [cdict.get(a.upper()) for a in data[data["country"]=="UK"].collection.value_counts().index]
    data[data["country"]=="UK"].collection.value_counts().plot(kind="pie", autopct=my_fmt, ax=ax2, colors=colors)
    ax2.set_ylabel('')
    ax2.set_title('UK', fontsize=14, fontweight='bold')

    size = len(data[data["country"]=="USA"])
    colors = [cdict.get(a.upper()) for a in data[data["country"]=="USA"].collection.value_counts().index]
    data[data["country"]=="USA"].collection.value_counts().plot(kind="pie", autopct=my_fmt, ax=ax3, colors=colors)
    ax3.set_ylabel('')
    ax3.set_title('USA', fontsize=14, fontweight='bold')

    size = len(data[data["country"]=="Japan"])
    colors = [cdict.get(a.upper()) for a in data[data["country"]=="Japan"].collection.value_counts().index]
    data[data["country"]=="Japan"].collection.value_counts().plot(kind="pie", autopct=my_fmt, ax=ax4, colors=colors)
    ax4.set_ylabel('');
    ax4.set_title('Japan', fontsize=14, fontweight='bold')

    plt.savefig(f"collection_{year}.png", dpi=250)


def plot_boxplot(data_2021:pd.DataFrame, data_2023:pd.DataFrame) -> None:
    """
    Plot boxplots for each market in 2021 and 2023.
    Prices are take excluded tax and convert in euros with 
    the exange rate of the respective year.

    Args:
        data_2021 (pd.DataFrame): 2021 Panerai data
        data_2023 (pd.DataFrame): 2023 Panerai data
    """
    ### Retrive exange rates
    exchange_2021 = utils.change_currency(2021, 12, 15)
    exchange_2023 = utils.change_currency(2023, 6, 16)

    ### Convert to euros
    data_2021_eur = utils.set_to_euros(data_2021.copy(), exchange_2021)
    data_2023_eur = utils.set_to_euros(data_2023.copy(), exchange_2023)


    ### Plot
    fig = plt.figure(figsize = (15, 5),  dpi=250)
    fig.suptitle('2021 vs 2023', fontsize=30, weight="bold")

    ax1 = fig.add_subplot(1, 2, 1)
    sns.boxplot(x=data_2021_eur['price_exclTax'], y=data_2021_eur['country'], ax=ax1, order=['France', 'UK', 'Japan', 'USA']);
    ax1.set_ylabel('')
    ax1.set_xlim(0,32500)

    ax2 = fig.add_subplot(1, 2, 2)
    sns.boxplot(x=data_2023_eur['price_exclTax'], y=data_2023_eur['country'], ax=ax2, order=['France', 'UK', 'Japan', 'USA']);
    ax2.set_ylabel('')
    ax2.set_xlim(0,32500)

    plt.savefig(f"boxplot_alleuros_2021_2023.png", dpi=250)



def plot_hist(data_2021:pd.DataFrame, data_2023:pd.DataFrame, country:str) -> None:
    """
    Plot price histograms of each collection for 2021 and 2023 data

    Args:
        data_2021 (pd.DataFrame): 2021 Panerai data
        data_2023 (pd.DataFrame): 2023 Panerai data
        country (str): country to study
    """
    palette = sns.color_palette()

    fig = plt.figure(figsize = (15, 14),  dpi=250)

    ax1 = fig.add_subplot(4, 2, 1)
    data_2021[
        ((data_2021['country']==country) &
        (data_2021['collection']=='LUMINOR') 
        )]['price_exclTax'].plot(kind='hist', ax=ax1, color=palette[4])
    ax1.set_title(f'{country} 2021')

    ax2 = fig.add_subplot(4, 2, 2)
    data_2023[
        ((data_2023['country']==country) &
        (data_2023['collection']=='Luminor')
        )]['price_exclTax'].plot(kind='hist', ax=ax2, color=palette[4])
    ax2.set_title(f'{country} 2023')


    ax3 = fig.add_subplot(4, 2, 3)
    data_2021[
        ((data_2021['country']==country) &
        (data_2021['collection']=='RADIOMIR') 
        )]['price_exclTax'].plot(kind='hist', ax=ax3, color=palette[5])


    ax4 = fig.add_subplot(4, 2, 4)
    data_2023[
        ((data_2023['country']==country) &
        (data_2023['collection']=='Radiomir')
        )]['price_exclTax'].plot(kind='hist', ax=ax4, color=palette[5])


    ax5 = fig.add_subplot(4, 2, 5)
    data_2021[
        ((data_2021['country']==country) &
        (data_2021['collection']=='LUMINOR-DUE') 
        )]['price_exclTax'].plot(kind='hist', ax=ax5, color=palette[6])

    ax6 = fig.add_subplot(4, 2, 6)
    data_2023[
        ((data_2023['country']==country) &
        (data_2023['collection']=='Luminor-Due')
        )]['price_exclTax'].plot(kind='hist', ax=ax6, color=palette[6])


    ax7 = fig.add_subplot(4, 2, 7)
    data_2021[
        ((data_2021['country']==country) &
        (data_2021['collection']=='SUBMERSIBLE') 
        )]['price_exclTax'].plot(kind='hist', ax=ax7, color=palette[7])

    ax8 = fig.add_subplot(4, 2, 8)
    data_2023[
        ((data_2023['country']==country) &
        (data_2023['collection']=='Submersible')
        )]['price_exclTax'].plot(kind='hist', ax=ax8, color=palette[7])


    ax12_xlim = 180e3 
    ax34_xlim = 330e3
    ax56_xlim = 32e3
    ax78_xlim = 200e3

    ax1.set_xlim(0,ax12_xlim)
    ax2.set_xlim(0,ax12_xlim)
    ax3.set_xlim(0,ax34_xlim)
    ax4.set_xlim(0,ax34_xlim)
    ax5.set_xlim(0,ax56_xlim)
    ax6.set_xlim(0,ax56_xlim)
    ax7.set_xlim(0,ax78_xlim)
    ax8.set_xlim(0,ax78_xlim)


    ax2.legend(['LUMINOR'])
    ax4.legend(['RADIOMIR'])
    ax6.legend(['LUMINOR-DUE'])
    ax8.legend(['SUBMERSIBLE'])

    plt.savefig(f"histplot_price_{country}.png", dpi=250)
    

