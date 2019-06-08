from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, TextField


class TrainForm(FlaskForm):
    epochs = IntegerField('Epochs')
    batch_size = IntegerField('Batch size')
    time_steps = IntegerField('Time steps')
    submit = SubmitField('Entraîner le modèle')


class BotForm(FlaskForm):
    time_trade = IntegerField('time trade')
    model_name = TextField('nom model')
    submit = SubmitField("Lancer le botTrader")


class BotDqlForm(FlaskForm):
    time_trade = IntegerField('time trade')
    model_name = TextField('nom model')
    submit = SubmitField("Lancer le DqlTrader")