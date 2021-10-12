class User:
	"""Get user related data by accession 'users' table in the database"""
	def __init__(self, db=None):
		self.db = db

	def get_user(self, username):
		"""Read user infomation through {username}"""
		cur = self.db.connection.cursor()
		query = "SELECT userId, username, password, email, fullName, siteIdFk FROM users WHERE username = '{username}' ".format(username=username)
		cur.execute(query)

		rows = cur.fetchall()
		
		return rows

	def get_username(self, userId):
		"""Get username with {userId}"""
		cur = self.db.connection.cursor()
		query = "SELECT username FROM users WHERE userId = '{userId}' ".format(userId=userId)
		cur.execute(query)

		row = cur.fetchone()[0]
		
		return row

class Site:
	"""Interaction with site related tables in the database"""
	def __init__(self, db=None):
		self.db = db

	def get_site(self, site_id):
		"""Read the information of a pecific site with id: {site_id}"""
		cur = self.db.connection.cursor()
		query = "SELECT siteId, siteName, street, city, state, zip, phone FROM sites WHERE siteId = '{site_id}' ".format(site_id=site_id)
		cur.execute(query)
		rows = cur.fetchall()

		return rows

	def get_user_sitename(self, userId):
		"""Get user {userId}'s working site name"""
		cur = self.db.connection.cursor()
		query = "SELECT siteName FROM sites INNER JOIN users ON sites.siteId = users.siteIdFk WHERE userId = '{userId}' ".format(userId=userId)
		cur.execute(query)
		row = cur.fetchone()[0]

		return row

	def has_service(self, siteId, service):
		"""Check if a site {siteId} provides some service {service}"""
		cur = self.db.connection.cursor()
		query = "SELECT COUNT(siteIdFk) FROM {service} WHERE siteIdFK = '{siteId}' ".format(siteId=siteId, service=service)
		cur.execute(query)
		num = cur.fetchone()[0]

		if int(num)==0:
			return False
		else:
			return True

	def calculate_services(self, siteId):
		"""Calculate the total services at a site {siteId}"""
		cur = self.db.connection.cursor()

		query_fb = "SELECT Count(foodBankId) FROM foodBanks WHERE siteIdFk = '{siteId}' ".format(siteId=siteId)
		query_fp = "SELECT Count(foodPantryId) FROM foodPantries WHERE siteIdFk = '{siteId}' ".format(siteId=siteId)
		query_sk = "SELECT Count(soupKitchenId) FROM soupKitchens WHERE siteIdFk = '{siteId}' ".format(siteId=siteId)
		query_sh = "SELECT Count(shelterId) FROM shelters WHERE siteIdFk = '{siteId}' ".format(siteId=siteId)

		cur.execute(query_fb)
		num_fb = cur.fetchone()[0]

		cur.execute(query_fp)
		num_fp = cur.fetchone()[0]

		cur.execute(query_sk)
		num_sk = cur.fetchone()[0]

		cur.execute(query_sh)
		num_sh = cur.fetchone()[0]

		num_services = num_fb + num_fp + num_sk + num_sh

		return num_services

