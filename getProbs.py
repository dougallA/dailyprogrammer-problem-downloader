#!/usr/bin/env python

"""
I hardcoded absolute filenames into this script
so that it will work better from CRON.
This script downloads new problems from
reddit.com/r/dailyprogrammer and saves them into text files in
a directory.
At the moment it successfully looks for new problems, stores them in a new file
and saves the path of that file to a database. 
YOU MUST FILL IN DATABASE CREDENTIALS TO GET THIS TO WORK AND YOU MUST FILL IN THE 
VARIABLE 'directory'
"""

import MySQLdb, praw, os, re
from pprint import pprint


#Connect to mySql problem bank database.
db = MySQLdb.connect(host="ENTER YOUR HOST", 
                     user="ENTER USER",
                     passwd="ENTER PASSWORD",
                     db="ENTER DB")

db.set_character_set('utf8')

c = db.cursor()
c.execute('SET NAMES "utf8";')
c.execute('SET CHARACTER SET utf8;')
c.execute('SET character_set_connection=utf8;')

#Setting up reddit connection
user_agent = ("Programming challenge downloader by /u/-AMAC-")
r = praw.Reddit(user_agent = user_agent)
sub = r.get_subreddit('dailyprogrammer')

""" Assuming that text files of the problems will be stored in a subdirectory
  of the current called ProblemsFromReddit. Change this variable if you
  want to put it somewhere else. """
directory = "path/to/cwd/ProblemsFromReddit/"
if not os.path.isdir(directory):
    os.mkdir(directory)

def make_nice_pathname(original_pathname):
    """
    This method removes illegal characters from filenames.
    Recall that /r/dailyprogramer problems have titles of the form
    [4/30/2014] Challenge #160 Intermediate Part 2 - Damage Control
    Don't want date or challenge number so we remove those as well.
    """
    nice_pathname = re.sub(r'\[.*\]', r'', original_pathname).lstrip()
    nice_pathname = re.sub(r'[:?"<>|/\\*-]', r'', nice_pathname).lstrip()
    nice_pathname = re.sub(r'\\n', r'', nice_pathname).lstrip()
    return nice_pathname.lstrip()
    
    
def add_new_problems():
    """
    Looks through reddit.com/r/dailyprogrammer/new and if it finds a problem that is not in the database yet it will create a file
    for it and add the problem to the database. 
    """
    #new_posts is a generator object, that contains all of the new posts in the subreddit.
    new_posts = sub.get_new(limit="none")
    for post in new_posts:
        # Check to see if title already has entry in database. Recall that a mysql query 
        # returns the number of rows matching the query. 
        if c.execute("SELECT * FROM problems WHERE name = '%s' ;" %(MySQLdb.escape_string(post.title.encode('utf-8')))) == 0:
            #make a file containing problem
            filename = directory + '/' + make_nice_pathname(post.title).lstrip().rstrip() + ".txt"
            target = open(filename, "wb")
            target.write(post.selftext.encode('utf-8'))
            target.close()
            problemTitle = MySQLdb.escape_string(post.title.encode('utf-8'))
            fullPath = MySQLdb.escape_string(os.path.abspath(filename.encode('utf-8')))
            #Put problem in the database
            c.execute("INSERT into problems VALUES ('%s', '%s', NULL);" %(problemTitle, fullPath))
            db.commit()


add_new_problems()
