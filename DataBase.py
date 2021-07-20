import sqlite3 #api
from config import starter #starter money + xp
conn = sqlite3.connect('database.db') #db
cursor = conn.cursor() #cursor
def InsertValues(val1, val2):#needs for registration user
	cursor.execute(f'INSERT INTO main VALUES ("{val1}", {val2}, {starter["StarterMoney"]}, {starter["StarterXP"]})')
	conn.commit() #save
def InsertBankValues(id):
	cursor.execute(f'INSERT INTO bank VALUES (0, {id})')
	conn.commit() #creating and saving table
def CreateDB(name, val1, val2, val3, val4):#if not exists table
	cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{name}"(
	"{val1}"TEXT,
	"{val2}"INT,
	"{val3}"INT,
	"{val4}"INT)''')
	conn.commit() #creating and saving table
def CreateShopDB():#needs for shop
	cursor.execute(f'''CREATE TABLE IF NOT EXISTS "shop"(
	"title"TEXT,
	"id"INT,
	"roleID"INT,
	"cost"INT)''')
	conn.commit() #creating and saving table
def CreateBankDB():
	cursor.execute(f'''CREATE TABLE IF NOT EXISTS "bank"(
	"money"INT,
	"id"INT)''')
	conn.commit() #creating and saving table
def UpdateValue(val_name, new_val, id):
	for row in cursor.execute(f"SELECT {val_name} FROM main where id={id}"):
		new = row[0]+new_val
		cursor.execute(f"UPDATE main SET {val_name}={new} where id={id}")
		conn.commit()
		print("Updated value!")
def ReplaceShopValue(val_name, new_val):
		cursor.execute(f"UPDATE shop SET {val_name}={new_val}")
		conn.commit()
		print("Replaced value!")
def ReplaceShopString(val_name, new_val):
		cursor.execute(f'UPDATE shop SET {val_name}="{new_val}"')
		conn.commit()
def ReplaceValue(val_name, new_val, id):
		cursor.execute(f"UPDATE main SET {val_name}={new_val} where id={id}")
		conn.commit()
		print("Replaced value!")
def InsertShopValues(val1, val2, val3, val4):
	cursor.execute(f'INSERT INTO shop VALUES ("{val1}", {val2}, {val3}, {val4})')
	conn.commit()
def UpdateBankValue(new_val, id):
	for row in cursor.execute(f"SELECT money FROM bank where id={id}"):
		new = row[0]+new_val
		cursor.execute(f"UPDATE bank SET money={new} where id={id}")
		conn.commit()
		print("Updated value!")
def ReplaceBankValue(new_val, id):
	cursor.execute(f"UPDATE bank SET money={new_val} where id={id}")
	conn.commit()
	print("Replaced value!")
def DeleteAccount(id):#have bugs
	cursor.execute(f"DELETE FROM main WHERE id={id}")
	conn.commit()
	print("Account Deleted!")
def GetAllMembers():
	for row in cursor.execute(f"SELECT money,id,XP,name FROM main"):
		print(f"{row[3]}: {row[1]}, {row[0]}, {row[2]}")