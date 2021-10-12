from flask import Flask, render_template, url_for, request, redirect, session, flash, g, make_response, send_file
from flask_mysqldb import MySQL
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from functools import wraps
import gc

from config import *

#import classes
from models import User, Site, Item, FoodBank, FoodPantry, SoupKitchen, Shelter, Request, Client, ClientLog #, Category, SubCategories, StorageTypes

#from flask_login import LoginManager

app = Flask(__name__, static_folder=ASSETS_FOLDER, template_folder=TEMPLATE_FOLDER)

app.secret_key = SECRET_KEY

app.config.from_object('config')

mysql = MySQL(app)

#initialize objects
users = User(db=mysql)
sites = Site(db=mysql)
items = Item(db=mysql)
foodbanks = FoodBank(db=mysql)
foodpantries = FoodPantry(db=mysql)
soupkitchens = SoupKitchen(db=mysql)
shelters = Shelter(db=mysql)
requests = Request(db=mysql)
clients = Client(db=mysql)
clientLogs = ClientLog(db=mysql)

#categories = Category(db=mysql)
#subCategories = SubCategories(db=mysql)
#storageTypes = StorageTypes(db=mysql)

#Home page
@app.route('/')
def homepage():
	return render_template("index.html")

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("Please login first.")
            return redirect(url_for('login'))

    return wrap

#User login with username and password
@app.route('/login/', methods=['GET','POST'])
def login():
    try:        
        error = None
        if request.method == 'POST':

            data = format_users(users.get_user(request.form['username']))[0]
            pw = data['password']

            if pw == request.form['password']:
                session['logged_in'] = True
                session['username'] = request.form['username']
                session['id'] = data['id']
                session['siteId'] = data['site']

                print "Session site: ", session['siteId']

                print "username: ", session['username']

                print "password: ", pw
                
                return redirect(url_for('show_user', username=data['username']))
                #return show_user(data['username'])

            else:
                error = 'Your username or password is not corect. Please try again.'

        gc.collect()

        return render_template('login.html', error=error)

    except Exception, e:
        print "exception: ", e
        error = 'Invalid credentials. Try again'

	return render_template('login.html', error=error)

#user logout
@app.route('/logout')
@login_required
def logout():
    session.clear()
    #flash("You have been logged out.")
    gc.collect()

    return redirect(url_for('homepage'))

#show the meals in the system
@app.route('/meals_remaining', methods=['GET'])
def meals_remaining():
    meals = items.calculate_meals()

    return render_template('meals_remaining.html', meals=meals)

#show the available bunks in the system
@app.route('/available_bunks', methods=['GET'])
def show_available_bunks():
    bunks_data = shelters.available_bunks()
    bunks = format_bunks(bunks_data)

    numbers = len(bunks)

    return render_template('available_bunks.html', bunks=bunks, numbers=numbers)

