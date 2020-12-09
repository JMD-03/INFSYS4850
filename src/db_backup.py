#!/usr/local/bin/python3

"""
Will backup all the databases listed, will put files in same DIR as script'
To run: $ python db_backup.py
"""

import configparser
import os
import time
import getpass

HOST='localhost'
PORT='3306'
DB_USER='dbadminTEST'
DB_PASS='dbadminTEST'
database='djangoproject'


if os.path.exists("djangoproject.sql"):
  os.remove("djangoproject.sql")
else:
  print("The file does not exist")

def get_dump(database):
    filestamp = time.strftime('%Y-%m-%d-%I')
    # D:/xampp/mysql/bin/mysqldump for xamp windows
    os.popen(r"C:\Program Files\MySQL\MySQL\ Server\ 8.0\bin\mysqldump --no-create-info -h %s -P %s -u %s -p%s %s > %s.sql" % (HOST,PORT,DB_USER,DB_PASS,database,database))
  #creating mysqldump file of database using admin user  
    print("\n|| Database dumped to "+database+"_"+database+".sql || ")

get_dump(database)
#if __name__=="__main__":
    #for database in databases:
       # get_dump(database)