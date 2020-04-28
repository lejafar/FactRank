from pattern.nl import sentiment
from pattern.nl import tag, parse, ngrams, tokenize, pprint
from pattern.server import App
import MySQLdb
from credentials import *
import sys

COLUMNNAMES = ["CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS", "LS", "MD", "NN", "NNS", "NNP", "NNPS", "PDT", "POS", "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "SYM", "TO", "UH", "VB", "VBZ", "VBP", "VBD", "VBN", "VBG", "WDT", "WP", "WP$", "WRB", "POINT", "COMMA","COLON","lBRACKET", "rBRACKET"]

db = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DB_NAME)
cur = db.cursor()

# MAKE SURE TERMINAL AND CONNECTION ENCODING USES UTF-8
reload(sys)
sys.setdefaultencoding('utf8')
cur.execute("SET NAMES 'utf8mb4';")
cur.execute("SET CHARACTER SET 'utf8mb4';")
cur.execute("SET character_set_connection='utf8mb4';")
CC = "CC"
for i in range(36, len(postags)):
	query = "ALTER TABLE features_s ADD POS_%s INT(100)" % (postags[i])
	cur.execute(query)
	db.commit()
	
db.close