#User <user_id>'s dashboard
@app.route('/users/<username>', methods=['GET', 'POST'])
@login_required
def show_user(username):
    user=format_users(users.get_user(username))[0]

    site_id = session['siteId']
    site = format_sites(sites.get_site(site_id))[0]

    has_foodbank = sites.has_service(site_id, 'foodBanks')
    has_foodpantry = sites.has_service(site_id, 'foodPantries')
    has_shelter = sites.has_service(site_id, 'shelters')
    has_soupkitchen = sites.has_service(site_id, 'soupKitchens')

    if has_foodbank:
        foodbank_id = foodbanks.get_foodbank_id(site_id)
    else:
        foodbank_id = 0

    if has_shelter:
        shelter_id = shelters.get_shelter_id(site_id)
    else:
        shelter_id = 0

    if has_foodpantry:
        foodpantry_id = foodpantries.get_foodpantry_id(site_id)
    else:
        foodpantry_id = 0

    if has_soupkitchen:
        soupkitchen_id = soupkitchens.get_soupkitchen_id(site_id)
    else:
        soupkitchen_id = 0

    has_services = {"foodbank": has_foodbank, 
                    "shelter": has_shelter,
                    "foodpantry": has_foodpantry, 
                    "soupkitchen": has_soupkitchen
                    }

    service_id = {"foodbank": foodbank_id, 
                    "shelter": shelter_id,
                    "foodpantry": foodpantry_id,
                    "soupkitchen": soupkitchen_id
                    }

    total_service = sites.calculate_services(site_id)
    delete_msg = ""
    delete_last_msg = "  Can not remove the last service!"

    if request.method == 'POST':
        form_val = request.form['form_name']

        if form_val=='create_fb':
            foodbanks.insert_foodbank(site_id)

            return redirect(url_for('show_user', username=session['username']))

        if form_val=='delete_fb':
            total_service = sites.calculate_services(site_id)

            if total_service<=1:
                return render_template('user_dashboard.html', user=user, site=site, services=has_services, service_id=service_id, total=total_service, dlmsg=delete_last_msg)

            else:
                foodbank = foodbanks.get_foodbank_id(session['siteId'])

                items.delete_foodbank_items(foodbank)
                foodbanks.delete_foodbank(foodbank)
                
                return redirect(url_for('show_user', username=session['username']))

        if form_val=='delete_fp':
            total_service = sites.calculate_services(site_id)

            if total_service<=1:
                return render_template('user_dashboard.html', user=user, site=site, services=has_services, service_id=service_id, total=total_service, dlmsg=delete_last_msg)

            else:
                foodpantries.delete_foodpantry(site_id)
                
                return redirect(url_for('show_user', username=session['username']))

        if form_val=='delete_sk':

            total_service = sites.calculate_services(site_id)
            
            if total_service<=1:
                return render_template('user_dashboard.html', user=user, site=site, services=has_services, service_id=service_id, total=total_service, dlmsg=delete_last_msg)

            else:
                soupkitchens.delete_soupkitchen(site_id)

                return redirect(url_for('show_user', username=session['username']))

        if form_val=='delete_shelter':
            total_service = sites.calculate_services(site_id)
            
            if total_service<=1:
                return render_template('user_dashboard.html', user=user, site=site, services=has_services, service_id=service_id, total=total_service, dlmsg=delete_last_msg)

            else:
                shelterId = shelters.get_shelter_id(site_id)

                shelters.delete_bunks(shelterId)
                shelters.delete_shelter(shelterId)

                return redirect(url_for('show_user', username=session['username']))

    return render_template('user_dashboard.html', user=user, site=site, services=has_services, service_id=service_id, total=total_service, dlmsg=delete_msg)

#show all items in the system
@app.route('/items', methods=['GET', 'POST'])
@login_required
def show_items():

    if request.method == 'POST':
        item_id = request.form['form_name']

        if int(item_id) > 0:
            print "Entering item update form"

            quan = request.form['quantity'].strip()

            if quan=='' or not RepresentsInt(quan) or int(quan)<0 :
                flash("Please input a non-negative number.")

                return redirect(url_for('show_items'))

            elif int(quan)==0:

                item_requests = requests_on_item(item_id)

                #if no request on this item, delete this item directly
                if len(item_requests)<1:
                    print "len: ", len(item_requests)
                    items.delete_item(item_id)

                #if some requests on this item, close the requests first
                #then set item number as 0
                else:
                    for reqId in item_requests:
                        requests.update_request_out(reqId)

                    items.update_item_count(item_id, 0)

                return redirect(url_for('show_items'))

            else:
                items.update_item_count(item_id, quan)

                return redirect(url_for('show_items'))

        else:
            print "Entering request item form"

            item_id = 0 - int(item_id)
            quan = request.form['quantity'].strip()
            userId = session['id']
            fb = items.get_item_foodbank(item_id)

            if quan =='' or not RepresentsInt(quan) or int(quan)<=0 :
                flash("Please input a positive number.")

                return redirect(url_for('show_items'))

            else:
                requests.insert_request(quan, userId, item_id, fb)
                return redirect(url_for('show_items'))

    items_data = format_items(items.get_items())
    message = "All items in the system: "
 
    return render_template('show_items.html', items=items_data, message=message)
    