class Shelter(object):
	"""Interaction with shelter related tables in the database"""
	def __init__(self, db=None):
		self.db = db

	def get_shelter_id(self, siteId):
		"""Get the shelter's ID at site {siteId} """
		cur = self.db.connection.cursor()
		query = "SELECT shelterId FROM shelters WHERE siteIdFk='{siteId} '".format(siteId=siteId)
		cur.execute(query)
		row = cur.fetchone()[0]

		return row

	def update_shelter(self, sh_id, desc, hours, con):
		"""Update shelter's information"""
		cur = self.db.connection.cursor()
		query = "UPDATE shelters SET description = '{desc}', hours = '{hours}', conditions = '{con}' WHERE shelterId = '{sh_id}' ".format(desc=desc, hours=hours, con=con, sh_id=sh_id)
		cur.execute(query)
		self.db.connection.commit()

	def insert_shelter(self, siteId, desc, hours, con):
		"""Create a new shelter at site: {siteId}"""
		cur = self.db.connection.cursor()
		cur.execute ('''INSERT INTO shelters (description, hours, conditions, siteIdFk)
						VALUES (%s, %s, %s, %s)
						''', (desc, hours, con, siteId))
		self.db.connection.commit()

	def delete_shelter(self, shelterId):
		"""Delete the shelter with id: {shelterId}"""
		cur = self.db.connection.cursor()
		query = "DELETE FROM shelters WHERE shelterId = {shelterId} ".format(shelterId=shelterId)
		cur.execute(query)

		self.db.connection.commit()

	def delete_bunks(self, shelterId):
		"""Delete all the bunks in the shelter {shelterId}"""
		cur = self.db.connection.cursor()
		query = "DELETE FROM bunks WHERE shelterIdFk = {shelterId} ".format(shelterId=shelterId)
		cur.execute(query)

		self.db.connection.commit()

	def insert_bunks(self, shelterId, male, female, mix):
		"""Create a bunk at shelter: {shelterId}"""
		cur = self.db.connection.cursor()
		cur.execute ('''INSERT INTO bunks (maleCount, femaleCount, mixedCOunt, shelterIdFk)
						VALUES (%s, %s, %s, %s)
						''', (male, female, mix, shelterId))
		self.db.connection.commit()

	def update_bunks(self, sh_id, male, female, mix):
		"""Given a shelter with id {sh_id}, update the counts of bunks"""
		cur = self.db.connection.cursor()
		query = "UPDATE bunks SET maleCount = '{male}', femaleCount = '{female}', mixedCount = '{mix}' WHERE shelterIdFk = '{sh_id}' ".format(male=male, female=female, mix=mix, sh_id=sh_id)

		print "update_bunks query: " + query
		cur.execute(query)
		self.db.connection.commit()

	def update_bunk(self, shelterId, bunk, bunkCount):
		"""Update the count of a specific {bunk} to {bunkCount} at shelter {shelterId}"""
		cur = self.db.connection.cursor()
		query = "UPDATE bunks SET {bunk} = '{bunkCount}' WHERE shelterIdFk = '{shelterId}' ".format(bunk=bunk, bunkCount=bunkCount, shelterId=shelterId)

		print "update_bunk query: " + query
		cur.execute(query)

		self.db.connection.commit()

	def available_bunks(self):
		"""Show all the available bunks in the whole system"""
		cur = self.db.connection.cursor()
		cur.execute('''SELECT sites.siteId, sites.siteName, sites.street, sites.city, sites.state, sites.zip, sites.phone,
			shelters.description, shelters.hours, shelters.conditions, shelters.shelterId, 
			bunks.maleCount, bunks.femaleCount, bunks.mixedCount 
			FROM sites 
			INNER JOIN shelters ON sites.siteId = shelters.siteIdFk
			INNER JOIN bunks ON bunks.shelterIdFk = shelters.shelterId
			WHERE (bunks.maleCount + bunks.femaleCount + bunks.mixedCount) > 0
			ORDER BY sites.siteName ''')

		rows = cur.fetchall()

		return rows

	def get_bunk(self, siteId):
		"""get the available bunks in a specific site {siteId}"""
		cur = self.db.connection.cursor()
		query = ('''SELECT sites.siteId, sites.siteName, sites.street, sites.city, sites.state, sites.zip, sites.phone,
			shelters.description, shelters.hours, shelters.conditions, shelters.shelterId, 
			bunks.maleCount, bunks.femaleCount, bunks.mixedCount
			FROM sites 
			INNER JOIN shelters ON sites.siteId = shelters.siteIdFk
			INNER JOIN bunks ON bunks.shelterIdFk = shelters.shelterId 
			WHERE siteId = '{siteId}' ''').format(siteId=siteId)

		print "get_bunk query: ", query

		cur.execute(query)
		rows = cur.fetchall()

		return rows

