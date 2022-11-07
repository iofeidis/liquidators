# FOMC Announcement Dates
# Format: {YYYY-MM-dd}

import pandas as pd

anns = ["2022-12-14",
        "2022-12-13",
        "2022-11-02",
        "2022-11-01",
        "2022-09-21",
        "2022-09-20",
        "2022-07-27",
        "2022-07-26",
        "2022-06-15",
        "2022-06-14",
        "2022-05-04",
        "2022-05-04",
        "2022-03-16",
        "2022-03-15",
        "2022-01-26",
        "2022-01-25",
        "2021-12-15",
        "2021-12-14",
        "2021-11-03",
        "2021-11-02",
        "2021-09-22",
        "2021-09-21",
        "2021-07-28",
        "2021-07-27",
        "2021-06-16",
        "2021-06-15",
        "2021-04-28",
        "2021-04-27",
        "2021-03-17",
        "2021-03-16",
        "2021-01-27",
        "2021-01-26",
        "2020-12-16",
        "2020-12-15",
        "2020-11-05",
        "2020-11-04",
        "2020-09-16",
        "2020-09-15",
        "2020-08-27",
        "2020-07-29",
        "2020-07-28",
        "2020-06-10",
        "2020-06-09",
        "2020-04-29",
        "2020-04-28",
        ]

df = pd.DataFrame({"anns":anns})

df.to_csv("announcements.csv", index=False)