#search items and display the results
@app.route('/items/search_items', methods=['GET', 'POST'])
@login_required
def search_items():

    if request.method == 'POST':

        print "you clicked some button"
        form_name = request.form['form_name']

        print "form name: " + form_name

        if form_name == 'search':
            print "entering search form"

            searchFrom = request.form['searchFrom']

            if searchFrom == 'system':
                siteId = ''
                print "from the whole system"
            else:
                siteId = searchFrom
                print "from the current site: " + siteId

            expression = request.form['expression'].strip()
            category = int(request.form['category'])
            subcategory = int(request.form['subcategory'])
            storage = int(request.form['storage'])
            expiration = request.form['expiration'].strip()
            print "exp time: ", expiration

            message = "Items matching you search: "

            search_data = items.filt_items(siteId, category, subcategory, storage, expiration, expression)

            items_data = format_items(search_data)

            return render_template('show_items.html', items=items_data, message=message)

        else:

            item_id = request.form['form_name']

            print "item id: " + item_id

            if int(item_id) > 0:
                print "Entering item update form"

                quan = request.form['quantity'].strip()


                if quan=='' or not RepresentsInt(quan) or int(quan)<0 :
                    flash("Please input a non-negative integer.")

                    return redirect(url_for('show_items'))

                elif int(quan)==0:

                    item_requests = requests_on_item(itemId)

                    #if no request on this item, delete this item directly
                    if len(item_requests)<1:
                        print "len: ", len(item_requests)
                        items.delete_item(itemId)

                    #if some requests on this item, close the requests first
                    #then set item number as 0
                    else:
                        for reqId in item_requests:
                            requests.update_request_out(reqId)

                        items.update_item_count(itemId, 0)

                    return redirect(url_for('show_items'))

                else:
                    items.update_item_count(itemId, quan)

                    return redirect(url_for('show_items'))

            else:
                print "Entering request item form"

                item_id = 0 - int(item_id)
                quan = request.form['quantity'].strip()
                userId = session['id']
                fb = items.get_item_foodbank(item_id)

                if quan =='' or not RepresentsInt(quan) or int(quan)<=0 :
                    flash("Please input a positive number.")

                    return redirect(url_for('show_items'))

                else:
                    requests.insert_request(quan, userId, item_id, fb)
                    return redirect(url_for('show_items'))

    return render_template('search_items.html')

#insert an item into the database
@app.route('/items/insert_item', methods=['GET', 'POST'])
@login_required
def insert_item():

    if request.method == 'POST':
        error = 0

        itemName = request.form['itemname'].strip()
        quan = request.form['quantity'].strip()
        #category = request.form['category']
        subcategory = int(request.form['subcategory'])
        storage = int(request.form['storage'])
        expiration = request.form['expiration'].strip()

        if expiration == '':
            expiration = '2099-01-01'

        print "expiration: ", expiration

        if itemName == '':
            error = 1
            flash("Please input the name of item.")

        if quan=='' or not RepresentsInt(quan) or int(quan)<=0 :
            error = 1
            flash("Please input a positive integer in the 'quantity' field.")

        if subcategory == 0:
            error = 1
            flash("Please select subcategory.")

        if storage == 0:
            error = 1
            flash("Please select storage type.")

        if error == 1:
            return render_template('insert_item.html')

        else:
            foodbank = foodbanks.get_foodbank_id(session['siteId'])

            items.insert_item(itemName, subcategory, storage, quan, expiration, foodbank)

            return redirect(url_for('show_foodbank', foodbank_id=foodbank))

    return render_template('insert_item.html')

#show information of a food pantry {foodpantry_id}
@app.route('/foodpantry/<foodpantry_id>')
@login_required
def show_foodpantry(foodpantry_id):
    foodpantry_data = foodpantries.get_foodpantry(foodpantry_id)
    foodpantry_data = format_foodpantries(foodpantry_data)[0]

    return render_template('show_foodpantry.html', foodpantry=foodpantry_data)

#create a new foodpantry at site {site_id}
@app.route('/create_foodpantry/<site_id>', methods=['GET', 'POST'])
@login_required
def create_foodpantry(site_id):
    site = sites.get_site(site_id)
    message = "Please input food pantry information before submit."

    if request.method=='POST':
        desc = request.form['description'].strip()
        hours = request.form['hours'].strip()
        con = request.form['conditions'].strip()

        if desc=='' or hours=='' or con=='':
            message = "Please input all information for the food pantry"

            return render_template('insert_foodpantry.html', site=site, message=message)

        foodpantries.insert_foodpantry(site_id, desc, hours, con)

        return redirect(url_for('show_user', username=session['username']))

    return render_template('insert_foodpantry.html', site=site, message=message)

#Edit the information of foodpantry {foodpantry_id}
@app.route('/update_foodpantry/<foodpantry_id>', methods=['GET', 'POST'])
@login_required
def update_foodpantry(foodpantry_id):
    old_data = format_foodpantries(foodpantries.get_foodpantry(foodpantry_id))[0]

    message = "Please check the food pantry information before modification."

    if request.method=='POST':
        desc = request.form['description'].strip()
        hours = request.form['hours'].strip()
        conditions = request.form['conditions'].strip()

        if desc=='' and hours=='' and conditions=='':
            message = "You change nothing. Please input new infomation"

            return render_template('update_foodpantry.html', message=message, old=old_data)

        else:
            if desc=='':
                desc = old_data['description']
            if hours=='':
                hours = old_data['hours']
            if conditions=='':
                conditions = old_data['conditions']

            foodpantries.update_foodpantry(foodpantry_id, desc, hours, conditions)
            #message = "You have successfully updated the food pantry."

            return redirect(url_for('show_foodpantry', foodpantry_id=foodpantry_id))

    return render_template('update_foodpantry.html', message=message, old=old_data)

