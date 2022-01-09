import requests, json, yaml, os
from requests.exceptions import HTTPError
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    try:
        stream = open(os.getcwd() + "/config.yml", 'r')
        config = yaml.load(stream, Loader=yaml.FullLoader)

        set_url_api_key = f'https://freecurrencyapi.net/api/v2/latest?apikey={config["api_key"]}&base_currency=TRY'

        req = requests.get(set_url_api_key).text
        req_loads = json.loads(req)

        get_base = req_loads.get("query").get("base_currency")
        get_data = req_loads.get('data')

        compare_list = ['TRY', 'USD', 'EUR', 'HUF', 'CHF', 'SEK', 'PLN']

        match_pair = dict()
        try_rate = dict()

        for key in get_data:
            for each in compare_list:
                if key == each and key == "TRY":
                    try_rate[key] = get_data[key]
                elif key == each:
                    match_pair[key] = get_data[key]

        return render_template("index.html", match_pair=match_pair, try_rate=try_rate)

    except HTTPError as http_err:

        print(f'HTTP error occurred: {http_err}')

    except Exception as err:

        print(f'Other error occurred: {err}')


if __name__ == '__main__':
    app.run(debug=True)
