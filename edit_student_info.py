from flask import Blueprint, render_template,request,session, redirect, url_for
from flask_pymongo import MongoClient
# import bcrypt
from dbconnect import * 

edit_info_BP = Blueprint('edit_info', __name__)

# Set up MongoDB connection
client = MongoClient(mongoclient)
db = client[dbname]
print(db)


# Sample user data for demonstration purposes
# users = {
#     "user1": "password1",
#     "user2": "password2",
#     "admin": "admin"
# }






@edit_info_BP.route('/edit', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        # roll_number = request.form['roll_number']
        # password = request.form['password']
        email = request.form['email']

        mobile_number = request.form['mobile_number']
        linkedin_id = request.form['linkedin_id']
        other_link = request.form['other_link']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        percentage_10 = request.form['percentage_10']
        school_name_10 = request.form['school_name_10']
        edu_board_10 = request.form['edu_board_10']
        school_10_addr = request.form['school_10_addr']

        yop_10 = request.form['yop_10']
        percentage_12 = request.form['percentage_12']
        school_name_12 = request.form['school_name_12']
        school_12_addr = request.form['school_12_addr']
        edu_board_12 = request.form['edu_board_12']
        yop_12 = request.form['yop_12']
        subject_12 = request.form['subject_12']
        # roll_number = request.form['roll_number']
        clg_university_name = request.form['clg_university_name']
        clg_university_yos = request.form['clg_university_yos']
        clg_university_yop = request.form['clg_university_yop']
        clg_university_addr = request.form['clg_university_addr']
        course = request.form['course']
        clg_marks = request.form['clg_marks']


        branch = request.form['branch']
        gender = request.form['gender']
        # skills = request.form['skills']

        roll_number = session['roll_number']
        # existing_user = db.users.find_one({"roll_number": roll_number})
        # if existing_user:
        #     # User exists, update the information
        #     db.users.update_one({"roll_number": roll_number}, {"$set": {"first_name": first_name,"last_name": last_name}})
        #     print("User information updated.")
        # else:
            # User does not exist, store the new user information
            # Here you would typically add code to store the user's information in a database
            # hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        if middle_name != '':
            user_data  = {'first_name':first_name, 'middle_name':middle_name,'last_name':last_name, 'dob':dob,'email':email,'mobile_number':mobile_number,'address':address, 'linkedin_id':linkedin_id, 'other_link':other_link,'city':city,'state':state,'country':country,'percentage_10':percentage_10,'school_name_10':school_name_10,'school_10_addr':school_10_addr,'edu_board_10':edu_board_10,'yop_10':yop_10,'percentage_12':percentage_12,'school_name_12':school_name_12, 'school_12_addr':school_12_addr,'subject_12':subject_12,'edu_board_12':edu_board_12,'yop_12':yop_12,'clg_university_name':clg_university_name, 'clg_university_addr':clg_university_addr, 'clg_university_yos':clg_university_yos,'clg_university_yop':clg_university_yop,'course':course,'branch':branch, 'clg_marks':clg_marks,'gender':gender}
        else:
            user_data  = {'first_name':first_name, 'last_name':last_name,  'dob':dob,'email':email,'mobile_number':mobile_number,'address':address, 'linkedin_id':linkedin_id,'other_link':other_link,'city':city,'state':state,'country':country,'percentage_10':percentage_10,'school_name_10':school_name_10,'school_10_addr':school_10_addr,'edu_board_10':edu_board_10,'yop_10':yop_10,'percentage_12':percentage_12,'school_name_12':school_name_12, 'school_12_addr':school_12_addr,'subject_12':subject_12,'edu_board_12':edu_board_12,'yop_12':yop_12,'clg_university_name':clg_university_name, 'clg_university_addr':clg_university_addr,'clg_university_yos':clg_university_yos,'clg_university_yop':clg_university_yop,'course':course,'branch':branch, 'clg_marks':clg_marks,'gender':gender}

            # user_data = { str(i):i for i in data }
            # user_data['password'] = hashed_password
        print(user_data)
        # user_data = {'first_name': first_name, 'last_name': last_name, "roll_number": roll_number,'password': hashed_password, 'email': email}
        # db.users.insert_one(user_data)
        db.users.update_one({"roll_number": roll_number}, {"$set": user_data})
        # new_user = {'first_name':first_name,'last_name':last_name,'age':age}
        # db.users.insert_one(new_user)
        print("User information Updated.")
        return redirect(url_for('log.profile'))
        # return redirect(url_for('hello_admin'))
        # return render_template("login.html")
    roll_number = session['roll_number']
    user_data = db.users.find_one({"roll_number": roll_number})
    return render_template('edit_student_info.html', data = user_data)