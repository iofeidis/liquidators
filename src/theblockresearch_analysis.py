# Module containing operations
# to preprocess files for plots
# coming from theblockresearch

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import os

def preprocess_file(filename: str):
    
    df = pd.read_csv(f"utils/theblockresearch/{filename}")
    df = df.set_index("Timestamp")
    df = df.pivot(columns="Series", values="Result")
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df.reset_index(inplace=True)
    df.to_csv(f"results/theblockresearch/{filename}", index=False)

def preprocess_all_files():
    
    for (root, dirs, files) in os.walk('utils/theblockresearch',
                                       topdown=True):
        for f in files:
            preprocess_file(f)

def plot_Protocol_Loan_to_Value(name: str, time_window: str = "2022"):
    """Plot Protocol's Loan to Value vs Announcements

    Args:
        name (str): filename
        time_window (str, optional): "total" or "2022". Defaults to "2022".
    """
    df = pd.read_csv(f"results/theblockresearch/{name}.csv")
    df.Timestamp = pd.to_datetime(df.Timestamp)
    
    # Dates of Announcements
    df_anns = pd.read_csv("utils/announcements.csv")
    df_anns.anns = pd.to_datetime(df_anns.anns)
    
    if time_window == "2022":
        df = df[df.Timestamp > "2021-12-01"]
        df_anns = df_anns[df_anns.anns > "2021-12-01"]

    
    df = df.set_index("Timestamp")
    
    # Plotting
    sns.set_theme()
    fig, ax = plt.subplots()
    chart = sns.lineplot(data=df, x="Timestamp",
                            y="Loan to Value").get_figure().autofmt_xdate()

    # Adding vertical lines for the Announcements
    for i in df_anns.anns.values:
        plt.axvline(x=i, color='red', linewidth=0.4, linestyle='-')

    # Fixing dates format on xaxis
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    plt.xlabel(None)
    ylabel = name + '_' + time_window
    plt.ylabel(ylabel)

    # Save figure to .jpg
    plt.savefig(f'results/figures/theblockresearch/{ylabel}.jpg',
                dpi=200, bbox_inches='tight')

def plot_Protocol_TVL_and_Debt(name: str, time_window: str = "2022",
                               values:str = "TVL"):
    """Plot Protocol's TVL or Debt vs Announcements

    Args:
        name (str): filename
        time_window (str, optional): "total" or "2022". Defaults to "2022".
        values (str, optional): "Outstanding Debt" or "TVL". Defaults to "TVL".
    """
    df = pd.read_csv(f"results/theblockresearch/{name}.csv")
    df.Timestamp = pd.to_datetime(df.Timestamp)
    
    # Dates of Announcements
    df_anns = pd.read_csv("utils/announcements.csv")
    df_anns.anns = pd.to_datetime(df_anns.anns)
    
    if time_window == "2022":
        df = df[df.Timestamp > "2021-12-01"]
        df_anns = df_anns[df_anns.anns > "2021-12-01"]

    
    df = df.set_index("Timestamp")
    
    # Plotting
    sns.set_theme()
    fig, ax = plt.subplots()
    chart = sns.lineplot(data=df, x="Timestamp",
                            y=values).get_figure().autofmt_xdate()

    # Adding vertical lines for the Announcements
    for i in df_anns.anns.values:
        plt.axvline(x=i, color='red', linewidth=0.4, linestyle='-')

    # Fixing dates format on xaxis
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    plt.xlabel(None)
    ylabel = name.split('TVL')[0] + '_' + values + '_' + time_window
    plt.ylabel(ylabel)

    # Save figure to .jpg
    plt.savefig(f'results/figures/theblockresearch/{ylabel}.jpg',
                dpi=200, bbox_inches='tight')

def plot_Ethereum_Lending_TVL(name: str, time_window: str = "2022"):
    """Plot added TVL of Aave & Compound vs Announcements

    Args:
        name (str): filename
        time_window (str, optional): "total" or "2022". Defaults to "2022".
    """
    df = pd.read_csv(f"results/theblockresearch/{name}.csv")
    df.Timestamp = pd.to_datetime(df.Timestamp)
    df['TVL'] = df['Aave v2'] + df['Compound v2']
    values = 'TVL'

    # Dates of Announcements
    df_anns = pd.read_csv("utils/announcements.csv")
    df_anns.anns = pd.to_datetime(df_anns.anns)

    if time_window == "2022":
        df = df[df.Timestamp > "2021-12-01"]
        df_anns = df_anns[df_anns.anns > "2021-12-01"]

    df = df.set_index("Timestamp")

    # Plotting
    sns.set_theme()
    fig, ax = plt.subplots()
    chart = sns.lineplot(data=df, x="Timestamp",
                         y=values).get_figure().autofmt_xdate()

    # Adding vertical lines for the Announcements
    for i in df_anns.anns.values:
        plt.axvline(x=i, color='red', linewidth=0.4, linestyle='-')

    # Fixing dates format on xaxis
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    plt.xlabel(None)
    ylabel = name.split('TVL')[0] + '_' + values + '_' + time_window
    plt.ylabel(ylabel)

    # Save figure to .jpg
    plt.savefig(f'results/figures/theblockresearch/{ylabel}.jpg',
                dpi=200, bbox_inches='tight')