class SoupKitchen(object):
	"""Interaction with soupkitchen related tables in the database"""
	def __init__(self, db=None):
		self.db = db

	def get_soupkitchen_id(self, siteId):
		"""Get the ID of the soupkitche at site {siteId}"""
		cur = self.db.connection.cursor()
		query = "SELECT soupKitchenId FROM soupKitchens WHERE siteIdFk='{siteId} '".format(siteId=siteId)
		cur.execute(query)
		row = cur.fetchone()[0]

		return row

	def get_soupkitchen(self, soupkitchenId):
		"""Get the information of a specific soupkitchen {soupkitchenId}"""
		cur = self.db.connection.cursor()
		query = ('''SELECT soupKitchenId, description, hours, conditions, seats, siteIdFk, sites.siteName 
			FROM soupKitchens 
			INNER JOIN sites ON sites.siteId=soupKitchens.siteIdFk 
			WHERE soupKitchenId='{soupkitchenId}' ''').format(soupkitchenId=soupkitchenId)

		print "get_soupkitchen query: ", query

		cur.execute(query)
		row = cur.fetchall()

		return row

	def update_soupkitchen(self, sk_id, desc, hours, con, seats):
		"""Update the information of the soupkitchen {sk_id}"""
		cur = self.db.connection.cursor()
		query = "UPDATE soupKitchens SET description = '{desc}', hours = '{hours}', conditions = '{con}', seats = '{seats}' WHERE soupKitchenId = '{sk_id}' ".format(desc=desc, hours=hours, con=con, sk_id=sk_id, seats=seats)
		cur.execute(query)
		self.db.connection.commit()

	def insert_soupkitchen(self, siteId, desc, hours, con, seats):
		"""Create a soupkitchen at site {siteId}"""
		cur = self.db.connection.cursor()
		cur.execute ('''INSERT INTO soupKitchens (description, hours, conditions, seats, siteIdFk)
						VALUES (%s, %s, %s, %s, %s)
						''', (desc, hours, con, seats, siteId))
		self.db.connection.commit()

	def delete_soupkitchen(self, siteId):
		"""Delete the soupkitchen at site {siteId}"""
		cur = self.db.connection.cursor()
		query = "DELETE FROM soupKitchens WHERE siteIdFk = {siteId} ".format(siteId=siteId)
		cur.execute(query)

		self.db.connection.commit()

class FoodPantry(object):
	"""Interaction with foodpantry related tables in the database"""
	def __init__(self, db=None):
		self.db = db

	def get_foodpantry_id(self, siteId):
		"""get the ID of foodpantry at site {siteId}"""
		cur = self.db.connection.cursor()
		query = "SELECT foodPantryId FROM foodPantries WHERE siteIdFk='{siteId} '".format(siteId=siteId)
		cur.execute(query)
		row = cur.fetchone()[0]

		return row

	def get_foodpantry(self, foodpantryId):
		"""Read the foodpantry {foodpantryId}'s information"""
		cur = self.db.connection.cursor()
		query = ('''SELECT foodPantryId, description, hours, conditions, siteIdFk, sites.siteName 
			FROM foodPantries 
			INNER JOIN sites ON sites.siteId=foodPantries.siteIdFk
			WHERE foodPantryId='{foodpantryId}' ''').format(foodpantryId=foodpantryId)

		print "get_foodpantry uery: ", query

		cur.execute(query)
		row = cur.fetchall()

		return row

	def update_foodpantry(self, fp_id, desc, hours, con):
		"""update the information of foodpantry {fp_id}"""
		cur = self.db.connection.cursor()
		query = "UPDATE foodPantries SET description = '{desc}', hours = '{hours}', conditions = '{con}' WHERE foodPantryId = '{fp_id}' ".format(desc=desc, hours=hours, con=con, fp_id=fp_id)
		cur.execute(query)

		self.db.connection.commit()

	def insert_foodpantry(self, siteId, desc, hours, con):
		"""create a foodpantry at site {siteId}"""
		cur = self.db.connection.cursor()
		cur.execute ('''INSERT INTO foodPantries (description, hours, conditions, siteIdFk)
						VALUES (%s, %s, %s, %s)
						''', (desc, hours, con, siteId))
		self.db.connection.commit()

	def delete_foodpantry(self, siteId):
		"""Delete the foodpantry at site {siteId}"""
		cur = self.db.connection.cursor()
		query = "DELETE FROM foodPantries WHERE siteIdFk = {siteId} ".format(siteId=siteId)
		cur.execute(query)

		self.db.connection.commit()

