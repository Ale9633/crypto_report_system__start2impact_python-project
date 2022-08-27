import json
import logging
import requests
import os
import time
from datetime import datetime
import emoji

logging.basicConfig(level=logging.INFO, filename="log.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")
logging.debug("debug")
logging.info("info")
logging.warning("warning")
logging.error("error")
logging.critical("critical")

class CoinmarketcapApi:
    """Connect JSON to CoinMarketCap"""
    def __init__(self):
        self.url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        self.parameters = {}
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '959fbabc-4d77-4796-8eec-17cfa1337607',
        }

    def fetch_currencies_data(self):
        # Return data directly from CoinMarketCap and keep your report updated (API refresh rate: 60s)
        r = requests.get(url=self.url, params=self.parameters, headers=self.headers).json()
        return r["data"]

class GetCurrencies(CoinmarketcapApi):
    """Create different reports for different tasks"""

    def __init__(self):
        super().__init__()

    def best_volume_24h(self):
        # Crypto with the $ largest volume of the last 24 hours

        self.parameters = {
            "convert": "USD",
            "start": 1,
            "limit": 1,
            "sort": "volume_24h",
            "sort_dir": "desc"
        }

        output = self.fetch_currencies_data()
        return output

    def best_percent_increment_24h(self):
        # Best top 10 Crypto % increase in the last 24 hours

        self.parameters = {
            "convert": "USD",
            "start": 1,
            "limit": 10,
            "sort": "percent_change_24h",
            "sort_dir": "desc",
            "percent_change_24h_min": 0
        }

        output = self.fetch_currencies_data()
        return output

    def worst_percent_increment_24h(self):
        # Worst top 10 Crypto % increase in the last 24 hours

        self.parameters = {
            "convert": "USD",
            "start": 1,
            "limit": 10,
            "sort": "percent_change_24h",
            "sort_dir": "asc",
            "percent_change_24h_min": 0
        }

        output = self.fetch_currencies_data()
        return output

    def top_twenty_market_cap_rank(self):
        # Top 20 Crypto in order of CoinMarketCap's market cap rank

        self.parameters = {
            "convert": "USD",
            "start": 1,
            "limit": 20,
            "sort": "market_cap",
            "sort_dir": "desc",
        }

        output = self.fetch_currencies_data()
        return output

    def dollar_per_top_twenty(self):
        # The amount of $ per unit of each top 20 Crypto
        amount = 0

        self.parameters = {
            "convert": "USD",
            "start": 1,
            "limit": 20,
            "sort": "market_cap",
            "sort_dir": "desc",
        }

        output = self.fetch_currencies_data()
        for crypto in output:
            amount += crypto["quote"]["USD"]["price"]
        return round(amount, 2)

    def dollar_per_all(self):
        # The amount of $ per unit of all Crypto in CoinMarketCap with a $76000000 threshold of minimum volume in the last 24h
        amount = 0

        self.parameters = {
            "convert": "USD",
            "start": 1,
            "limit": 5000,
            "sort": "market_cap",
            "volume_24h_min": 76000000
        }

        output = self.fetch_currencies_data()
        for crypto in output:
            amount += crypto["quote"]["USD"]["price"]
        return round(amount, 2)

    def profit_loss_yesterday(self):
        # % Profit/loss buying one of each top 20 Crypto both today and yesterday (assuming the same rank)
        yesterday_amount = 0
        today_amount = 0

        self.parameters = {
            "convert": "USD",
            "start": 1,
            "limit": 20,
            "sort": "market_cap",
            "sort_dir": "desc"
        }

        output = self.fetch_currencies_data()
        for crypto in output:
            today_amount += crypto["quote"]["USD"]["price"]
            yesterday_price = crypto["quote"]["USD"]["price"] / (1 + (crypto["quote"]["USD"]["percent_change_24h"] / 100))
            yesterday_amount += yesterday_price
        profit_loss = round(((today_amount - yesterday_amount) / yesterday_amount) * 100, 1)
        return profit_loss

def report_settings(report):
    # Function to create the complete JSON report (the file name is gonna be as equal as the datetime.now() object)
    file_name = time.strftime("CoinMarketCap_Report %Y-%m-%d.json", time.localtime())
    script_dir = os.path.dirname(os.path.abspath(__file__))
    destination_dir = os.path.join(script_dir, 'CoinMarketCap JSON Reports')
    path = os.path.join(destination_dir, file_name)

    # Directory creation with 'os'
    try:
        os.makedirs(destination_dir)
    except FileExistsError as e:
        logging.exception("Unable to create a file, coz the file already exists: 'docs'")
    with open(path, "w") as outfile:
        json.dump(report, outfile, indent=4)

def json_report():
    # Run and display a recap of the GetCurrencies class
    seconds = 60
    minutes = 60
    hours = 24
    standby = (seconds * minutes) * hours

    while True:
        report = GetCurrencies()

        print(f"""Hi there! {emoji.emojize(":waving_hand:")}
This is a li'l recap of your JSON Crypto-Report, based on CoinMarketCap API.\n
    {emoji.emojize(":calendar:")} --> {datetime.now().strftime("%Y-%m-%d")}
    {emoji.emojize(":eight_o’clock:")} --> {datetime.now().strftime("%H:%M:%S")}
\nLet's get into it!
\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
\n\nThis is the top 20 Crypto in order of CoinMarketCap's market cap rank: {report.top_twenty_market_cap_rank()}\n\n
\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
\n\n*** Start2impact Python Project, made with {emoji.emojize(":red_heart:")}By Alessio Nava ***\n\n""")

        report_settings(report)
        time.sleep(standby)

if __name__ == "__main__":
    json_report()


#                                               RICORDATI DI RIMUOVERE LA PASSWORD DELL'API --> (COINMARKETCAP_API_KEY)

# \n\nThis is the top 20 Crypto in order of CoinMarketCap's market cap rank: {report.top_twenty_market_cap_rank()}\n\n
# \n1) Crypto with the $ largest volume of the last 24 hours: {report.best_volume_24h()}
# \n2) Best top 10 Crypto % increase in the last 24 hours: {report.best_percent_increment_24h()}
#      Worst top 10 Crypto % increase in the last 24 hours: {report.worst_percent_increment_24h()}
# \n3) The amount of $ per unit of each top 20 Crypto: {report.dollar_per_top_twenty()}$
# \n4) The amount of $ per unit of all Crypto in CoinMarketCap with a $76000000 threshold of minimum volume in the last 24h: {report.dollar_per_all()}$
# \n5) % Profit/loss buying one of each top 20 Crypto both today and yesterday (assuming the same rank): {report.profit_loss_yesterday()}%