from pdb import pm
from warnings import filterwarnings
import pandas as pd
from typeguard import TypeChecker, TypeWarning
import fitbit
#import sheets
#
filterwarnings("always", category=TypeWarning)
if 1: #with TypeChecker(["fitbit"]):
    sleep = fitbit.get_data("2019-04-01", "2019-05-01")
    sleep = fitbit.get_data("2019-04-01", "2019-04-17")


# I'm going to do this is all in an unorganized way right now and make a better layout later 


def find_sleep_times(log: pd.DataFrame) -> pd.Series:
    dup_ts = pd.DataFrame({"content": log["content"], "ts": log.index})
    all_sleeps = dup_ts[log["content"] == "sleep"]
    # in the evening, this rounds to the next day (so we substract it to the correct bedtime day)
    # we want to consider early morning as the previous day, early morning rounds to the same day
    # so substracting gives us the day we want
    day_groups = all_sleeps.groupby(lambda ts: ts.round("D") - pd.Timedelta("1D"))
    sleep_times = day_groups.last()["ts"]
    return sleep_times

def test_find_sleep_times():
    test_data = sheets.read_log("test-data/sleep_times_log.csv")
    expected = pd.Series(
    	pd.to_datetime(["2019-05-11 00:30", "2019-05-11 23:33", "2019-05-13 23:21"]),
    	index=pd.to_datetime(["2019-05-10", "2019-05-11", "2019-05-13"])
    )
    assert (find_sleep_times(test_data) == expected).all()


#log = sheets.get_data()

