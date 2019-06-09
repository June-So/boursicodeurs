from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, StringField, SelectField
import os

class TrainForm(FlaskForm):
    epochs = IntegerField('Epochs')
    batch_size = IntegerField('Batch size')
    time_steps = IntegerField('Time steps')
    submit = SubmitField('Entraîner le modèle')


class BotForm(FlaskForm):
    time_trade = IntegerField('time trade')
    model_name = StringField('nom model')
    submit = SubmitField("Lancer le botTrader")


class BotDqlForm(FlaskForm):
    time_trade = IntegerField('time trade')
    model_name = StringField('nom model')
    FILENAMES = [(name, name) for i, name in enumerate(os.listdir('app/bot/qTrader/models/'))]
    model_name = SelectField(u'nom model', choices=FILENAMES)
    submit = SubmitField("Lancer le DqlTrader")