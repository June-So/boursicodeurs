from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField


class TrainForm(FlaskForm):
    epochs = IntegerField('Epochs')
    batch_size = IntegerField('Batch size')
    time_steps = IntegerField('Time steps')
    submit = SubmitField('Entraîner le modèle')