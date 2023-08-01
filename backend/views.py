from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
import environ
import requests

env = environ.Env()
environ.Env.read_env()


class StocksApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # for alpha vantage api docs, see https://www.alphavantage.co/documentation/
        url = 'https://www.alphavantage.co/query'
        params = {
            # 'adjusted' factors in price changes due to stock splits
            'function': 'TIME_SERIES_MONTHLY_ADJUSTED',
            'symbol': request.data.get('ticker'),
            'apikey': env("ALPHAVANTAGE_API_KEY"),
        }
        r = requests.get(url, params=params)
        data = r.json()

        if data.get("Monthly Adjusted Time Series") is not None:
            # key info from alpha vantage API
            start_month = request.data.get('start')[0:7]
            start_price = {key: value for key, value in data["Monthly Adjusted Time Series"].items()
                           if key.startswith(start_month)}
            start_price = list(start_price.values())[0]['5. adjusted close']

            current_price = list(data["Monthly Adjusted Time Series"].values())[
                0]['5. adjusted close']

            # calculated statistics
            number_stocks = float(request.data.get('number_stocks'))
            principal = float(start_price) * number_stocks
            current_value = float(current_price) * number_stocks
            price_change = float(current_price) - float(start_price)
            capital_gain = price_change * number_stocks
            dividends = sum_dividends(
                data["Monthly Adjusted Time Series"], start_month) * number_stocks
            total_gain = capital_gain + dividends
            total_current_value = current_value + dividends
            percent_gain = (total_current_value / principal - 1) * 100

            result = {
                'principal': round(principal, 2),
                'current_value': round(current_value, 2),
                'capital_gain': round(capital_gain, 2),
                'dividends': round(dividends, 2),
                'total_gain': round(total_gain, 2),
                'percent_gain': round(percent_gain, 2),
            }

            return Response(data=result, status=200)
        else:
            return (Response(status=400))


def sum_dividends(data, start_month):
    dividends = 0
    for key, value in data.items():
        dividends = dividends + float(value['7. dividend amount'])

        if (key.startswith(start_month)):
            break

    return dividends
