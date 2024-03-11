import mysql.connector

dataBase = mysql.connector.connect(
	host = 'localhost',
	user = 'root',
	passwd = 'IAmADragon',
	database= 'pharmacy_system',

	)

cursorObject = dataBase.cursor()



print("all done!")	