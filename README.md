<p align="center">
<img src="https://user-images.githubusercontent.com/91788111/187063710-e977356b-a0ec-4f89-85f1-db087101ff3d.jpg" width="350" height="300"/>
</p>

<h1 align="center">Start2impact: Python project</h1>
<h3 align="center">Create a Crypto reporting system, using CoinMarketCap’s API :desktop_computer:[^1]</h3><br /><br />
</h1>

Every day, at a certain specific time, we wanna get as much information as possible about cryptocurrencies, process it and store the results in a JSON file.

The following information will be written in the report:<br /><br />

1) **The Crypto with the largest volume** *(in $)* of the last 24 hours.

2) **The best and worst 10 cryptocurrencies** *(by % increase)* of the last 24 hours.

3) **The amount of $** needed to buy one unit of **each of the top 20 cryptocurrencies**[^2]

4) **The amount of $** required to purchase *a unit of all Crypto whose volume in the last 24 hours exceeds 76,000,000$.[^2]

5) **Profit/loss %** you would have made if you had bought one unit of each of the top 20 cryptocurrencies the day before (assuming that the rankings have not changed).<br /><br />




Once the project is complete, **send the report in JSON.**<br />
<sub>*To prevent your program from overwriting the same JSON file, name it with the ‘program run’ date (use datetime module).*</sub>




[^1]: Click [here](https://www.figma.com/file/JlmizyQeC6dW1Y5WetGrlU/Python-Project%3A-Flowchart?node-id=0%3A1) to see the complete flowchart of the project (*realized with Figma*)
[^2]: (the top 20 according to the CoinMarketCap default ranking, therefore sorted by capitalization)
