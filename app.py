
from flask import Flask,render_template, flash, redirect, url_for, session, request, logging
from passlib.hash import  sha256_crypt
from datetime import  datetime
from functools import  wraps

from db_connection import  db_connection
from forms import RegisterForm, RepurposeForm
import pymongo
from bson.objectid import ObjectId


app = Flask(__name__)

# conn = db_connection

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=('GET','POST'))
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        conn = db_connection()

        cur = conn.dove.users
        cur.insert({'name': name, 'username': username,
                    'email': email, 'password': password})

        conn.close()
        flash("You are now registered, you may log in", "success")
        return  redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_candidate = request.form['password']
        # connect to the db
        client = pymongo.MongoClient()
        db = client.dove
        # create cursor
        # cursor = db.users.find({'username': username})

        results = db.users.find({'username': username})
        # results = db.users.find()
        num_records = int(results.count())
        app.logger.info("NUMBER OF RECORDS {0} ".format(results.count()))
        if num_records > 0:
            data = results.next()
            password = data['password']
            # app.logger.info('RESULTS {}'.format(data['password']))
            if sha256_crypt.verify(password_candidate, password):
                app.logger.info('PASSWORD MATCHED')
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return  redirect(url_for('dashboard'))
            else:
                app.logger.info('PASSWORD NOT MATCHED')
                error = 'Invalid login'
                return render_template('login.html', error=error)

        else:
            app.logger.info('USER NOT FOUND')
            error = 'Username not found'
            return render_template('login.html', error=error)
    return render_template('login.html')
# Check login status

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return  wrap

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You have logged out of the system', 'danger')
    return redirect(url_for('login'))

@app.route('/dashboard')
@is_logged_in
def dashboard():
    client = pymongo.MongoClient()
    db = client.dove
    results = db.repurposed_drugs.find()

    if int(results.count()) >0:
        return  render_template('dashboard.html', drugs=results)
    else:
        msg='No Drugs in the Database'
        render_template('dashboard.html')


    return render_template('dashboard.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/diseases')
def diseases():
    return render_template('diseases.html')

@app.route('/api')
def api():
    return render_template('api.html')

@app.route('/download')
def download():
    return render_template('download.html')

#  Add a repurpose record into the database
@app.route('/add_drug', methods=('GET','POST'))
@is_logged_in
def addDrug():
    form = RepurposeForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        chem_id = form.chem_id.data
        drugbank_id = form.drugbank_id.data
        org_indication = form.org_indication.data
        new_indication = form.new_indication.data
        evidence = form.evidence.data
        pubmed_id = form.pubmed_id.data
        website = form.website.data
        additional_info = form.additional_info.data

        client = pymongo.MongoClient()
        db = client.dove

        db.repurposed_drugs.insert({'name': name,
                                    'chem_id': chem_id,
                                    'drugbank_id': drugbank_id,
                                    'org_indication': org_indication,
                                    'new_indication': new_indication,
                                    'evidence': evidence,
                                    'pubmed_id': pubmed_id,
                                    'website': website,
                                    'additional_info': additional_info,
                                    'added_by': session['username'],
                                    'created_date': datetime.now()})
        flash("New drug saved", "success")
        return  redirect(url_for('dashboard'))
    return render_template('repurpose.html', form=form)

@app.route('/edit_drug/<string:id>', methods=('GET','POST'))
@is_logged_in
def editDrug(id):
    form = RepurposeForm
    client = pymongo.MongoClient()
    db = client.dove

    drug = db.repurposed_drugs.find_one({'_id':ObjectId(id)})

    form = RepurposeForm(request.form)
    #  populate fields

    form.name.data = drug['name']
    form.drugbank_id.data = drug['drugbank_id']
    form.chem_id.data = drug['chem_id']
    form.pubmed_id.data = drug['pubmed_id']
    form.org_indication.data = drug['org_indication']
    form.new_indication.data = drug['new_indication']
    form.evidence.data = drug['evidence']
    form.website.data = drug['website']
    form.additional_info.data = drug['additional_info']
    # client.close()

    if request.method == 'POST' and form.validate():
        name = request.form['name']
        drugbank_id = request.form['drugbank_id']
        pubmed_id = request.form['pubmed_id']
        result = db.repurposed_drugs.find()
        app.logger.info(result)
        db.repurposed_drugs.update(
            {'_id': ObjectId(id)},
            { '$set': {
                "name":name,
                "drugbank_id":drugbank_id,
                "pubmed_id":pubmed_id
        }},
        upsert=False, multi=False)

        flash("Drug data updated successfully", "success")
        return  redirect(url_for('dashboard'))
    else:
        app.logger.info('NOTHING TO SHOW')
    return  render_template('edit_drug.html', form=form)


@app.route('/delete_drug/<string:id>', methods=['POST', 'GET'])
@is_logged_in
def deleteDrug(id):
    # if request.method == 'POST':
    client = pymongo.MongoClient()
    db = client.dove
    flash("Record successfully deleted!","success")
    drug = db.repurposed_drugs.delete_one({'_id':ObjectId(id)})
    return  redirect(url_for('dashboard'))


if __name__ == "__main__":
    app.secret_key = 'bigboy'
    app.run(debug=True)
