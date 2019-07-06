#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Manual classifier for sentences from the tweet subset
"""
__author__ = "Brecht Laperre"
__copyright__ = "Copyright 2017, Knowledge and the Web Project"
__credits__ = ["Brecht Laperre", "Ivo Merchiers", "Rafael Hautekiet"]
__version__ = "1.0.0"
__maintainer__ = "Brecht Laperre"
__email__ = "brecht.laperre@student.kuleuven.be"
__status__ = "Development"

import MySQLdb
import sys,textwrap
from credentials import *

# wrapper to intend sentences
preferredWidth = 90
normalwrapper = textwrap.TextWrapper(initial_indent="● ", width=preferredWidth,subsequent_indent='  ')
previouswrapper = textwrap.TextWrapper(initial_indent="  ⎌ ", width=preferredWidth,subsequent_indent='    ')

class bcolors:
    MAGENTA = '\033[1;35m'
    YELLOW = '\033[0;33m'
    CYAN = '\033[0;36m'
    ENDC = '\033[0m'

# SET TESTNUMBER HERE
try:
	testnum = sys.argv[1]
except:
	print("Error, not enough input arguments. Did you specify a test number?")
	print("Corrrect use: python classifier.py <testnum>")
	exit()

# Source of _Getch: http://code.activestate.com/recipes/134892-getch-like-unbuffered-character-reading-from-stdin/

class _Getch:
    """
    Gets a single character from standard input.  Does not echo to
    the screen.
    """

    def __init__(self):
        try:
            self.impl = _GetchUnix()  # _GetchWindows()
        except ImportError:
            try:
                self.impl = _GetchMacCarbon()
            except(AttributeError, ImportError):
                self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty
        import sys

    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


class _GetchMacCarbon:
    """
    A function which returns the current ASCII key that is down;
    if no ASCII key is down, the null string is returned.  The
    page http://www.mactech.com/macintosh-c/chap02-1.html was
    very helpful in figuring out how to do this.
    """

    def __init__(self):
        import Carbon
        Carbon.Evt  # see if it has this (in Unix, it doesn't)

    def __call__(self):
        import Carbon
        if Carbon.Evt.EventAvail(0x0008)[0] == 0:  # 0x0008 is the keyDownMask
            return ''
        else:
            #
            # The event contains the following info:
            # (what,msg,when,where,mod)=Carbon.Evt.GetNextEvent(0x0008)[1]
            #
            # The message (msg) contains the ASCII char which is
            # extracted with the 0x000000FF charCodeMask; this
            # number is converted to an ASCII character with chr() and
            # returned
            #
            (what, msg, when, where, mod) = Carbon.Evt.GetNextEvent(0x0008)[1]
            return chr(msg & 0x000000FF)


db = MySQLdb.connect(host=HOST, user=USER, passwd=PASSWD, db=DB_NAME)

cur = db.cursor()
# MAKE SURE TERMINAL AND CONNECTION ENCODING USES UTF-8
reload(sys)
sys.setdefaultencoding('utf8')
cur.execute("SET NAMES 'utf8mb4';")
cur.execute("SET CHARACTER SET 'utf8mb4';")
cur.execute("SET character_set_connection='utf8mb4';")

getch = _Getch()

# INCREASE FANCYNESS OF OUTPUT
def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()

def fetchNext(id):
	cur.execute('SELECT sentence_id, subset, id FROM sentence_subsets WHERE  subset = %s AND sentence_subsets.id = (SELECT min(id) FROM sentence_subsets WHERE id > %s) LIMIT 1 ', [
	            "sent" + str(int(testnum) - 1), id])
	res = cur.fetchone()
	if cur.rowcount == 0:
		return 0
	return res;


def fetchPrev(id):
	cur.execute('SELECT sentence_id, subset, id FROM sentence_subsets WHERE  subset = %s AND sentence_subsets.id = (SELECT max(id) FROM sentence_subsets WHERE id < %s) LIMIT 1 ', [
	            "sent" + str(int(testnum) - 1), id])
	res = cur.fetchone()
	if cur.rowcount == 0:
		return 0
	return res;


# Ask the contributor ID, I assume we are the contributors.
cur.execute('SELECT id, name FROM contributors')
contr = cur.fetchall()
for c in contr:
		print "userid: " +str(c[0]) + ", username: " + str(c[1])
gotID = False

# Should ask name instead of idnumber, but doing it like this for now.
while not gotID:
	cid = raw_input("Please enter your corresponding id: ")
	for c in contr:
		if str(c[0]) == cid:
			gotID = True
			break
	if not gotID:
		print("Not a valid id.")

# Retrieve tweet info from tweetsubset

# INIT: Use the subset_id to run over all things
min_id = 1
cur.execute('SELECT sentence_id, subset, id FROM sentence_subsets WHERE subset = %s AND sentence_subsets.id =  (SELECT min(id) FROM sentence_subsets WHERE subset = %s) LIMIT 1', [
            "sent" + str(int(testnum) - 1), "sent" + str(int(testnum) - 1)])
s = cur.fetchone()
ids = str(s[2])

print(bcolors.YELLOW + "Skip to first unclassified sentence (y)? Or start from beginning (n)?" + bcolors.ENDC)
sk = getch.impl()
skipping = False
if sk == "y":
	skipping = True
	print("Skipping to first unclassified sentence...")
print("")
notStopping = True
fetch = -1  # initialisation value
previous_info = "None"
count = 0
while notStopping:
	if fetch == 1:
		s = fetchNext(str(s[2]))
		count = count + 1
	elif fetch == 0:
		s = fetchPrev(str(s[2]))
		count = count - 1
	if s == 0:
		notStopping = False
		print("No more sentences. Stopping program.")
		break
	if count % 10 == 0:
		if skipping:
			restart_line()
			sys.stdout.flush()
			sys.stdout.write(bcolors.CYAN  + "Skipping " + str(count) + " sentences ..." + bcolors.ENDC)
		if not skipping:
			print("\n"+bcolors.CYAN + "Already " + str(count) + " sentences classified 🥂 " + bcolors.ENDC)
			print(bcolors.CYAN +"j: CFS | k: UFS | l: NFS | i: US | u: previous | o: skip | s: stop | p: farSkip"+ bcolors.ENDC+"\n")
	sentid = str(s[0])
	exists = False
	AlreadyClassified = False
	info = "None"
	if cur.execute("SELECT (1) FROM classification_s WHERE classification_s.sentence_id = %s LIMIT 1", [sentid]):
		exists = True
	if exists:
		cur.execute(
		    "SELECT category, contributor_id FROM classification_s WHERE classification_s.sentence_id = %s", [sentid])
		existingclass = cur.fetchall()
		# Initialise info
		contributors = ""
		classes = ""
		info = "None"
		for cl in existingclass:
			if str(cl[1]) == cid:
				info = 'You already classified this sentence as: ' + bcolors.YELLOW + str(cl[0] + bcolors.ENDC)
				if skipping:
					AlreadyClassified = True
				break
			cur.execute("SELECT name FROM contributors WHERE id = %s", [cl[1]])
			contributors = contributors + cur.fetchone()[0] + ", "
			classes = classes + cl[0] + ", "
		# In the case the sentence was already classified by something we skip further to the next sentence.
		if AlreadyClassified:
			fetch = 1
			continue
		# else:
		#	skipping = False # This statement is never used?
		# print('Following tweet has already been classified by {0} giving it the classification {1}'.format(contributors, classes))
	cur.execute("SELECT content FROM sentences WHERE sentences.id = %s", [sentid])
	cont = cur.fetchall()
	if skipping:
		print("\n"+bcolors.CYAN +"j: CFS | k: UFS | l: NFS | i: US | u: previous | o: skip | s: stop | p: farSkip"+ bcolors.ENDC+"\n")
		skipping = False # Stop skipping when sentence has been printed again
	sentence = normalwrapper.fill(cont[0][0])
	if info != "None":
		sentence = previouswrapper.fill(cont[0][0])
	if previous_info != "None" and info == "None" or previous_info == "None" and info != "None":
		# Add break between previous and normal sections
		sentence = "\n"+sentence
	print(bcolors.MAGENTA+sentence + bcolors.ENDC)
	if info != "None":
		print("    ⌙ " + str(info) )
	previous_info = info
	while True:
		i = getch.impl()
		if i == "j":
			cl = "CFS"
			break
		elif i == "k":
			cl = "UFS"
			break
		elif i == "l":
			cl = "NFS"
			break
		elif i == "i":
			cl = "US"
			break
		elif i == "o":
			print(" skipped")
			cl = "SKIP"
			fetch = 1
			break
		elif i == "u":
			fetch = 0
			cl = "SKIP"
			break
		elif i == "s":
			print("Stopping program...")
			cl = "stop"
			break
		elif i == "p":
			print("Skipping to next unclassified sententce.")
			skipping = True
			cl = "SKIP"
			fetch = 1
			break
		else:
			print("Not a valid input, please try again.")
	if cl == "SKIP":
		continue
	elif cl == "stop":
		break
	elif info == "None":
		fetch = 1
		print("  ⌙ Classified as: " + bcolors.YELLOW + cl + bcolors.ENDC)
		cur.execute('''INSERT INTO classification_s (sentence_id, category, contributor_id, last_updated, test) VALUES (%s, %s, %s, CURRENT_TIMESTAMP, %s)''', (sentid, cl, cid, testnum))
		db.commit()
	else:
		fetch = 1
		print("      "+bcolors.YELLOW + "→ New classification: " + cl + bcolors.ENDC)
		cur.execute('''UPDATE classification_s SET category=%s, last_updated=CURRENT_TIMESTAMP WHERE (sentence_id=%s AND contributor_id=%s AND test=%s)''', [cl, sentid, cid, testnum])
		db.commit()
