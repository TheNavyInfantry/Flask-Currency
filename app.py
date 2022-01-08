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

        return render_template("index.html", base=get_base, data=get_data)

    except HTTPError as http_err:

        print(f'HTTP error occurred: {http_err}')

    except Exception as err:

        print(f'Other error occurred: {err}')


if __name__ == '__main__':
    app.run(debug=True)