class FoodBank:
	"""Interaction with foodbank related tables in the database"""
	def __init__(self, db=None):
		self.db = db

	def get_foodbank_id(self, siteId):
		"""get the ID of foodbank at site {siteId}"""
		cur = self.db.connection.cursor()
		query = "SELECT foodbankId FROM foodBanks WHERE siteIdFk='{siteId} '".format(siteId=siteId)
		cur.execute(query)
		row = cur.fetchone()[0]

		return row

	def get_foodbank_siteId(self, foodbank_id):
		"""Get the ID of a site which has a foodbank {foodbank_id}"""
		cur = self.db.connection.cursor()
		query = "SELECT siteIdFk FROM foodBanks WHERE foodBankId = '{foodbank_id}' ".format(foodbank_id=foodbank_id)
		cur.execute(query)
		row = cur.fetchone()[0]

		return row

	def insert_foodbank(self, siteId):
		"""create a foodbank at site {siteId}"""
		cur = self.db.connection.cursor()
		query = "INSERT INTO foodBanks (siteIdFk) VALUES ('{siteId}')".format(siteId=siteId)
		cur.execute(query)

		self.db.connection.commit()

	def delete_foodbank(self, foodbankId):
		"""delete the foodbank {foodbankId}"""
		cur = self.db.connection.cursor()
		query = "DELETE FROM foodBanks WHERE foodBankId = {foodbankId} ".format(foodbankId=foodbankId)
		cur.execute(query)

		self.db.connection.commit()

