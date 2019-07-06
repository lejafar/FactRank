#!/usr/bin/env python3
"""
Preprocess all sentences in DB

NOTE: This script was only used in order to speed
      up the hyperparameter optimization
"""

# SOME USEFULL COLORS
class bc:
    MAG = '\033[1;35m'
    YEL = '\033[0;33m'
    CYA = '\033[0;36m'
    END = '\033[0m'

# PROVIDE FEEDBACK
print(bc.YEL + "● LOADING DEPENDENCIES ... " + bc.END)

# IMPORT DEPENDENCIES
import MySQLdb
import sys
from tqdm import *
from importlib import reload
sys.path.insert(0, '..')  # Add dir to import featureExtractor

# IMPORT IVO'S EXTRACTOR
from extractor import Extractor

# IMPORT DB CREDENTIALS AND CONNECT
from credentials import *
db = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DB_NAME)
cur = db.cursor()

# MAKE SURE TERMINAL AND CONNECTION ENCODING USES UTF-8
reload(sys)
# Since the default on Python 3 is UTF-8 already,
# there is no point in leaving those statements in.
# sys.setdefaultencoding('utf8')
cur.execute("SET NAMES 'utf8mb4';")
cur.execute("SET CHARACTER SET 'utf8mb4';")
cur.execute("SET character_set_connection='utf8mb4';")

# PROVIDE FEEDBACK
print(bc.YEL + "● CONNECTING TO DATABASE, RETRIEVING SENTENCES ... ")

# RETRIEVE ALL SENTENCES THAT HAVE BEEN CLASSIFIED SO FAR
cur.execute("""SELECT id, content
			   FROM sentences
			   WHERE id
			   IN (SELECT sentence_id
			       FROM classification_s
				   WHERE 1)
			   ORDER BY id
			   ASC""")
sentence_rows = cur.fetchall()
sentence_rows_len = len(sentence_rows)

# PROVIDE FEEDBACK
print("● STARTED PARSING SENTENCES AND PUSHING TO DATABASE" + bc.CYA)

counter = 0
for sentence_row in tqdm(sentence_rows, ncols=100):
    try:
        sentence_id = sentence_row[0]
        sentence = sentence_row[1]
        extractorObject = Extractor(sentence)
        sentence_features = (sentence_id,
                             extractorObject.length(),
                             extractorObject.polarity(),
                             extractorObject.subjectivity(),
                             extractorObject.lemmataSentence(),
                             extractorObject.posTagSentence(),
                             extractorObject.lemmataPosTagSentence(),
                             )
        # Insert and update when sentence is already present.
        cur.execute("""INSERT INTO features_s_plus
                    (S_ID, LENGTH, POL, SUBJ, LEMMA_SENT, POS_SENT, LEMMA_POS)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                    ON DUPLICATE KEY UPDATE
                    `S_ID`=%s,
                    `LENGTH`=%s,
                    `POL`=%s,
                    `SUBJ`=%s,
                    `LEMMA_SENT`=%s,
                    `POS_SENT`=%s,
                    `LEMMA_POS`=%s
                    """, sentence_features*2
                    )
        # Notice the values (sentence_id, ... ) were passed to the function 'execute'
        # as a second argument, not as part of the first argument through string
        # interpolation. MySQL will properly quote the arguments for us.
        db.commit()
        counter += 1

    except:
        # PROVIDE FEEDBACK
        print("\n" + bc.MAG + "● AN ERROR OCCURED. STOPPING THE PROGRAM.")
        print("● CURRENT SENTENCE: " + sentence)
        print("● ERROR: ", sys.exc_info()[0] + bc.END)
        break

db.close
# PROVIDE FEEDBACK
print(bc.YEL + "● CLOSED CONNECTION TO DATABASE" + bc.END)
print(bc.YEL + "● SUCCESFULLY PUSHED " + str(counter) + " SENTENCES UPSTREAM" + bc.END)