#show the information of the soupkitchen {soupkitchen_id}
@app.route('/soupkitchen/<soupkitchen_id>')
@login_required
def show_soupkitchen(soupkitchen_id):
    soupkitchen_data = soupkitchens.get_soupkitchen(soupkitchen_id)
    soupkitchen_data = format_soupkitchens(soupkitchen_data)[0]

    return render_template('show_soupkitchen.html', soupkitchen=soupkitchen_data)

#create a new soupkitchen at site {site_id}
@app.route('/create_soupkitchen/<site_id>', methods=['GET', 'POST'])
@login_required
def create_soupkitchen(site_id):
    site = sites.get_site(site_id)
    message = "Please input soup kitchen information before submit."

    if request.method=='POST':
        desc = request.form['description'].strip()
        hours = request.form['hours'].strip()
        con = request.form['conditions'].strip()
        seats = request.form['seats'].strip()

        if desc=='' or hours=='' or con=='' or seats=='':
            message = "Please input all information for the soup kitchen"

            return render_template('insert_soupkitchen.html', site=site, message=message)

        soupkitchens.insert_soupkitchen(site_id, desc, hours, con, seats)

        return redirect(url_for('show_user', username=session['username']))

    return render_template('insert_soupkitchen.html', site=site, message=message)

#Edit the information of the soupkitchen {soupkitchen_id}
@app.route('/update_soupkitchen/<soupkitchen_id>', methods=['GET', 'POST'])
@login_required
def update_soupkitchen(soupkitchen_id):
    old_data = format_soupkitchens(soupkitchens.get_soupkitchen(soupkitchen_id))[0]

    message = "Please check the soupkitchen information before modification."

    if request.method=='POST':
        desc = request.form['description'].strip()
        hours = request.form['hours'].strip()
        conditions = request.form['conditions'].strip()
        seats = request.form['seats'].strip()

        if desc=='' and hours=='' and conditions=='' and seats=='':
            message = "You change nothing. Please input new infomation"

            return render_template('update_soupkitchen.html', message=message, old=old_data)

        else:
            if desc=='':
                desc = old_data['description']
            if hours=='':
                hours = old_data['hours']
            if conditions=='':
                conditions = old_data['conditions']
            if seats=='':
                seats = old_data['seats']

            soupkitchens.update_soupkitchen(soupkitchen_id, desc, hours, conditions, seats)
            #message = "You have successfully updated the food pantry."

            return redirect(url_for('show_soupkitchen', soupkitchen_id=soupkitchen_id))

    return render_template('update_soupkitchen.html', message=message, old=old_data)

#Show information of the shelter {shelter_id}
@app.route('/shelter/<site_id>')
@login_required
def show_shelter(site_id):

    shelter_data = format_bunks(shelters.get_bunk(site_id))[0]

    return render_template('show_shelter.html', shelter=shelter_data, siteId=site_id)

#create a new shelter at site {site_id}
@app.route('/create_shelter/<site_id>', methods=['GET', 'POST'])
@login_required
def create_shelter(site_id):
    site = sites.get_site(site_id)

    message = "Please check the shelter information before submitting."

    if request.method=='POST':
        desc = request.form['description'].strip()
        hours = request.form['hours'].strip()
        conditions = request.form['conditions'].strip()

        malecount = request.form['malecount'].strip()
        femalecount = request.form['femalecount'].strip()
        mixedcount = request.form['mixedcount'].strip()

        shelter_is_filled = not(desc=='' or hours=='' or conditions=='')
        bunk_is_filled = not(malecount=='' or femalecount=='' or mixedcount=='') 

        if not shelter_is_filled or not bunk_is_filled:
            message = "Please fill all fields."

            return render_template('insert_shelter.html', message=message, site=site)

        else:
            shelters.insert_shelter(site_id, desc, hours, conditions)

            shelterId = shelters.get_shelter_id(site_id)

            shelters.insert_bunks(shelterId, malecount, femalecount, mixedcount)

            #return redirect(url_for('show_shelter', site_id=site_id))
            return redirect(url_for('show_user', username=session['username']))

    return render_template('insert_shelter.html', message=message, site=site)