class Item:
	"""Interaction with items related tables in the database"""
	def __init__(self, db=None):
		self.db = db

	def get_items(self):
		"""Read all the items in the database"""
		cur = self.db.connection.cursor()
		cur.execute('''SELECT items.itemId, items.item, subCategories.subcategory, storageTypes.storageType, items.quantity, items.expiration, sites.siteId, sites.siteName 
			FROM items 
			INNER JOIN foodBanks 
			ON foodBanks.foodBankId = items.foodBankIdFk 
			INNER JOIN sites 
			ON sites.siteId = foodBanks.siteIdFk 
			INNER JOIN subCategories 
			ON subCategories.subCatId = items.subCatIdFk 
			INNER JOIN storageTypes 
			ON storageTypes.storageId = items.storageIdFk 
			ORDER BY sites.siteName ''')

		rows = cur.fetchall()

		return rows

	def get_items_by_foodbank(self, foodbankId):
		"""read all the items in a specific foodbank {foodbankId}"""
		cur = self.db.connection.cursor()
		query = ('''SELECT items.itemId, items.item, subCategories.subcategory, storageTypes.storageType, items.quantity, items.expiration, sites.siteId, sites.siteName 
			FROM items 
			INNER JOIN foodBanks 
			ON foodBanks.foodBankId = items.foodBankIdFk 
			INNER JOIN sites 
			ON sites.siteId = foodBanks.siteIdFk 
			INNER JOIN subCategories 
			ON subCategories.subCatId = items.subCatIdFk 
			INNER JOIN storageTypes 
			ON storageTypes.storageId = items.storageIdFk 
			WHERE foodBanks.foodBankId = '{foodbankId}' ''').format(foodbankId=foodbankId)

		print "get_items_by_foodbank query: ", query
		
		cur.execute(query)
		rows = cur.fetchall()

		return rows

	def filt_items(self, siteId, cat, subCat, storage, expiration, expression):
		"""
		Search items in the database.
		The query changes dynamically basing on the searching terms input by the user.
		"""
		cur = self.db.connection.cursor()
		query = ('''SELECT items.itemId, items.item, subCategories.subcategory, storageTypes.storageType, items.quantity, items.expiration, sites.siteId, sites.siteName 
			FROM items 
			INNER JOIN foodBanks 
			ON foodBanks.foodBankId = items.foodBankIdFk 
			INNER JOIN sites 
			ON sites.siteId = foodBanks.siteIdFk 
			INNER JOIN subCategories 
			ON subCategories.subCatId = items.subCatIdFk 
			INNER JOIN storageTypes 
			ON storageTypes.storageId = items.storageIdFk ''')

		hasFormerFilter = False
		filter_query = ""

		print "siteId: " + siteId

		if siteId != '':
			filter_query += "sites.siteId = '{siteId}' ".format(siteId=int(siteId))
			hasFormerFilter = True

		if subCat != 0:
			if hasFormerFilter:
				filter_query += "AND "

			filter_query += "items.subCatIdFk = '{subCat}' ".format(subCat=subCat)
			hasFormerFilter = True
		else:
			if cat == 1:
				if hasFormerFilter:
					filter_query += "AND "

				filter_query += "items.subCatIdFk < 7 "
				hasFormerFilter = True

			if cat == 2:
				if hasFormerFilter:
					filter_query += "AND "

				filter_query += "items.subCatIdFk > 6 "
				hasFormerFilter = True

		if storage != 0:
			if hasFormerFilter:
				filter_query += "AND "

			filter_query += "items.storageIdFk = '{storage}' ".format(storage=storage)
			hasFormerFilter = True

		if expiration != '':
			if hasFormerFilter:
				filter_query += "AND "

			filter_query += "items.expiration > '{expiration}' ".format(expiration=expiration)
			hasFormerFilter = True

		if expression != '':
			if hasFormerFilter:
				filter_query += "AND "

			filter_query += "items.item LIKE CONCAT('%', '{expression}', '%') ".format(expression=expression)
			hasFormerFilter = True

		if hasFormerFilter:
			query += "WHERE " + filter_query

		query += "ORDER BY sites.siteName"

		print "filt query: " + query

		cur.execute(query)
		rows = cur.fetchall()

		return rows

	def get_requsted_item(self, reqId):
		"""Get the item information of a specitic request {reqId}"""
		cur = self.db.connection.cursor()
		query = ('''SELECT itemId, items.quantity 
			FROM items 
			INNER JOIN requests ON items.itemId = requests.itemIdFk 
			WHERE requests.requestId = {reqId} ''').format(reqId=reqId)

		print "get_requsted_item query: ", query

		cur.execute(query)
		row = cur.fetchone()

		return row
	
	def insert_item(self, itemName, subcat, store, quant, exp, foodbank):
		"""Insert a new item"""
		cur = self.db.connection.cursor()
		cur.execute ('''INSERT INTO items (item, subCatIdFk, storageIdFk, quantity, expiration, foodBankIdFk)
						VALUES (%s, %s, %s, %s, %s, %s)
						''', (itemName, subcat, store, quant, exp, foodbank))
		self.db.connection.commit()

	def delete_foodbank_items(self, foodbankId):
		"""Delete all the items in a foodbank {foodbankId}"""
		cur = self.db.connection.cursor()
		query = "DELETE FROM items WHERE foodBankIdFk = {foodbankId} ".format(foodbankId=foodbankId)
		cur.execute(query)

		self.db.connection.commit()

	def delete_item(self, itemId):
		"""Delete a specific item {itemId}"""
		cur = self.db.connection.cursor()
		query = "DELETE FROM items WHERE itemId = {itemId} ".format(itemId=itemId)
		cur.execute(query)

		self.db.connection.commit()

	def calculate_meals(self):
		"""Calculate all the meals in the database"""
		cur = self.db.connection.cursor()

		query_veg = ('''SELECT sum(quantity) FROM items WHERE subCatIdFk = 1 ''')
		query_nut = ('''SELECT sum(quantity) FROM items WHERE subCatIdFk = 2 ''')
		query_meat = ('''SELECT sum(quantity) FROM items WHERE subCatIdFk = 3 OR subCatIdFk = 4 ''')

		cur.execute(query_veg)
		vegetable = cur.fetchone()[0]

		cur.execute(query_nut)
		nut = cur.fetchone()[0]

		cur.execute(query_meat)
		meat = cur.fetchone()[0]

		return (vegetable, nut, meat)

	def update_item_count(self, itemId, quant):
		"""Update the count of the item {itemId} to a given number {quant}"""
		cur = self.db.connection.cursor()
		query = "UPDATE items SET Quantity = '{quant}' WHERE itemId = '{itemId}' ".format(quant=quant, itemId=itemId)
		cur.execute(query)

		self.db.connection.commit()


	def get_item_foodbank(self, itemId):
		"""get the ID of a foodbank where the item {itemId} is stored"""
		cur = self.db.connection.cursor()
		query = "SELECT foodBankIdFk FROM items WHERE itemId ='{itemId}' ".format(itemId=itemId)
		cur.execute(query)
		row = cur.fetchone()[0]

		return row

