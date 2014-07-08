__author__ = 'Brandon Harmon'
import sqlite3 as lite
import Statics, random, re, sys, argparse

CITIES_TXT = 'lists/US.txt'
MALE_TXT = 'lists/dist.male.first'
FEMALE_TXT = 'lists/dist.female.first'
LAST_TXT = 'lists/dist.all.last'
STREET_TXT = 'lists/allstreets.txt'

DESCRIPTION = '''
This program generates dictionary objects that can be used to represent common information
 needed to populate user/account data.\n
This information is populated through the use of random numbers for any numeric value, and
information from the census to populate names. Other information is included including
accurate street names, and cities that are associated with the correct city and zip code.

Initial Usage:
Download the program, the initial run of the program must load the data from the text files
 to either reupload or initialize the database call this program with the '-r' argument.\n

To output a random sample to the standard output, run this progrma with the '-s <# of samples>'
'''


class PersonGenerator():
	con = None
	max_city = -1
	max_male = -1
	max_female = -1
	max_last = -1
	max_street = -1
	
	def __init__(self, fresh_load):
		self.con = lite.connect('random_details.sql')
		if fresh_load:
			self.clean()
			self.setTables()
			self.loadTables()
		self.setCounts()
	
	def clean(self):
		cur = self.con.cursor()
		cur.execute(Statics.DROP_CITIES)
		cur.execute(Statics.DROP_MALE)
		cur.execute(Statics.DROP_FEMALE)
		cur.execute(Statics.DROP_LAST)
		cur.execute(Statics.DROP_STREET)
		self.con.commit()

	def setTables(self):
		print 'Creating Tables...'
		cur = self.con.cursor()
		cur.execute(Statics.CITIES)
		cur.execute(Statics.MALE_NAMES)
		cur.execute(Statics.FEMALE_NAMES)
		cur.execute(Statics.LAST_NAMES)
		cur.execute(Statics.STREETS)
		self.con.commit()
		print 'Tables Created'

	def loadTables(self):
		print 'Loading data...'
		self.loadCities()
		self.loadNames()
		self.loadStreets()
		print 'Data is loaded'

	def loadCities(self):
		cur = self.con.cursor()
		f = open(CITIES_TXT,'r')

		for line in f:
			split = re.split(r'\t+',line)
			safe = []
			for word in split:
				safe.append(word.replace("'",""))
			cur.execute(Statics.ADD_CITY % (safe[0],safe[1],safe[2],safe[3],safe[4]))

		self.con.commit()

	def loadNames(self):
		cur = self.con.cursor()
		f = open(MALE_TXT, 'r')
		for line in f:
			cur.execute(Statics.ADD_MALE % (line.split(' ',1)[0]))

		f = open(FEMALE_TXT,'r')
		for line in f:
			cur.execute(Statics.ADD_FEMALE % (line.split(' ',1)[0]))

		f = open(LAST_TXT,'r')
		for line in f:
			cur.execute(Statics.ADD_LAST % (line.split(' ',1)[0]))

		self.con.commit()

	def loadStreets(self):
		cur = self.con.cursor()
		f = open(STREET_TXT,'r')
		for line in f:
			cur.execute(Statics.ADD_STREET % line)
		self.con.commit()

	def setCounts(self):
		cur = self.con.cursor()
		self.max_street = cur.execute(Statics.COUNT_STREET).fetchone()[0]
		self.max_city = cur.execute(Statics.COUNT_CITY).fetchone()[0]
		self.max_male = cur.execute(Statics.COUNT_MALE).fetchone()[0]
		self.max_female = cur.execute(Statics.COUNT_FEMALE).fetchone()[0]
		self.max_last = cur.execute(Statics.COUNT_LAST).fetchone()[0]

		print '''\nLoaded...\n %s streets \n %s cities \n %s male names \n %s female names \n %s last names''' % \
			(self.max_street, self.max_city, self.max_male, self.max_female, self.max_last)

	def getAddress(self):
		cur = self.con.cursor()
		street =  cur.execute(Statics.GET_STREET % random.randint(1,self.max_street)).fetchone()[0]	
		house_num = random.randint(1,9999)
		return str(house_num) + ' ' + street + ' ' + random.choice(Statics.STREET_SUF)

	def getPhoneNumber(self):
		return  str(random.randint(100,999))+'-'+str(random.randint(100,999))+'-'+str(random.randint(1000,9999))

	def getEmail(self, prefix = ""):
		return prefix + str(random.randint(1000,9999)) + '@' + random.choice(Statics.EMAIL_SUF)

	def getRandomMale(self):
		cur = self.con.cursor()
		rand = random.randint(1,self.max_male)
		return cur.execute(Statics.GET_MALE % rand ).fetchone()[0]
	
	def getRandomFemale(self):
                cur = self.con.cursor()
	  	rand = random.randint(1,self.max_female)
               	return cur.execute(Statics.GET_FEMALE % rand ).fetchone()[0]
	
	def getRandom(self):
		cur = self.con.cursor()
		#City includes state and other information
		city =  cur.execute(Statics.GET_CITY % random.randint(1,self.max_city)).fetchone()
		b_city = cur.execute(Statics.GET_CITY % random.randint(1,self.max_city)).fetchone()
		last =  cur.execute(Statics.GET_LAST % random.randint(1,self.max_last)).fetchone()[0]
		is_male = (random.randint(1,100) % 2 == 0)

		person = { 
			'first_name' : self.getRandomMale() if is_male else self.getRandomFemale(), \
			'middle_name' : self.getRandomMale() if is_male else self.getRandomFemale(), \
			'last_name' : last, \
			'password' : 'test',\
			'address' : self.getAddress(),\
			'phone' : self.getPhoneNumber(),\
			'alternate_phone' : self.getPhoneNumber(),\
			'country' : city[0],\
			'is_male' : is_male,\
			'zip' : city[1],\
		 	'city' : city[2],\
			'state' : city[3],\
			'state_abbrev' : city[4],\
			'email' : self.getEmail(prefix = last),\
			'alternate_email' : self.getEmail(prefix = city[2]),\
			'billing_address' : self.getAddress(),\
			'billing_country' : b_city[0],\
			'billing_zip':b_city[1],\
			'billing_city':b_city[2],\
			'billing_state':b_city[3],\
			'billing_state_abbrev':b_city[4],\
			'billing_cc_no':random.getrandbits(128),\
			'billing_csv':random.randint(100,999),\
			'billing_exp_month':random.randint(1,13),\
			'billing_exp_year':14+random.randint(0,5)}
		return person

def main(args):
	handler = PersonGenerator(args.reload)
	if args.sample > -1:
		for num in range(0,args.sample):
			print handler.getRandom()

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('-r','--reload', action="store_true", \
	help='Reloads the data from text files. \n Use this option if no sql file exists')
parser.add_argument('-s','--sample', type=int, help='Outputs provided number of person objects to std out')
parser.set_defaults(reload=False)
parser.set_defaults(sample=-1)
args = parser.parse_args()

if __name__ == '__main__':
	main(args)
