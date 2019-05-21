from app import app, db
from flask import render_template, request, flash, redirect, url_for
import fxcmpy
import pandas as pd
from SECRET import *
from sqlalchemy import create_engine
from .utils import utilsDatabase
import app.ScriptModel as script_model
from app.forms import TrainForm


@app.route('/')
def index():
    # formulaire d'entrainement
    form = TrainForm()

    # connection API fxcmpy
    con_fxcmpy = fxcmpy.fxcmpy(FXCMY_ACCESS_TOKEN, server='demo')

    # list of instruments, generate choice for get data in view
    instruments = con_fxcmpy.get_instruments()
    return render_template('index.html', instruments=instruments, trainform=form)


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
    con_fxcmpy = fxcmpy.fxcmpy(FXCMY_ACCESS_TOKEN, server='demo')

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


@app.route('/train-model', methods=['GET', 'POST'])
def train_model():
    """ entraîne le modèle sur les donnèes existantes
        effectue une sauvegarde du model
    """
    if request.method == 'POST':
        epochs = request.form['epochs']
        time_step = request.form['time_steps']
        batch_size = request.form['batch_size']

        model = script_model.train_model(epochs=int(epochs), batch_size= int(batch_size), time_steps=int(time_step))
        flash('Le modèle à bien été entraîné')
        return redirect(url_for('index'))


@app.route('/get-predict')
def get_predict():
    """ Prédiction du modèle """
    model_name = 'modelDAX_Hour0.hdf5'
    # récupère toutes les données
    data = script_model.get_data_on_db()

    inputs_pred_ds, real_input_ds = script_model.make_prediction(data, model_name)

    print(zip(inputs_pred_ds, real_input_ds))
    flash('Prédiction effectuées')
    return redirect(url_for('index'))
