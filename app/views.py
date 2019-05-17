from app import app
from flask import render_template, request
import fxcmpy
from SECRET import *


@app.route('/')
def index():
    # connection API fxcmpy
    con_fxcmpy = fxcmpy.fxcmpy(ACCESS_TOKEN, server='demo')

    # list of instruments, generate choice for get data in view
    instruments = con_fxcmpy.get_instruments()
    return render_template('index.html', instruments=instruments)


@app.route('/get-data-<instrument>', methods=['GET'])
def get_data(instrument):
    """
    Stock data for one instrument in csv
    :param instrument: name of instrument for research
    :return: json of data for instrument
    """
    # connection API fxcmpy
    con_fxcmpy = fxcmpy.fxcmpy(ACCESS_TOKEN, server='demo')

    # search params GET for get candle
    params_candle = request.args.to_dict()
    if request.args.get('number'):
        params_candle['number'] = int(params_candle['number'])

    # get data from api, use GET params
    data = con_fxcmpy.get_candles(instrument, params_candle)

    # stock data in csv
    filename = 'bourse_' + instrument + '.csv'
    data.to_csv('app/data/' + filename)

    return data.to_json()
