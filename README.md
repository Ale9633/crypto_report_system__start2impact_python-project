<p align="center">
<img src="https://user-images.githubusercontent.com/91788111/187063710-e977356b-a0ec-4f89-85f1-db087101ff3d.jpg" width="350" height="300"/>
</p>

<h1 align="center">Start2impact: Python project</h1>
<h3 align="center">Create a Crypto reporting system, using CoinMarketCap’s API 🖥️</h3><br />



<h2>📝Tasks</h2>
Every day, at a certain specific time, we wanna get as much information as possible about cryptocurrencies, process it and store the results in a JSON file.<br /><br /><br />

The following information will be written in the report:<br />

1) **The Crypto with the largest volume** *(in $)* of the last 24 hours.

2) **The best and worst 10 cryptocurrencies** *(by % increase)* of the last 24 hours.

3) **The amount of $** needed to buy one unit of **each of the top 20 cryptocurrencies**[^1]

4) **The amount of $** required to purchase **a unit of all Crypto whose volume in the last 24 hours exceeds 76,000,000$.**[^1]

5) **Profit/loss %** you would have made if you had bought one unit of each of the top 20 cryptocurrencies the day before (assuming that the rankings have not changed).<br /><br />


Once the project is complete, **send the report in JSON.**<br />
<sub>*To prevent your program from overwriting the same JSON file, name it with the ‘program run’ date (use datetime module).*</sub><br /><br /><br />





## 🧑🏻‍💻How I worked[^2]<br />
<img width="2906" alt="Python Project_ Flowchart" src="https://user-images.githubusercontent.com/91788111/187067341-2e1ead2e-532b-4605-af0c-7a291fec8e3a.png"><br />
> **The CoinMarketCap API** is a suite of **high-performance RESTful JSON** endpoints that are specifically designed to meet the mission-critical demands of application developers, data scientists, and enterprise business platforms.

<br />Let's start connecting our *"script.py"* file to CoinMarketCap...[^3]
```python
class CoinmarketcapApi:
    """Connecting to CoinMarketCap"""
    def __init__(self):
        self.url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        self.parameters = {}
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'YOUR_COINMARKETCAP_API_KEY',
        }
    ...

```

...implementing this **request function** as well to fetch data directly from the API:

```python
    ...
    def fetch_currencies_data(self):
        # Return data directly from CoinMarketCap and keep your report updated (API refresh rate: 60s)
        r = requests.get(url=self.url, params=self.parameters, headers=self.headers).json()
        return r["data"]
```


<br /><br />
Awesome!🚀<br />
Once the live production environment is set up, let's create the class ***'GetCurrencies'*** which will cointain all functions of the program:<br />


```python
class GetCurrencies(CoinmarketcapApi):
    """Create different reports for different tasks"""

    def __init__(self):
        super().__init__()
        ...
```
Now link all functions and 📦 them in ***GetCurrencies()*** with the One that creates the JSON final report.
```python
        ...
        self.conversion = self.to_json()
```


<br /><br />
OK! Everything works well...<br />
It's time to move on to tasks and fetch data, grouping them according to the project requests above.<br />
**Take it away**🔥
<br /><br />








#### 1️⃣best volume 24h ($)
<p align="center">
<img src="https://user-images.githubusercontent.com/91788111/187084522-24a8aabe-3890-4da9-af27-7cf03acc45ce.png" width="600" height="200"/>
</p>

```python
    def best_volume_24h(self):

        self.parameters = {
            "convert": "USD",
            "start": 1,
            "limit": 1,
            "sort": "volume_24h",
            "sort_dir": "desc"
        }

        output = self.fetch_currencies_data()
        return output[0]
```
<br />
Key data:<br />

- ***convert_id:*** Optionally calculate market quotes by CoinMarketCap ID instead of symbol. This option is identical to convert outside of ID format. Ex: convert_id=1,2781 would replace convert=BTC,USD in your query. This parameter cannot be used when convert is used.
- ***start:*** Optionally offset the start (1-based index) of the paginated list of items to return.[^4]
- ***limit:*** Optionally specify the number of results to return. Use this parameter and the "start" parameter to determine your own pagination size.[^5]
- ***sort:*** What field to sort the list of cryptocurrencies by.[^6]
- ***sort_dir:*** The direction in which to order cryptocurrencies against the specified sort.[^7]
<br />



#### 2️⃣best & worst crypto (% increase)
<p align="center">
<img src="https://user-images.githubusercontent.com/91788111/187084355-b83f9a24-8045-4f7c-a481-749a3e30167b.png" width="600" height="400"/>
</p>

```python
    def best_percent_increment_24h(self):

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
```
```python
    def worst_percent_increment_24h(self):

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
```
<br />
Key data:<br />

