from app import app
from flask import request
from .utils import utilsDatabase
from app.utils.fxcmManager import connect_fxcm
from app.models import StockHistory
import json
import jsonify

@app.route('/get-data-<instrument>', methods=['GET'])
def get_data(instrument):
    """
    Stock data for one instrument in csv
    :param instrument: name of instrument for research
    :return: json of data for instrument
    """
    # get asset or create
    asset = utilsDatabase.get_asset(instrument)

    # connection API fxcmpy
    con_fxcmpy = connect_fxcm()

    # search params GET for get candle
    params_candle = request.args.to_dict()
    if request.args.get('number'):
        params_candle['number'] = int(params_candle['number'])

    # get data from api, use GET params
    data = con_fxcmpy.get_candles(instrument, **params_candle)
    data['asset_id'] = asset.id
    con_fxcmpy.close()

    data = utilsDatabase.actualize_data(data)

    # stock data in csv
    filename = 'bourse_' + instrument + '.csv'
    data.to_csv('app/data/' + filename)

    return data.to_json()


@app.route('/data-stock-history')
def get_stock_history():
    data = StockHistory.query.all()
    result = [d.serialize() for d in data]
    print(data)
    return json.dumps(result,)