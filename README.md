# Stocks Tracker

API endpoint to track your investment in a given stock. Simply input stock ticker, number of stocks and purchase date to view the following statistics

```
{
	principal
	current_value
	capital_gain
	dividends
	total_gain
	percent_gain
}
```

## Installation and Setup

In the root folder, create a virtual environment and activate it

```
python3 -m venv env
source env/bin/activate
```

Install packages

```
pip install -r requirements.txt
```

Run migrations for the user model in the default sqlite database

```
python manage.py migrate
```

Create a super user

```
python manage.py createsuperuser
```

This API utilizes the [Alpha Vantage API](https://www.alphavantage.co/). [Signup](https://www.alphavantage.co/support/#api-key) for an API key, create a `.env` file in the `backend` folder, and place the key in it like so

```
ALPHAVANTAGE_API_KEY=PASTE_YOUR_KEY_HERE
```

## Running the API

With the virtual environment activated in the root folder, start the server

```
python manage.py runserver
```

For quick testing, open a new browser window and go to [http://127.0.0.1:8000/api/track](http://127.0.0.1:8000/api/track)
After logging in with your super user credentials, parameters can be submitted via the post content section.
Example parameters:

```
{"ticker": "AAPL","number_stocks": "30","start":"2018-03-09"}
```

Alternatively, use curl on the command line. Replace user and password with your super user credentials

```
curl -X POST -H 'Accept: application/json; indent=4' -u user:password http://127.0.0.1:8000/api/track -d "ticker=AAPL&number_stocks=30&start=2018-03-09"
```

[See the official Django REST framework docs](https://www.django-rest-framework.org/tutorial/quickstart/#testing-our-api) for more info
