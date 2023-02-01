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
        events (list): list of event names
    """
    
    df1 = pd.read_csv(f"results/events_daily_counts/{events[0]}.csv")
    df1 = df1.set_index("dates")
    
    df2 = pd.read_csv(f"results/events_daily_counts/{events[1]}.csv")
    df2 = df2.set_index("dates")

    df_add = df1.add(df2, fill_value=0)
    
    df_add.reset_index(inplace=True)
    name = events[0].split('_')[0] + '_' + events[0].split('_')[2]
    df_add.to_csv(f"results/events_daily_counts/{name}_total.csv", index=False)

def event_vs_announcements(events: list):
    """Plot events vs fed announcements

    Args:
        events (list): list of combined events filenames
    """

    for name in events:
        df = pd.read_csv(f"results/events_daily_counts/{name}.csv")
        df.dates = pd.to_datetime(df.dates)

        df = df[df.dates > "2020-01-01"]
        df_anns = pd.read_csv("utils/announcements.csv")
        df_anns.anns = pd.to_datetime(df_anns.anns)
        if name.split('_')[0] == "Maker":
            df = df[df.dates > "2020-06-01"]
            df_anns = df_anns[df_anns.anns > "2020-06-01"]

        df = df.set_index("dates")
        sns.set_theme()
        fig, ax = plt.subplots()

        chart = sns.lineplot(data=df, x="dates",
                            y="count").get_figure().autofmt_xdate()

        # Dates of Announcements
        # Adding vertical lines for the Announcements
        for i in df_anns.anns.values:
            plt.axvline(x=i, color='red', linewidth=0.4, linestyle='-')

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
        plt.xlabel(None)
        ylabel = name.split('_')[0] + ' daily ' + name.split('_')[1]
        plt.ylabel(ylabel)

        plt.savefig(f'results/figures/events_vs_announcements/{name}.jpg',
                    dpi=200, bbox_inches='tight')
        plt.clf()

    


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
        # 'Compound_v2_liquidations', 
        # 'Compound_v1_liquidations',
        # 'Compound_v1_repay',
        # 'Compound_v2_repay',
        # 'Maker_v1_Bite',
        # 'Maker_v2_Bark',
        # 'Liquity_liquidations',
        
        ## Combined Events files
        # "Aave_deposits_total",
        # "Aave_liquidations_total",
        # "Aave_repay_total",
        # "Compound_liquidations_total",
        # "Compound_repay_total",
        # "Maker_Bite_total",
        # "Liquity_liquidations",
        
        "makis_1_2"
    ]

    # for i in EVENTS:
    #     number_of_daily_events(i)

    # join_different_versions(['Aave_v1_liquidations',
    #                          'Aave_v3_liquidations',])
    
    # Plot events vs announcements
    event_vs_announcements(EVENTS)