#edit the information of the shelter {shelter_id}
@app.route('/update_shelter/<site_id>', methods=['GET', 'POST'])
@login_required
def update_shelter(site_id):
    old_data = format_bunks(shelters.get_bunk(site_id))[0]

    message = "Please check the shelter information before modification."

    if request.method=='POST':
        desc = request.form['description'].strip()
        hours = request.form['hours'].strip()
        conditions = request.form['conditions'].strip()

        malecount = request.form['malecount'].strip()
        femalecount = request.form['femalecount'].strip()
        mixedcount = request.form['mixedcount'].strip()

        shelterId = old_data['shelterId']

        shelter_is_changed = not(desc=='' and hours=='' and conditions=='')
        bunk_is_changed = not(malecount=='' and femalecount=='' and mixedcount=='') 

        if not shelter_is_changed and not bunk_is_changed:
            message = "You change nothing. Please input new infomation"

            return render_template('update_shelter.html', message=message, old=old_data)

        if shelter_is_changed:
            if desc=='':
                desc = old_data['shelter']
            if hours=='':
                hours = old_data['hours']
            if conditions=='':
                conditions = old_data['conditions']

            shelters.update_shelter(shelterId, desc, hours, conditions)

        if bunk_is_changed:
            if malecount=='':
                malecount = old_data['male']
            if femalecount=='':
                femalecount = old_data['female']
            if mixedcount=='':
                mixedcount = old_data['mixed']

            shelters.update_bunks(shelterId, malecount, femalecount, mixedcount)

        return redirect(url_for('show_shelter', site_id=site_id))

    return render_template('update_shelter.html', message=message, old=old_data)

#show information the foodbank {foodbank-id}
@app.route('/foodbank/<foodbank_id>', methods=['GET', 'POST'])
@login_required
def show_foodbank(foodbank_id):
    items_data = format_items(items.get_items_by_foodbank(foodbank_id))

    #siteId = session['siteId']
    siteId = foodbanks.get_foodbank_siteId(foodbank_id)

    reqs = format_requests(requests.outstanding_requests(siteId))

    message = "Pending requests in your site: "

    if request.method=='POST':
        postid = request.form['postid']
        
        if not RepresentsInt(postid):
            if postid == 'qtysort':
                reqs = format_requests(requests.outstanding_requests_by_qty(siteId))
            elif postid == 'catsort':
                reqs = format_requests(requests.outstanding_requests_by_subcat(siteId))
            elif postid == 'storesort':
                reqs = format_requests(requests.outstanding_requests_by_store(siteId))
            else:
                reqs = format_requests(requests.outstanding_requests(siteId))

            return render_template('show_foodbank.html', items=items_data, reqs=reqs, message=message)

        else:
            quan = request.form['quantity'].strip()
            if int(postid)>0:
                itemId = postid

                if quan=='' or not RepresentsInt(quan) or int(quan)<0:
                    flash("Please input a non-negative integer.")
                    
                    return render_template('show_foodbank.html', items=items_data, reqs=reqs, message=message)

                elif int(quan)==0:

                    item_requests = requests_on_item(itemId)

                    if len(item_requests)<1:
                        print "len: ", len(item_requests)
                        items.delete_item(itemId)

                    else:
                        for reqId in item_requests:
                            requests.update_request_out(reqId)

                        items.update_item_count(itemId, 0)

                    return redirect(url_for('show_foodbank', foodbank_id=foodbank_id))

                else:
                    items.update_item_count(itemId, quan)

                    return redirect(url_for('show_foodbank', foodbank_id=foodbank_id))

            else:
                reqId = 0 - int(postid)

                if quan=='' or not RepresentsInt(quan) or int(quan)<0:
                    flash("Please input a non-negative integer.")

                    return render_template('show_foodbank.html', items=items_data, reqs=reqs, message=message)

                else:
                    to_approval_num = int(quan)

                    requested_item = items.get_requsted_item(reqId)
                    itemId = requested_item[0]
                    item_num = int(requested_item[1])

                    req_num = int(requests.get_request_quan(reqId))

                    approved_num = min(item_num, req_num, to_approval_num)

                    updated_item_num = item_num - approved_num

                    if to_approval_num > approved_num:
                        flash("Your input is more than request or stock. Only minimal amount is approved.")

                    if item_num == approved_num:

                        if item_num == req_num:
                            status = "closed"
                        else:
                            status = "partial, out ot stock"

                    elif req_num == approved_num:
                        status = "closed"

                    else:
                        status = "partial"

                    items.update_item_count(itemId, updated_item_num)

                    requests.approve_request(reqId, approved_num, status, session['id'])

                    return redirect(url_for('show_foodbank', foodbank_id=foodbank_id))

    return render_template('show_foodbank.html', items=items_data, reqs=reqs, message=message)

