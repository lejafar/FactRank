import MySQLdb
import sys,textwrap
from tools.credentials import *
from parser import load_model, prepForPred

db = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DB_NAME)

cur = db.cursor()
# MAKE SURE TERMINAL AND CONNECTION ENCODING USES UTF-8
cur.execute("SET NAMES 'utf8mb4';")
cur.execute("SET CHARACTER SET 'utf8mb4';")
cur.execute("SET character_set_connection='utf8mb4';")

cur.execute('SELECT id, content FROM sentences')
results = cur.fetchall()

cur.execute('DELETE FROM `sentence_predictions` WHERE model_version = "v1.0.0"')
db.commit()
cur.execute('DELETE FROM `sentence_predictions` WHERE model_version = "v0.1.1-beta"')
db.commit()

old_model, _= load_model(name='trained_model.pkl')
new_model, _= load_model(name='trained_model_1.0.pkl')

for s_id, content in results:
    # run old model
    checkworthyness = old_model.predict_proba(prepForPred([content]))[0][1]
    print(s_id, content, checkworthyness)
    cur.execute('''INSERT INTO sentence_predictions (sentence_id, label, probability, model_version) VALUES (%s, "FR", %s, "v0.1.1-beta")''', (s_id, round(checkworthyness, 3)))
    db.commit()
    # run new model (old model with new data)
    checkworthyness = new_model.predict_proba(prepForPred([content]))[0][1]
    print(s_id, content, checkworthyness)
    cur.execute('''INSERT INTO sentence_predictions (sentence_id, label, probability, model_version) VALUES (%s, "FR", %s, "v1.0.0")''', (s_id, round(checkworthyness, 3)))
    db.commit()