class Request(object):
	"""Interaction with clients related tables in the database"""
	def __init__(self, db=None):
		self.db = db

	def get_requests_by_user(self, makingUser):
		"""Get the request by user {makingUser}"""
		cur = self.db.connection.cursor()
		query = ('''SELECT requestId, requestedQty, providedQty, status, makingUserFk, approvingUserFk, 
			requests.itemIdFk, requests.foodBankIdFk, items.item, sites.siteName
			FROM requests 
			INNER JOIN items ON items.itemId = requests.itemIdFk 
			INNER JOIN foodBanks ON foodBanks.foodBankId = requests.foodBankIdFk
			INNER JOIN sites ON sites.siteId = foodBanks.siteIdFk 
			WHERE makingUserFk = '{makingUser}' ''').format(makingUser=makingUser)

		print "get_requests_by_user query: ", query

		cur.execute (query)
		rows = cur.fetchall()

		return rows

	def get_request_quan(self, reqId):
		"""get the requested quantity of a request {reqId}"""
		cur = self.db.connection.cursor()
		query = "SELECT requestedQty FROM requests WHERE requestId = {reqId} ".format(reqId=reqId)
		cur.execute(query)
		row = cur.fetchone()[0]

		return row

	def get_item_requestId(self, itemId):
		"""get the ID of a request on the given item {itemId}"""
		cur = self.db.connection.cursor()
		query = "SELECT requestId FROM requests WHERE itemIdFk = {itemId} ".format(itemId=itemId)
		cur.execute(query)
		rows = cur.fetchall()

		return rows

	def outstanding_requests(self, site_id):
		"""outstanding requests at site {site_id}"""
		cur = self.db.connection.cursor()
		query = ('''SELECT requestId, requestedQty, providedQty, status, makingUserFk, approvingUserFk, 
			requests.itemIdFk, requests.foodBankIdFk, items.item, sites.siteName
			FROM requests 
			INNER JOIN items ON items.itemId = requests.itemIdFk 
			INNER JOIN foodBanks ON foodBanks.foodBankId = requests.foodBankIdFk
			INNER JOIN sites ON sites.siteId = foodBanks.siteIdFk 
			WHERE requests.status = 'pending' AND sites.siteId = '{site_id}' 
			ORDER BY requestId ''').format(site_id=site_id)

		print "outstanding requests query: " + query

		cur.execute(query)

		rows = cur.fetchall()

		print "query results: " + str(rows)

		return rows

	def outstanding_requests_by_qty(self, site_id):
		"""outstanding requests at site {site_id}"""
		cur = self.db.connection.cursor()
		query = ('''SELECT requestId, requestedQty, providedQty, status, makingUserFk, approvingUserFk, 
			requests.itemIdFk, requests.foodBankIdFk, items.item, sites.siteName
			FROM requests 
			INNER JOIN items ON items.itemId = requests.itemIdFk 
			INNER JOIN foodBanks ON foodBanks.foodBankId = requests.foodBankIdFk
			INNER JOIN sites ON sites.siteId = foodBanks.siteIdFk 
			WHERE requests.status = 'pending' AND sites.siteId = '{site_id}' 
			ORDER BY requestedQty ''').format(site_id=site_id)

		print "outstanding requests query: " + query

		cur.execute(query)

		rows = cur.fetchall()

		print "query results: " + str(rows)

		return rows

	def outstanding_requests_by_subcat(self, site_id):
		"""outstanding requests at site {site_id}"""
		cur = self.db.connection.cursor()
		query = ('''SELECT requestId, requestedQty, providedQty, status, makingUserFk, approvingUserFk, 
			requests.itemIdFk, requests.foodBankIdFk, items.item, sites.siteName
			FROM requests 
			INNER JOIN items ON items.itemId = requests.itemIdFk 
			INNER JOIN foodBanks ON foodBanks.foodBankId = requests.foodBankIdFk
			INNER JOIN sites ON sites.siteId = foodBanks.siteIdFk 
			WHERE requests.status = 'pending' AND sites.siteId = '{site_id}' 
			ORDER BY items.subCatIdFk ''').format(site_id=site_id)

		print "outstanding requests query: " + query

		cur.execute(query)

		rows = cur.fetchall()

		return rows

	def outstanding_requests_by_store(self, site_id):
		"""outstanding requests at site {site_id}"""
		cur = self.db.connection.cursor()
		query = ('''SELECT requestId, requestedQty, providedQty, status, makingUserFk, approvingUserFk, 
			requests.itemIdFk, requests.foodBankIdFk, items.item, sites.siteName
			FROM requests 
			INNER JOIN items ON items.itemId = requests.itemIdFk 
			INNER JOIN foodBanks ON foodBanks.foodBankId = requests.foodBankIdFk
			INNER JOIN sites ON sites.siteId = foodBanks.siteIdFk 
			WHERE requests.status = 'pending' AND sites.siteId = '{site_id}' 
			ORDER BY items.storageIdFk ''').format(site_id=site_id)

		print "outstanding requests query: " + query

		cur.execute(query)

		rows = cur.fetchall()

		print "query results: " + str(rows)

		return rows

	def insert_request(self, quantity, userId, itemId, foodbankId):
		"""insert a request by user {userId} on foodbank {foodbankId}"""
		cur = self.db.connection.cursor()
		cur.execute ('''INSERT INTO requests (requestedQty, status, makingUserFk, itemIdFk, foodBankIdFk)
						VALUES (%s, %s, %s, %s, %s)
						''', (quantity, 'pending', userId, itemId, foodbankId))
		self.db.connection.commit()

	def cancel_request(self, requestId):
		"""cancel a request {requestId}"""
		cur = self.db.connection.cursor()
		query = "DELETE FROM requests WHERE requestId = '{requestId}' ".format(requestId=requestId)
		cur.execute (query)
		self.db.connection.commit()

	def update_request(self, requestId, quan):
		"""update the quantiy of a request {requestId}"""
		cur = self.db.connection.cursor()
		query = "UPDATE requests SET requestedQty = '{quantity}' WHERE requestId = '{requestId}' ".format(quantity=quan, requestId=requestId)
		cur.execute (query)
		self.db.connection.commit()

	def update_request_out(self, requestId):
		"""update request {requestedId} because the items are out of stock"""
		cur = self.db.connection.cursor()
		query = "UPDATE requests SET status ='out of stock' WHERE requestId = '{requestId}' ".format(requestId=requestId)
		cur.execute (query)
		self.db.connection.commit()

	def approve_request(self, requestId, quantity, status, approvingUser):
		"""update a request basing on approval information"""
		cur = self.db.connection.cursor()
		query = "UPDATE requests SET providedQty = '{quantity}', status = '{status}', approvingUserFk = '{approvingUser}' WHERE requestId = '{requestId}' ".format(quantity=quantity, approvingUser=approvingUser, requestId=requestId, status=status)
		cur.execute (query)
		self.db.connection.commit()

