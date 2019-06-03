from app import app, db
from flask import request, flash, redirect, url_for
import app.utils.ScriptModel as script_model
from app.models import TrainHistory, Asset
import os

@app.route('/train-model', methods=['GET', 'POST'])
def train_model():
    """ entraîne le modèle sur les donnèes existantes
        effectue une sauvegarde du model
    """
    if request.method == 'POST':
        epochs = request.form['epochs']
        time_step = request.form['time_steps']
        batch_size = request.form['batch_size']

        # Si un fichier .hd5 a été envoyé --> Ne pas entrainer le modèle -> passer à la phase de sauvegarde
        # check if the post request has the file part

        if request.files:
                file = request.files['filename']
                filename = 'import_' + file.filename
                file.save('app/models/' + filename)
                script_model.train_model(epochs=int(epochs), batch_size=int(batch_size), time_steps=int(time_step), filename=filename)
                os.remove('app/models/' + filename)
                flash('Le modèle à bien été ajouté')
        else:
                script_model.train_model(epochs=int(epochs), batch_size=int(batch_size), time_steps=int(time_step))
                flash('Le modèle à bien été entraîné')
        return redirect(url_for('index'))

    return 'Vous ne devriez pas être là.. Passez par le formulaire !'


@app.route('/delete-model-<int:model_id>')
def delete_model(model_id):
    """" Supprime un modèle précedement entrainé et ses prédictions"""

    train_history = TrainHistory.query.get(model_id)

    # suppression dans la base de données
    db.session.delete(train_history)
    db.session.commit()

    # suppression du fichier hd5
    os.remove('app/models/' + train_history.filename)

    flash(f"Nous avons exterminé le modèle n°{train_history.id} !")
    return redirect(url_for('index'))


@app.route('/get-predict-<int:asset_id>-<int:model_id>')
def get_predict(asset_id, model_id):
    """ Prédiction du modèle """

    # Récupération du  modèle entrainé, à utiliser pour la prédiction + l'indice qui doit être prédit
    train_history = TrainHistory.query.get(model_id)
    asset = Asset.query.get(asset_id)

    # récupère toutes les données
    data = script_model.get_data_on_db()
    stock = script_model.make_prediction(data, train_history, asset)

    flash(f'Prédiction effectuées pour {stock.asset.name} le {stock.date} :\n ASK :\n\topen :{stock.askopen} close{stock.askclose} low:{stock.asklow} high:{stock.askhigh} \n BID :\n\topen :{stock.bidopen} close{stock.bidclose} low:{stock.bidlow} high:{stock.bidhigh}')
    return redirect(url_for('index'))