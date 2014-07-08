DROP_CITIES = 'DROP TABLE IF EXISTS city'
DROP_MALE = 'DROP TABLE IF EXISTS male_name'
DROP_FEMALE = 'DROP TABLE IF EXISTS female_name'
DROP_LAST = 'DROP TABLE IF EXISTS last_name'
DROP_STREET = 'DROP TABLE IF EXISTS street'

CITIES = 'CREATE TABLE IF NOT EXISTS city(id INTEGER PRIMARY KEY AUTOINCREMENT, country_code VARCHAR(2),\
		zip_code VARCHAR(10), name VARCHAR(50), state VARCHAR(50), state_abbrev VARCHAR(2))'
MALE_NAMES = 'CREATE TABLE IF NOT EXISTS male_name(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50))'
FEMALE_NAMES = 'CREATE TABLE IF NOT EXISTS female_name(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50))'
LAST_NAMES = 'CREATE TABLE IF NOT EXISTS last_name(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(50))'
STREETS = 'CREATE TABLE IF NOT EXISTS street(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(100))'

ADD_CITY = '''INSERT INTO city(country_code, zip_code, name, state, state_abbrev) VALUES ('%s', '%s', '%s', '%s', '%s')'''
ADD_MALE = '''INSERT INTO male_name(name) VALUES ('%s')'''
ADD_FEMALE = '''INSERT INTO female_name(name) VALUES ('%s')'''
ADD_LAST = '''INSERT INTO last_name(name) VALUES ('%s')'''
ADD_STREET = '''INSERT INTO street(name) VALUES ('%s')'''

GET_STREET = '''SELECT name FROM street WHERE id = %s'''
GET_CITY = '''SELECT country_code, zip_code, name, state, state_abbrev FROM city WHERE id = %s'''
GET_MALE = '''SELECT name FROM male_name WHERE id = %s'''
GET_FEMALE = '''SELECT name FROM female_name WHERE id = %s'''
GET_LAST = '''SELECT name from last_name WHERE id = %s'''

COUNT_STREET = '''SELECT COUNT(*) FROM street'''
COUNT_CITY = '''SELECT COUNT(*) FROM city'''
COUNT_MALE = '''SELECT COUNT(*) FROM male_name'''
COUNT_FEMALE = '''SELECT COUNT(*) FROM female_name'''
COUNT_LAST = '''SELECT COUNT(*) FROM last_name'''

STREET_SUF = ['RD','ST','BLVD','DR','AVE']
EMAIL_SUF = ['gmail.com','hotmail.com','somecompany.com','zoho.com','aol.com','msn.com','yahoo.com','inbox.com']
