This program is a script that downloads new problems from the programming challenge website www.reddit.com/r/dailyprogrammer
It saves problems as text files and maintains a list of challenges downloaded and the paths to the files in a MySQL database. 
I run this script using a cron job a few times a week so that my collection of programming challenges grows automatically.

Note that in getProbs.py you are responsible for giving the program database information and you are also responsible for setting the 'directory' variable to be the directory where you want the problems to be saved. 

Note that this requires the MySQLdb and the praw modules to be installed. 
