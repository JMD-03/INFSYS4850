
import configparser
import os
import time
import getpass

HOST='localhost'
PORT='3306'
DB_USER='dbadminTEST'
DB_PASS='dbadminTEST'
database='djangoproject'

fo = open("djangoproject.sql")
print ("Name of the file: ", fo.name)

#os.popen("D:\\mysql-8.0.22-winx64\\mysql-8.0.22-winx64\\bin\\mysqldump.exe -h %s -P %s -u %s -p%s %s < D:\\INFSYS4850-nick\\src\\%s.sql" % (HOST,PORT,DB_USER,DB_PASS,database,database))
os.popen("D:\\mysql-8.0.22-winx64\\mysql-8.0.22-winx64\\bin\\mysqldump.exe -h localhost -P 3306 -u dbadminTEST -pdbadminTEST djangoproject < D:\\INFSYS4850-nick\\src\\djangoproject.sql")
#print("\n|| Database restored frocm "+database+".sql || ")