import mysql.connector
import user

import requests
from bs4 import BeautifulSoup

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="PropertyValueMonitor"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM users")

dbUsers = mycursor.fetchall()

for dbUser in dbUsers:
	currentUser = user.User(dbUser[0], dbUser[1], dbUser[2], str(dbUser[3]), dbUser[4])
	
	print(currentUser.propertyCode)
	
	newValue = currentUser.checkPropertyValue()
		
	if newValue != None:
		mycursor.execute(f"UPDATE users SET propertyValue = {newValue} where id = {currentUser.userid}")
		mydb.commit()
