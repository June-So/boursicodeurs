# coding: utf-8
from app import db


class StockPrediction(db.Model):
    __tablename__ = 'stock_prediction'

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    date = db.Column(db.DateTime, index=True)
    bidopen = db.Column(db.Float(asdecimal=True))
    bidclose = db.Column(db.Float(asdecimal=True))
    bidhigh = db.Column(db.Float(asdecimal=True))
    bidlow = db.Column(db.Float(asdecimal=True))
    askopen = db.Column(db.Float(asdecimal=True))
    askclose = db.Column(db.Float(asdecimal=True))
    askhigh = db.Column(db.Float(asdecimal=True))
    asklow = db.Column(db.Float(asdecimal=True))
    tickqty = db.Column(db.BigInteger)


class StockHystory(db.Model):
    __tablename__ = 'stock_history'

    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('asset.id'), nullable=False)
    date = db.Column(db.DateTime, index=True)
    bidopen = db.Column(db.Float(asdecimal=True))
    bidclose = db.Column(db.Float(asdecimal=True))
    bidhigh = db.Column(db.Float(asdecimal=True))
    bidlow = db.Column(db.Float(asdecimal=True))
    askopen = db.Column(db.Float(asdecimal=True))
    askclose = db.Column(db.Float(asdecimal=True))
    askhigh = db.Column(db.Float(asdecimal=True))
    asklow = db.Column(db.Float(asdecimal=True))
    tickqty = db.Column(db.BigInteger)


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    stock_predictions = db.relationship('StockPrediction', backref='asset', cascade="all,delete", lazy=True)
    stock_historys = db.relationship('StockHystory', backref='asset', cascade="all,delete", lazy=True)

    def __init__(self, name):
        self.name = name


class TrainHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    epochs = db.Column(db.Integer)
    batch_size = db.Column(db.Integer)
    time_steps = db.Column(db.Integer)
    total_data = db.Column(db.Integer)
    score_train = db.Column(db.Float(asdecimal=True))
    score_test = db.Column(db.Float(asdecimal=True))
    filename = db.Column(db.String(255))