def plot_Protocol_Daily_Net_Borrows(name: str, time_window: str = "2022",
                                    protocol: str = "Aave"):
    """Plot Protocol's Daily Net Borrows vs Announcements

    Args:
        name (str): filename
        time_window (str, optional): "total" or "2022". Defaults to "2022".
        protocol (str): protocol's name
    """
    df = pd.read_csv(f"results/theblockresearch/{name}.csv")
    df.Timestamp = pd.to_datetime(df.Timestamp)

    # Dates of Announcements
    df_anns = pd.read_csv("utils/announcements.csv")
    df_anns.anns = pd.to_datetime(df_anns.anns)

    if time_window == "2022":
        df = df[df.Timestamp > "2021-12-01"]
        df_anns = df_anns[df_anns.anns > "2021-12-01"]

    df = df.set_index("Timestamp")

    # Plotting
    sns.set_theme()
    fig, ax = plt.subplots()
    chart = sns.lineplot(data=df, x="Timestamp",
                         y=protocol).get_figure().autofmt_xdate()

    # Adding vertical lines for the Announcements
    for i in df_anns.anns.values:
        plt.axvline(x=i, color='red', linewidth=0.4, linestyle='-')

    # Fixing dates format on xaxis
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    plt.xlabel(None)
    ylabel = 'Daily_Net_Borrows' + '_' + protocol + '_' + time_window
    plt.ylabel(ylabel)

    # Save figure to .jpg
    plt.savefig(f'results/figures/theblockresearch/{ylabel}.jpg',
                dpi=200, bbox_inches='tight')

def plot_Total_DEX_Traders(name: str, time_window: str = "2022"):
    """Plot Total DEX Traders vs Announcements

    Args:
        name (str): filename
        time_window (str, optional): "total" or "2022". Defaults to "2022".
    """
    df = pd.read_csv(f"results/theblockresearch/{name}.csv")
    df.Timestamp = pd.to_datetime(df.Timestamp)

    # Dates of Announcements
    df_anns = pd.read_csv("utils/announcements.csv")
    df_anns.anns = pd.to_datetime(df_anns.anns)

    if time_window == "2022":
        df = df[df.Timestamp > "2021-12-01"]
        df_anns = df_anns[df_anns.anns > "2021-12-01"]

    df = df.set_index("Timestamp")

    # Plotting
    sns.set_theme()
    fig, ax = plt.subplots()
    chart = sns.lineplot(data=df, x="Timestamp",
                         y="Traders").get_figure().autofmt_xdate()

    # Adding vertical lines for the Announcements
    for i in df_anns.anns.values:
        plt.axvline(x=i, color='red', linewidth=0.4, linestyle='-')

    # Fixing dates format on xaxis
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    plt.xlabel(None)
    ylabel = 'Total_DEX_Traders' + '_' + time_window
    plt.ylabel(ylabel)

    # Save figure to .jpg
    plt.savefig(f'results/figures/theblockresearch/{ylabel}.jpg',
                dpi=200, bbox_inches='tight')


def plot_USD_Addresses_with_Balance_Over(name: str, time_window: str = "2022",
                                         values: str = "Over 10K"):
    """Plot USDC(T) Addresses with Balance Over X vs Announcements

    Args:
        name (str): filename
        time_window (str, optional): "total" or "2022". Defaults to "2022".
        values (str): "Over 100K", "Over 10K", "Over 10M", "Over 1K", "Over 1M"
    """
    df = pd.read_csv(f"results/theblockresearch/{name}.csv")
    df.Timestamp = pd.to_datetime(df.Timestamp)

    # Dates of Announcements
    df_anns = pd.read_csv("utils/announcements.csv")
    df_anns.anns = pd.to_datetime(df_anns.anns)

    if time_window == "2022":
        df = df[df.Timestamp > "2021-12-01"]
        df_anns = df_anns[df_anns.anns > "2021-12-01"]

    df = df.set_index("Timestamp")

    # Plotting
    sns.set_theme()
    fig, ax = plt.subplots()
    chart = sns.lineplot(data=df, x="Timestamp",
                         y=values).get_figure().autofmt_xdate()

    # Adding vertical lines for the Announcements
    for i in df_anns.anns.values:
        plt.axvline(x=i, color='red', linewidth=0.4, linestyle='-')

    # Fixing dates format on xaxis
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    plt.xlabel(None)
    ylabel = name.split('Add')[0] + '_#_of_Addresses'  + '_' + values + '_' + time_window
    plt.ylabel(ylabel)

    # Save figure to .jpg
    plt.savefig(f'results/figures/theblockresearch/{ylabel}.jpg',
                dpi=200, bbox_inches='tight')


if __name__ == "__main__":
    
    filenames = [
        # "AaveLoan-to-Value",
        # "CompoundLoan-to-Value", 
        # "MakerDAOLoan-to-Value",
        
        # "AaveTVLandOutstandingDebt",
        # "CompoundTVLandOutstandingDebt",
        
        # "EthereumLendingTVL",
        
        # "DailyNetBorrowsperProtocol",
        
        # "TotalEthereumDEXTraders",
        
        "USDCAddresseswithBalanceoverX",
        "USDTAddresseswithBalanceoverX",
        ]
    
    for i in filenames:
        # plot_Protocol_Loan_to_Value(i, time_window="total")
        
        # plot_Protocol_TVL_and_Debt(i, time_window="2022", values="TVL")
        
        # plot_Ethereum_Lending_TVL(i, time_window="total")
        
        # plot_Protocol_Daily_Net_Borrows(i, time_window="2022", protocol="Euler")
        
        # plot_Total_DEX_Traders(i, time_window="2022")
        
        plot_USD_Addresses_with_Balance_Over(i, time_window="2022",
                                             values="Over 10M")