#show the user {user_id}'s requests
@app.route('/requests_by_user/<user_id>', methods=['GET', 'POST'])
@login_required
def show_requests_by_user(user_id):
    userRequests = format_requests(requests.get_requests_by_user(user_id))
    message = "Requests created by you: "

    if request.method=='POST':
        postid = request.form['update']

        if int(postid)<0:
            req_id = 0 - int(postid)
            requests.cancel_request(req_id)

            return redirect(url_for('show_requests_by_user', user_id=user_id))

        else:
            quan = request.form['quantity'].strip()
            req_id = request.form['update']

            if quan=='' or not RepresentsInt(quan) or int(quan)<0:
                flash("Please input a non-negative integer.")
                
                return render_template('show_requests.html', reqs=userRequests, message=message)

            elif int(quan)==0:
                requests.cancel_request(req_id)

                return redirect(url_for('show_requests_by_user', user_id=user_id))

            else:
                requests.update_request(req_id, quan)

                return redirect(url_for('show_requests_by_user', user_id=user_id))

    return render_template('show_requests.html', reqs=userRequests, message=message)

#client enrollment
@app.route('/enroll_client', methods=['GET', 'POST'])
@login_required
def enroll_client():

    message = "Please check the client's information before enrollment."

    if request.method == 'POST':
        name = request.form['clientname'].strip()
        desc = request.form['description'].strip()
        phone = request.form['phone'].strip()

        if name=='' or desc=='' or phone=='':
            message = "Please input all the fields."

        else: 
            clients.insert_client(name, desc, phone)

            message = "You have successfully enrolled " + name + " as a client!"
    
    return render_template('enroll_client.html', message=message)

#search clients through clients' name and/or description
@app.route('/search_clients', methods=['GET', 'POST'])
@login_required
def search_clients():
    message = "Please input search information."

    if request.method == 'POST':
        name = request.form['clientname'].strip()
        desc = request.form['description'].strip()

        if name=='' and desc=='':
            message = "You are searching nothing."

            return render_template('search_clients.html', message=message)

        else:
            clients_data = clients.search_clients(name, desc)

            clients_data = format_clients(clients_data)

            return render_template('show_clients.html', clients=clients_data)
    
    return render_template('search_clients.html', message=message)

#Show a client's information
@app.route('/show_client/<client_id>', methods=['GET', 'POST'])
@login_required
def show_client(client_id):
    client_data = clients.get_client(client_id)

    client_data = format_clients(client_data)[0]

    checkin_logs = format_checkin_logs(clientLogs.get_checkin_logs(client_id))

    modify_logs = format_modify_logs(clientLogs.get_modify_logs(client_id))

    return render_template('show_client.html', client=client_data, checkins=checkin_logs, modifies=modify_logs)

#update a client's information
@app.route('/update_client/<client_id>', methods=['GET', 'POST'])
@login_required
def update_client(client_id):

    old_data = format_clients(clients.get_client(client_id))[0]

    message = "Please check the client's information before modification."

    if request.method == 'POST':
        notes = ""
        name = request.form['clientname'].strip()
        desc = request.form['description'].strip()
        phone = request.form['phone'].strip()

        change = 0

        if name == '':
            name = old_data['name']

        elif name != old_data['name']:
            notes += "Name modified: " + name + "(original: " + old_data['name'] + " ). "
            change += 1

        if desc == '':
            desc = old_data['desc']

        elif desc != old_data['desc']:
            notes += "Description modified: " + desc + "(original: " + old_data['desc'] + " ). "
            change += 1

        if phone == '':
            phone = old_data['phone']

        elif phone != old_data['phone']:
            notes += "Phone modified: " + phone + "(original: " + old_data['phone'] + " ). "
            change += 1

        if change == 0:
            message = "You changed nothing."

        else:

            clients.update_client(client_id, name, desc, phone)

            clientLogs.insert_client_modification_log(client_id, notes)

            return redirect(url_for('show_client', client_id=client_id))
    
    return render_template('update_client.html', message=message, old=old_data)

