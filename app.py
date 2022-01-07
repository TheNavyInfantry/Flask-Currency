import requests, json
from requests.exceptions import HTTPError
from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/TRY")
        data = r.json()
        # data_dumps = json.dumps(data, indent=3)
        data_get_base = data.get("base")
        data_get_rates = data.get("rates")

        return render_template("index.html", base=data_get_base, rates=data_get_rates)

    except HTTPError as http_err:

        print(f'HTTP error occurred: {http_err}')

    except Exception as err:

        print(f'Other error occurred: {err}')


if __name__ == '__main__':
    app.run()
