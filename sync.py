import requests
from timeit import default_timer

def fetch(session, csv):
    base_url = "https://people.sc.fsu.edu/~jburkardt/data/csv/"
    with session.get(base_url + csv) as response:
        data = response.text
        if response.status_code != 200:
            print("FAILURE::{0}".format(url))
        # Return .csv data for future consumption
        return data

def get_data_synchronous():
    csvs_to_fetch = [
        "ford_escort.csv",
        "cities.csv",
        "hw_25000.csv",
        "mlb_teams_2012.csv",
        "nile.csv",
        "homes.csv",
        "hooke.csv",
        "lead_shot.csv",
        "news_decline.csv",
        "snakes_count_10000.csv",
        "trees.csv",
        "zillow.csv"
    ]

    with requests.Session() as session:
        print("{0:<30} {1:>20}".format("File", "Completed at"))

        # Set any session parameters here before calling `fetch`
        # For instance, if you needed to set Headers or Authentication
        # this can be done before starting the loop

        total_start_time = default_timer()
        for csv in csvs_to_fetch:
            fetch(session, csv)
            elapsed = default_timer() - total_start_time
            time_completed_at = "{:5.2f}s".format(elapsed)
            print("{0:<30} {1:>20}".format(csv, time_completed_at))

def main():
    # Simple for now
    get_data_synchronous()

main()