#Check-In a client
@app.route('/checkin_client/<client_id>', methods=['GET', 'POST'])
@login_required
def checkin_client(client_id):
    site_id = session['siteId']

    client_data = format_clients(clients.get_client(client_id))[0]
    bunk_data = shelters.get_bunk(site_id)

    has_foodpantry = sites.has_service(site_id, 'foodPantries')
    has_shelter = sites.has_service(site_id, 'shelters')
    has_soupkitchen = sites.has_service(site_id, 'soupKitchens')

    if has_shelter:
        bunk_data = format_bunks(shelters.get_bunk(session['siteId']))[0]
    else:
        bunk_data = {}

    message = "Welcome, " + client_data['name'] + "! Please select some services."

    if request.method == 'POST':
        notes = "Service used: "

        if has_foodpantry:
            fp = request.form['foodpantry']
            if int(fp) == 1:
                notes += "Food Pantry; "

        if has_soupkitchen:
            sk = request.form['soupkitchen']
            if int(sk) == 1:
                notes += "Soup Kitchen; "

        if has_shelter:

            if bunk_data['male'] + bunk_data['female'] + bunk_data['mixed'] >= 1:

                bunk = request.form['bunk']

                if bunk != 'notuse':
                    notes += "shelter; "

                    if bunk == 'maleCount':
                        bunkCount = bunk_data['male'] - 1

                    elif bunk == 'femaleCount':
                        bunkCount = bunk_data['female'] - 1

                    else:
                        bunkCount = bunk_data['mixed'] - 1

                    shelterId = shelters.get_shelter_id(session['siteId'])
                    print "shelterId: " + str(shelterId)

                    shelters.update_bunk(shelterId, bunk, bunkCount)

        note = request.form['note'].strip()

        notes += "Notes: " + note

        clientLogs.insert_client_checkin_log(client_id, session['siteId'], notes)

        return redirect(url_for('show_client', client_id=client_id))

    return render_template('checkin_client.html', client=client_data, bunk=bunk_data, has_foodpantry=has_foodpantry, has_soupkitchen=has_soupkitchen, message=message)

####################################################
#Help methods
def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def requests_on_item(item_id):
    reqs = requests.get_item_requestId(item_id)

    reqs_id = []

    for req in reqs:
        reqs_id.append(req[0])

    return reqs_id

def format_users(data):
    users = []

    for row in data:
        users.append ({
            'id':row[0],
            'username': row[1],
            'password': row[2],
            'email': row[3],
            'fullname': row[4],
            'site': row[5]
        })

    return users

def format_items(data):
    items_data = []

    for item in data:

        items_data.append({
            'itemId': item[0],
            'itemName': item[1],
            'quantity': item[4],
            'subcategory': item[2],
            'storage': item[3],
            'expiration': item[5],
            'siteId': item[6],
            'siteName': item[7]
            })

    return items_data

def format_sites(data):
    sites_data = []

    for site in data:
        sites_data.append({
            'siteId': site[0],
            'siteName': site[1],
            'street': site[2],
            'city': site[3],
            'state': site[4],
            'zip': site[5],
            'phone': site[6]
            })

    return sites_data

def format_requests(data):
    requests_data = []

    for req in data:
        if req[5]:
            requests_data.append({
                'requestId': req[0],
                'itemId': req[6],
                'requestQty': req[1],
                'providedQty': req[2],
                'foodBankId': req[7],
                'status': req[3],
                'makingUserId': req[4],
                'makingUsername': users.get_username(req[4]),
                'approvingUserId': req[5],
                'approvingUsername': users.get_username(req[5]),
                'itemName': req[8],
                'itemSite': req[9],
                'reqSite': sites.get_user_sitename(req[4])
                })
        else:
            requests_data.append({
                'requestId': req[0],
                'itemId': req[6],
                'requestQty': req[1],
                'providedQty': req[2],
                'foodBankId': req[7],
                'status': req[3],
                'makingUserId': req[4],
                'makingUsername': users.get_username(req[4]),
                'approvingUserId': req[5],
                'approvingUsername': None,
                'itemName': req[8],
                'itemSite': req[9],
                'reqSite': sites.get_user_sitename(req[4])
                })
    return requests_data

def format_clients(data):
    clients_data = []

    for client in data:
        clients_data.append({
            'id': client[0],
            'name':client[1],
            'desc':client[2],
            'phone':client[3]
            })
    return clients_data

def format_bunks(data):
    bunks = []

    for bunk in data:
        bunks.append({
            'siteName': bunk[1],
            'street': bunk[2],
            'city': bunk[3],
            'state': bunk[4],
            'zip': bunk[5],
            'phone': bunk[6],
            'shelter': bunk[7],
            'hours': bunk[8],
            'conditions': bunk[9],
            'shelterId': bunk[10],
            'male': bunk[11],
            'female': bunk[12],
            'mixed': bunk[13]
            })

    return bunks

