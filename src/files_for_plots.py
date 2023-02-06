# Module containing operations
# to preprocess files for plots

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates


def number_of_daily_events(event_name: str):
    """Events daily count to .csv

    Args:
        event_name (str): name of event
    """
    df = pd.read_csv(f"results/events/{event_name}.csv")
    
    df.dates = pd.to_datetime(df.dates, utc=True)
    cdf = pd.DataFrame({"count": df.groupby(df.dates.dt.date).size()})
    cdf.reset_index(inplace=True)
    cdf.to_csv(f"results/events_daily_counts/{event_name}.csv", index=False)

def join_different_versions(events: list):
    """Join events .csv from the same
        Protocol but different version

    Args:
        events (list)    : list of event names
    """
    
    df1 = pd.read_csv(f"results/events_daily_counts/{events[0]}.csv")
    df1 = df1.set_index("dates")
    
    df2 = pd.read_csv(f"results/events_daily_counts/{events[1]}.csv")
    df2 = df2.set_index("dates")

    df_add = df1.add(df2, fill_value=0)
    
    df_add.reset_index(inplace=True)
    name = events[0].split('_')[0] + '_' + events[0].split('_')[2]
    df_add.to_csv(f"results/events_daily_counts/{name}_total.csv", index=False)

def event_vs_announcements(events: list, time_window: str):
    """Plot events vs fed announcements

    Args:
        events (list)    : list of combined events filenames
        time_window (str): time window of results
                           options: 'total', '2022'
    """

    for name in events:
        # Events daily counts
        df = pd.read_csv(f"results/events_daily_counts/{name}.csv")
        df.dates = pd.to_datetime(df.dates)

        # Dates of Announcements
        df_anns = pd.read_csv("utils/announcements.csv")
        df_anns.anns = pd.to_datetime(df_anns.anns)

        # Different protocols start at different dates
        if name.split('_')[0] == "Maker":
            df = df[df.dates > "2020-06-01"]
            df_anns = df_anns[df_anns.anns > "2020-06-01"]
        elif name.split('_')[0] == "Aave":
            df = df[df.dates > "2020-01-01"]
            df_anns = df_anns[df_anns.anns > "2020-01-01"]
        elif name.split('_')[0] == "Liquity":
            df = df[df.dates > "2021-01-01"]
            df_anns = df_anns[df_anns.anns > "2021-01-01"]
            

        if time_window == "2022":
            df = df[df.dates > "2021-12-01"]
            df_anns = df_anns[df_anns.anns > "2021-12-01"]
        
        df = df.set_index("dates")
        
        ## Plotting
        sns.set_theme()
        fig, ax = plt.subplots()
        chart = sns.lineplot(data=df, x="dates",
                            y="count").get_figure().autofmt_xdate()

        # Adding vertical lines for the Announcements
        for i in df_anns.anns.values:
            plt.axvline(x=i, color='red', linewidth=0.4, linestyle='-')

        # Fixing dates format on xaxis
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
        plt.xlabel(None)
        ylabel = name.split('_')[0] + '_' + name.split('_')[1] + '_' + time_window
        plt.ylabel(ylabel)
        
        # Fix for aave v3 versions
        if name.split('_')[1] == "v3":
            ylabel = ylabel + '_' + name.split('_')[2]


        # Save figure to .jpg
        plt.savefig(f'results/figures/events_vs_announcements/{ylabel}.jpg',
                    dpi=200, bbox_inches='tight')
        plt.clf()

def anns_vs_non_anns(events: list):
    # TODO
    """Plots for comparing
    announcements vs non-announcements days

    Args:
        events (list): _description_
    """
    pass


def add_is_fed_ann(events: list, plus_minus=1):
    """Add a column if this date
    is a date of Fed announcement

    Args:
        events (list)   : events
        plus_minus (int): number of plus-minus days
                          close to announcement
                          to be taken into account
    """

    
    for name in events:
        df = pd.read_csv(f"results/events_daily_counts/{name}.csv")
        df.dates = pd.to_datetime(df.dates)
        
        # Fed Announcements Dates
        df_anns = pd.read_csv("utils/announcements.csv")
        df_anns.anns = pd.to_datetime(df_anns.anns)
        
        df["is_Fed_Announcement"] = df.dates.apply(lambda x: x in df_anns.anns.values)
        
        df[f"plus_minus_{plus_minus}days"] = df.dates.apply(lambda x:
            x in df_anns.anns.values or 
            (x.date() + pd.Timedelta(days=plus_minus)) in df_anns.anns.to_list() or
            (x.date() + pd.Timedelta(days=-plus_minus)) in df_anns.anns.to_list()
        )

        
        df.to_csv(f"results/events_daily_counts/{name}.csv", index=False)
    
    

if __name__ == "__main__":
    
    EVENTS = [
        ## Single Event files
        # 'Aave_v1_liquidations',
        # 'Aave_v3_liquidations',
        # 'Aave_v2_flashloans',
        # 'Aave_v1_deposits',
        # 'Aave_v2_deposits',
        # 'Aave_v1_repay',
        # 'Aave_v2_repay',
        
        # 'Aave_v3_borrows',
        # 'Aave_v3_withdraws',

        #   'Compound_v2_liquidations',
        #   'Compound_v1_liquidations',
        #   'Compound_v1_repay',
        #   'Compound_v2_repay',

        # 'Compound_v1_deposits',
        # 'Compound_v2_deposits',
        # 'Compound_v1_withdraws',
        # 'Compound_v2_withdraws',
        # 'Compound_v1_borrows',
        # 'Compound_v2_borrows',
        
        # 'Maker_v1_Bite',
        # 'Maker_v2_Bark',
        # 'Liquity_liquidations',
        
        ## Combined Events files
        # "Aave_deposits_total",
        # "Aave_liquidations_total",
        # "Aave_repay_total",
        # "Compound_liquidations_total",
        # "Compound_repay_total",
        
        "Aave_v3_borrows",
        "Aave_v3_withdraws",
        "Compound_deposits_total",
        "Compound_withdraws_total",
        "Compound_borrows_total",
        
        # "Maker_Bite_total",
        # "Liquity_liquidations",

    ]

    # for i in EVENTS:
    #     number_of_daily_events(i)

    # join_different_versions(['Compound_v1_borrows',
    #                          'Compound_v2_borrows',])
    
    # Plot events vs announcements
    event_vs_announcements(EVENTS, time_window="total")
    
    # add_is_fed_ann(EVENTS, plus_minus=2)
