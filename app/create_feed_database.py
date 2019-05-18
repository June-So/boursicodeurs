import mysql.connector
import pandas as pd
from sqlalchemy import create_engine
import fxcmpy
from SECRET import *

con = fxcmpy.fxcmpy(FXCMY_ACCESS_TOKEN, server='real')

df = con.get_candles('GER30', period='H1', number=10000)
#df.reset_index()
engine = create_engine('mysql+mysqldb://{user}:{password}@{server}:{port}/{database}?charset=utf8mb4'.format(**DATABASE))

#df.to_sql(name='assets_tables',con=engine , if_exists='append', index=False)

# Création et remplissage de la table assets_tables avec le dataframe des données.
#df.to_sql(name='assets_tables', con=engine, if_exists='replace')


#connection = engine.connect()
table_pred = engine.execute("""CREATE TABLE IF NOT EXISTS assets_forecast (
  id INT NOT NULL AUTO_INCREMENT,
  `date` datetime,
  bidopen_forcast DOUBLE,
  bidclose_forcast DOUBLE,
  bidhigh_forcast DOUBLE,
  bidlow_forcast DOUBLE,
  askopen_forcast DOUBLE,
  askclose_forcast DOUBLE,
  askhigh_forcast DOUBLE,
  asklow_forcast DOUBLE,
  tickqty_forcast BIGINT(20),
  PRIMARY KEY (id),
  CONSTRAINT fk_assets_forecast FOREIGN KEY (`date`)
  REFERENCES assets_tables (`date`) ON DELETE CASCADE
);""")
table_pred.close()