class Client(object):
	"""Interaction with items related tables in the database"""
	def __init__(self, db=None):
		self.db = db

	def insert_client(self, name, desc, phone):
		"""insert a client"""
		cur = self.db.connection.cursor()
		cur.execute ('''INSERT INTO clients (fullName, description, phone)
						VALUES (%s, %s, %s)
						''', (name, desc, phone))
		self.db.connection.commit()

	def get_client(self, client_id):
		"""get the information of a client {client_id}"""
		cur = self.db.connection.cursor()
		query = "SELECT clientId, fullName, description, phone FROM clients WHERE clientId = '{client_id}' ".format(client_id=client_id)
		cur.execute(query)

		row = cur.fetchall()

		return row

	def search_clients(self, name, desc):
		"""
		search clients
		dynamic query basing on searching terms
		limit 5 output
		"""
		cur = self.db.connection.cursor()
		query = ('''SELECT clientId, fullName, description, phone FROM clients ''')

		hasFormerFilter = False
		filter_query = ""

		if name != '':
			if hasFormerFilter:
				filter_query += "AND "

			filter_query += "fullName LIKE CONCAT('%', '{name}', '%') ".format(name=name)
			hasFormerFilter = True

		if desc != '':
			if hasFormerFilter:
				filter_query += "AND "

			filter_query += "description LIKE CONCAT('%', '{desc}', '%') ".format(desc=desc)
			hasFormerFilter = True


		if hasFormerFilter:
			query += "WHERE " + filter_query

		query += "ORDER BY fullName LIMIT 5"

		print "search clients query: " + query

		cur.execute(query)
		rows = cur.fetchall()

		return rows

	def update_client(self, client_id, name, desc, phone):
		"""update client {client_id}'s information """
		cur = self.db.connection.cursor()
		query = "UPDATE clients SET fullName = '{name}', description = '{desc}', phone = '{phone}' WHERE clientId = '{client_id}' ".format(name=name, desc=desc, phone=phone, client_id=client_id)
		cur.execute(query)

		self.db.connection.commit()
		
