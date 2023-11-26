from flask import Blueprint, render_template,request,session, redirect, url_for
from flask_pymongo import MongoClient
import bcrypt
from dbconnect import * 

loginBP = Blueprint('log', __name__)

# Set up MongoDB connection
client = MongoClient(mongoclient)
db = client[dbname]
print(db)


def project(data):
     # Retrieve student project details from MongoDB
    project_names = []
    project_descs = []
    count_of_project = []
    # Define the maximum number of project_name fields you expect
    max_input_count = 3 #- count_of_project # Change this to the maximum expected count

    for input_count in range(1, max_input_count + 1):
        pro_name = f'project_name_{input_count}'
        pro_desc = f'project_desc_{input_count}'
        if pro_name in data:
            project_names.append(data[pro_name])
            project_descs.append(data[pro_desc])
            count_of_project.append(input_count)

        # project_data_name = list(db.users.find({pro_name: {'$exists': True}}, {pro_name: 1, '_id': 0}))
        # project_data_desc = list(db.users.find({pro_desc: {'$exists': True}}, {pro_desc: 1, '_id': 0}))
        
        # if project_data_name and project_data_desc:
        #     project_names.extend(project_data_name)
        #     project_descs.extend(project_data_desc)
    # count_of_project = len(project_names)
    data = zip(project_names, project_descs)
    return data





@loginBP.route('/profile',methods=['GET','POST'])
def profile():
    print('inside profile')
    roll_number = session['roll_number']
    if roll_number == 'admin':
        return redirect(url_for('admin.admin_profile'))
    all_mails = db.mails.find()
    data = db.users.find_one({"roll_number": roll_number})
    # project_details= project(data)
    return render_template('Student_profile.html', user = data, mails = all_mails)

# Define a route for the login page
@loginBP.route('/login', methods=['GET', 'POST'])
def login():
    if not session.get("roll_number"):
        
        if request.method == 'POST':

            roll_number = request.form['roll_number']
            password = request.form['password']

            admin = db.admin.find_one({'name': roll_number})
            if roll_number == 'admin' and admin['password'] == password:
                session['roll_number'] = roll_number
                return redirect(url_for('admin.admin_profile'))

            # if username in users and users[username] == password:
            #     return render_template('Student_profile.html', username = username)
            # else:
            #     return "Invalid username or password. Please try again."

            user = db.users.find_one({'roll_number': roll_number})
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                session['roll_number'] = roll_number
                return redirect(url_for('log.profile'))
                # user_data = db.users.find_one({"roll_number": roll_number})
                # return profile(user_data)
                # return redirect(url_for('log.profile', data = user_data))
                # return redirect(url_for('cricket', favteam=team))
                # return render_template('Student_profile.html', user = user_data)
            else:
                return "Invalid username or password. Please try again."
    else:
        return redirect(url_for('log.profile'))

    return render_template('login.html')


@loginBP.route('/logout', methods=['GET', 'POST'])
def logout():
    # Remove 'username' from the session to log out the user
    # session.pop('first_name', None)
    # session.pop('last_name', None)
    # session.pop('roll_number', None)
    # session.pop('email', None)
    session.clear()
    return redirect(url_for('main.index'))

