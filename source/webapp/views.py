from django.shortcuts import render
import json
import requests
from datetime import datetime, timedelta

current = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"


def get_previous_price():
    one_hour_ago = datetime.now() - timedelta(hours=1)
    timestamp = int(one_hour_ago.timestamp() * 1000)
    historical_data_url = f"https://api.binance.com/api/v3/klines?symbol=ETHUSDT&interval=1m&startTime={timestamp}&limit=1"
    response = requests.get(historical_data_url)
    data = response.json()
    if data:
        previous_price = float(data[0][4])
        return previous_price
    return None


def main(request):
    current_price_response = requests.get(current)
    current_price_data = current_price_response.json()
    current_price = float(current_price_data['price'])
    previous_price = get_previous_price()

    if previous_price is not None:
        price_change_percentage = abs(current_price - previous_price) / previous_price * 100

        if price_change_percentage >= 1.0:
            ans = "Price has changed by 1% or more in the last hour."
        else:
            ans = "Price has changed less than 1% in the last hour."
    else:
        ans = "Unable to retrieve previous price."

    context = {
        'symbol': current_price_data['symbol'],
        'current_price': current_price,
        'previous_price': previous_price,
        'ans': ans
    }
    return render(request, "main_list.html", context)