class ClientLog(object):
	"""Interaction with client logs related tables in the database"""
	def __init__(self, db=None):
		self.db = db

	def get_modify_logs(self, clientId):
		"""get client {clientId}'s mocification logs"""
		cur = self.db.connection.cursor()
		query = ('''SELECT clientLogId, time, textNotes FROM clientLogs 
			WHERE logType = 'modified' AND clientIdFk = '{clientId}' 
			ORDER BY time DESC ''').format(clientId=clientId)
		cur.execute(query)
		rows = cur.fetchall()

		return rows

	def get_checkin_logs(self, clientId):
		"""get client {clientId}'s checkin logs"""
		cur = self.db.connection.cursor()
		query = ('''SELECT clientLogId, time, sites.siteName, textNotes 
			FROM clientLogs 
			INNER JOIN sites 
			ON sites.siteId = clientLogs.siteIdFk 
			WHERE logType = 'checkin' AND clientIdFk = '{clientId}' 
			ORDER BY time DESC ''').format(clientId=clientId)
		
		cur.execute(query)
		rows = cur.fetchall()

		return rows
		
	def insert_client_modification_log(self, client_id, notes):
		"""Insert client {client_id}'s modification log"""
		cur = self.db.connection.cursor()
		cur.execute ('''INSERT INTO clientLogs (clientIdFk, textNotes, logType)
						VALUES (%s, %s, %s) ''', (client_id, notes, 'modified'))
		self.db.connection.commit()

	def insert_client_checkin_log(self, client_id, site_id, notes):
		"""Insert client {client_id}'s checkin log"""
		cur = self.db.connection.cursor()
		cur.execute ('''INSERT INTO clientLogs (clientIdFk, siteIdFk, textNotes, logType)
						VALUES (%s, %s, %s, %s) ''', (client_id, site_id, notes, 'checkin'))
		self.db.connection.commit()