def format_checkin_logs(data):
    logs = []

    for log in data:
        logs.append({
            'id': log[0],
            'time': log[1],
            'site': log[2],
            'notes': log[3]
            })

    return logs

def format_modify_logs(data):
    logs = []

    for log in data:
        logs.append({
            'id': log[0],
            'time': log[1],
            'notes': log[2]
            })

    return logs

def format_foodpantries(data):
    pantries = []

    for pantry in data:
        pantries.append({
            'id': pantry[0],
            'description': pantry[1],
            'hours': pantry[2],
            'conditions': pantry[3],
            'siteId': pantry[4],
            'siteName': pantry[5]
            })

    return pantries

def format_soupkitchens(data):
    kitchens = []

    for kitchen in data:
        kitchens.append({
            'id': kitchen[0],
            'description': kitchen[1],
            'hours': kitchen[2],
            'conditions': kitchen[3],
            'seats': kitchen[4],
            'siteId': kitchen[5],
            'siteName': kitchen[6]
            })

    return kitchens

#########################################################
#temp routes used for testing
"""
#Show all users
@app.route('/users', methods=['GET'])
@login_required
def show_users():
    users_data = format_users(users.get_users())
    return render_template('show_users.html', users=users_data)

#show all sites
@app.route('/sites', methods=['GET'])
@login_required
def show_sites():
    sites_data = format_sites(sites.get_sites())
    return render_template('show_sites.html', sites=sites_data)

@app.route('/sites/<site_id>')
@login_required
def show_site(site_id):
    site_data = format_sites(sites.get_site(site_id))[0]

    return render_template('show_site.html', site=site_data)

@app.route('/outstanding_requests/<username>')
@login_required
def outstanding_requests(username):

    user_data = format_users(users.get_user(username))[0]

    siteId = user_data['site']

    reqs = format_requests(requests.outstanding_requests(siteId))

    message = "Pending requests in your site: "

    return render_template('show_requests.html', reqs=reqs, message=message)


@app.route('/cancel_request/<request_id>')
@login_required
def cancel_request(request_id):
    requests.cancel_request(request_id)

    return "You have canceled the request: " + request_id
"""
"""
@app.route('/category/<cat_id>', methods=['GET'])
def show_cat(cat_id):
    return categories.get_category(cat_id)

@app.route('/subcat/<subcat_id>', methods=['GET'])
def show_subcat(subcat_id):
    tp = subCategories.get_subCategory(subcat_id)
    return tp[0]

@app.route('/foodbank_site/<fb_id>', methods=['GET'])
def show_foodbank_site(fb_id):
    return str(foodbanks.get_foodbank_siteId(fb_id))

@app.route('/bunk/<site_id>', methods=['GET'])
def show_bunk(site_id):
    return str(shelters.get_bunk(site_id)[0])

@app.route('/show_user_info')
def show_user_info():
    return session['username']

@app.route('/show_username/<user_id>')
def show_username(user_id):
    return users.get_username(user_id)

@app.route('/foodbank/item/<item_id>', methods=['GET'])
def show_item_foodbank(item_id):
    fb = items.get_item_foodbank(item_id)

    return str(fb)

@app.route('/has_service/<siteId>')
def has_service(siteId):
    #num = sites.has_service(siteId, 'foodBanks')
    num = sites.calculate_services(siteId)
    return str(num)

@app.route('/get_requested_item/<req_id>')
def get_requsted_item(req_id):
    data = items.get_requsted_item(req_id)

    return str(data)

@app.route('/submit_request', methods=['GET', 'POST'])
def request_item():

    if request.method == 'POST':
        requestedQty = int(request.form['quantity'])
        makingUserFk = int(request.form['user'])
        #category = request.form['category']
        itemIdFk = int(request.form['item'])
        foodBankIdFk = int(request.form['foodbank'])

        print type(requestedQty), type(makingUserFk), type(itemIdFk), type(foodBankIdFk)
        print requestedQty, makingUserFk, itemIdFk, foodBankIdFk

        #items.insert_item(itemName, subcategory, storage, quantity, expiration, foodbank)
        requests.insert_request(requestedQty, makingUserFk, itemIdFk, foodBankIdFk)

    return render_template('request_item.html')

@app.route('/items/<foodbank_id>', methods=['GET'])
def show_items_foodbank(foodbank_id):
    return str(items.get_items_by_foodbank(foodbank_id))

@app.route('/items/search/<expression>', methods=['GET'])
def show_items_search(expression):
    return str(items.search_items(expression))
"""
##########################################################

if __name__ == '__main__':
	app = run()
