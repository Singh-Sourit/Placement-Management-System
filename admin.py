from flask import Blueprint, render_template,request, redirect, url_for, session
from flask_pymongo import MongoClient
# import smtplib
import datetime
from dbconnect import * 


admin_bp = Blueprint('admin', __name__)

# Set up MongoDB connection
client = MongoClient(mongoclient)
db = client[dbname]
print(db)


@admin_bp.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_profile():
    # roll_number = session['roll_number']
    if session['roll_number'] == 'admin':
        companies = db.companies.find()
        count_companies = db.companies.count_documents({}) 
        count_students = db.users.count_documents({}) 
        all_mails = db.mails.find()
        return render_template('admin_dashboard.html', companies = companies, count_companies = count_companies, count_students=count_students, mails = all_mails)
    # return render_template('company_list.html',companies = companies)

@admin_bp.route('/add_company', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        company = {'name': name, 'description': description}
        db.companies.insert_one(company)
        # companies.append({'name': name, 'description': description})
        return redirect(url_for('company.company_list'))
    return render_template('add_company.html')

@admin_bp.route('/student_list')
def student_list():
    # Here you can retrieve and display the list of registered students
    students = db.users.find()  # Retrieve student data from your database
    return render_template('student_list_2.html', students=students)


@admin_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    # Remove 'username' from the session to log out the user
    # session.pop('first_name', None)
    # session.pop('last_name', None)
    session.pop('roll_number', None)
    # session.pop('email', None)
    return redirect(url_for('main.index'))


@admin_bp.route('/send_email', methods=['POST'])
def send_email():
        if request.method == 'POST':
            subject = request.form['subject']
            message = request.form['message']
            dateTime = str(datetime.datetime.now())
            mail = {'date':dateTime[0:10], 'time':dateTime[11:16],'subject': subject, 'message': message}
            db.mails.insert_one(mail)
            return redirect(url_for('admin.admin_profile'))



@admin_bp.route('/delete_mail/<string:date>/<string:time>')
def delete_skill(date,time):
    # roll_number = session['roll_number']
    # student = db.users.find_one({"roll_number": roll_number})
    # skill_to_delete = 
    # # Update the document to remove the skill
    # db.mails.update_one(
    #     {"date": date},
    #     {"$pull": {"student_skills": {"skill_name": skill_name}}}
    # )
    db.mails.delete_one({
    "$and": [
        {"date": date},
        {"time": time}
        ]
    })
    return redirect(url_for('admin.admin_profile'))


@admin_bp.route('/<string:roll_number>')
def view_profile(roll_number):
    if "admin" == session.get("roll_number"):
        student_data = db.users.find_one({'roll_number': roll_number})
        return render_template('Student_Profile_admin.html',user = student_data)
    return url_for('log.profile')












    # try:
        # sender_email = request.form['sender_email'] #'your_email@gmail.com'  # Your email address
        # sender_password = request.form['sender_password'] #'your_password'  # Your email password
        # recipient_email = request.form['recipient_email']

        # # Connect to the SMTP server (in this case, Gmail)
        # smtp = smtplib.SMTP('smtp.gmail.com', 587)
        # smtp.starttls()
        # smtp.login(sender_email, sender_password)

        # # Create the email
        # email = f'Subject: {subject}\n\n{message}'

        # # Send the email
        # smtp.sendmail(sender_email, recipient_email, email)

        # # Close the connection
        # smtp.quit()

    #     return 'Email sent successfully'
    # except Exception as e:
    #     print('Error sending email:',e)
    #     return f'Error sending email: {str(e)}'