- ***convert_id:*** Optionally calculate market quotes by CoinMarketCap ID instead of symbol. This option is identical to convert outside of ID format. Ex: convert_id=1,2781 would replace convert=BTC,USD in your query. This parameter cannot be used when convert is used.
- ***start:*** Optionally offset the start (1-based index) of the paginated list of items to return.[^4]
- ***limit:*** Optionally specify the number of results to return. Use this parameter and the "start" parameter to determine your own pagination size.[^5]
- ***sort:*** What field to sort the list of cryptocurrencies by.[^6]
- ***sort_dir:*** The direction in which to order cryptocurrencies against the specified sort.[^7]
- ***percent_change_24h_min***: Optionally specify a threshold of minimum 24 hour percent change to filter results by.[^8]
<br />




#### 3️⃣$ amount (each top 20 crypto)
<p align="center">
<img src="https://user-images.githubusercontent.com/91788111/187084599-34e75afb-9a7b-481f-b9ba-a18a341369b7.png" width="90%"/>
</p>

```python
    def dollar_per_top_twenty(self):
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
```
<br />
Key data:<br />

- ***convert_id:*** Optionally calculate market quotes by CoinMarketCap ID instead of symbol. This option is identical to convert outside of ID format. Ex: convert_id=1,2781 would replace convert=BTC,USD in your query. This parameter cannot be used when convert is used.
- ***start:*** Optionally offset the start (1-based index) of the paginated list of items to return.[^4]
- ***limit:*** Optionally specify the number of results to return. Use this parameter and the "start" parameter to determine your own pagination size.[^5]
- ***sort:*** What field to sort the list of cryptocurrencies by.[^6]
- ***sort_dir:*** The direction in which to order cryptocurrencies against the specified sort.[^7]
<br />





#### 4️⃣$ amount (all crypto with volume > 76.000.000$)
<p align="center">
<img src="https://user-images.githubusercontent.com/91788111/187085096-32aa0f8c-46ef-40f2-b37e-c5d32c8ef58e.png" width="90%" height="250"/>
</p>

```python
    def dollar_per_all(self):
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
```
<br />
Key data:<br />

- ***convert_id:*** Optionally calculate market quotes by CoinMarketCap ID instead of symbol. This option is identical to convert outside of ID format. Ex: convert_id=1,2781 would replace convert=BTC,USD in your query. This parameter cannot be used when convert is used.
- ***start:*** Optionally offset the start (1-based index) of the paginated list of items to return.[^4]
- ***limit:*** Optionally specify the number of results to return. Use this parameter and the "start" parameter to determine your own pagination size.[^5]
- ***sort:*** What field to sort the list of cryptocurrencies by.[^6]
- ***volume_24h_min:*** Optionally specify a threshold of minimum 24 hour USD volume to filter results by.[^9]
<br />





#### 5️⃣% profit/loss timedelta=1 (each top 20 crypto)
<p align="center">
<img src="https://user-images.githubusercontent.com/91788111/187085309-f8771417-c96e-44aa-9d56-bceee6cf40f1.png" width="90%" height="250"/>
</p>

```python
    def profit_loss_yesterday(self):
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
```
<br />
Key data:<br />

- ***convert_id:*** Optionally calculate market quotes by CoinMarketCap ID instead of symbol. This option is identical to convert outside of ID format. Ex: convert_id=1,2781 would replace convert=BTC,USD in your query. This parameter cannot be used when convert is used.
- ***start:*** Optionally offset the start (1-based index) of the paginated list of items to return.[^4]
- ***limit:*** Optionally specify the number of results to return. Use this parameter and the "start" parameter to determine your own pagination size.[^5]
- ***sort:*** What field to sort the list of cryptocurrencies by.[^6]
- ***sort_dir:*** The direction in which to order cryptocurrencies against the specified sort.[^7]
<br />




<p align="center">
<img src="https://media.giphy.com/media/l0Iy7z476CjEV3G0w/giphy.gif"/>
</p>














[^1]: (the top 20 according to the CoinMarketCap default ranking, therefore sorted by capitalization)
[^2]: Click [here](https://www.figma.com/file/JlmizyQeC6dW1Y5WetGrlU/Python-Project%3A-Flowchart?node-id=0%3A1) to see the complete flowchart of the project (*realized with Figma*)
[^3]: {'X-CMC_PRO_API_KEY': 'YOUR_COINMARKETCAP_API_KEY'} --> put your **private key** as ***'value'*** of 'X-CMC_PRO_API_KEY'
[^4]: *integer >= 1 (default = 1)*
[^5]: *integer [ 1 .. 5000 ] (default = 100)*
[^6]: *valid values: "name""symbol" | "date_added" | "market_cap" | "market_cap_strict" | "price""circulating_supply" | "total_supply" | "max_supply" | "num_market_pairs" | "volume_24h""percent_change_1h" | "percent_change_24h" | "percent_change_7d" | "market_cap_by_total_supply_strict" | "volume_7d""volume_30d" (default = 'market_cap')*
[^7]: *valid values: "asc" | "desc"*
[^8]: *number >= -100*
[^9]: *number [ 0 .. 100000000000000000 ]*
