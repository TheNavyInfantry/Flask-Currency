import requests, json, yaml, os
from datetime import datetime
from requests.exceptions import HTTPError
from flask import Flask
from flask import render_template, jsonify

app = Flask(__name__)

def do_request():
    stream = open(os.getcwd() + "/config.yml", 'r')
    config = yaml.load(stream, Loader=yaml.FullLoader)

    set_url_api_key = f'https://freecurrencyapi.net/api/v2/latest?apikey={config["api_key"]}&base_currency=TRY'

    req = requests.get(set_url_api_key).json()

    return req

def do_parsing():
    req = do_request()
    get_base = req.get("query").get("base_currency")
    get_data = req.get('data')
    get_timestamp = req.get("query").get("timestamp")

    compare_list = ['TRY', 'USD', 'EUR', 'HUF', 'CHF', 'SEK', 'PLN']

    match_pair = dict()
    try_rate = dict()

    for key in get_data:
        for each in compare_list:
            if key == each and key == get_base:
                try_rate[key] = get_data[key]
            elif key == each:
                match_pair[key] = get_data[key]

    ts = int(get_timestamp)
    timestamp = datetime.fromtimestamp(ts).strftime('%H:%M - %d/%m/%-Y')

    return match_pair,try_rate,timestamp

@app.route('/')
def index():
    try:

        match_pair, try_rate, timestamp = do_parsing()

        return render_template("display.html", match_pair=match_pair, try_rate=try_rate, timestamp=timestamp)

    except HTTPError as http_err:

        print(f'HTTP error occurred: {http_err}')

    except Exception as err:

        print(f'Other error occurred: {err}')

@app.route('/data_json')
def get_data_json():

    req2 = do_request()
    get_timestamp = req2.get("query").get("timestamp")

    ts = int(get_timestamp)
    set_timestamp = datetime.fromtimestamp(ts).strftime('%H:%M - %d/%m/%-Y')
    req2["query"]["timestamp"] = set_timestamp

    req2['data'] = do_parsing()
    return jsonify(req2)

if __name__ == '__main__':
    app.run(debug=True)