from flask import Blueprint, render_template, request, redirect, session, url_for
from flask_pymongo import MongoClient
from dbconnect import * 

student_bp = Blueprint('student', __name__)

# Set up MongoDB connection
client = MongoClient(mongoclient)
db = client[dbname]
print(db)

# @student_bp.route('/student_info', methods=['GET', 'POST'])
# def student_info():
#     if request.method == 'POST':
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
#         age = request.form['age']
#         email = request.form['email']
        
#         roll_number = session['roll_number']
#         # Here you can add code to process and store student information
        
#         # User already exists, update the information
#         db.users.update_one({"roll_number": roll_number}, {"$set": {"first_name":first_name ,"last_name": last_name,"age":age,"email":email}})
#         print("User information updated.")
#         user_data = db.users.find_one({"roll_number": roll_number})
#         return render_template('Student_profile.html', notification = "User information updated.", user = user_data )
      

#     roll_number = session['roll_number']
#     user_data = db.users.find_one({"roll_number": roll_number})
#     return render_template('student_form.html', user = user_data)


@student_bp.route('/delete_project',methods=['GET', 'POST']) 
def delete_project():
    if request.method == 'POST':

        value = request.form['mySelect']
        # print(project_name)
        # Retrieve the student document by its ObjectId
        roll_number = session['roll_number']
        student = db.users.find_one({"roll_number": roll_number})

        deleted_project = student["projects"].pop(int(value)-1)
        print(deleted_project)

        # Update the student document in MongoDB
        a = db.users.update_one({"roll_number": roll_number}, {"$set": student})

    return redirect(url_for('log.profile'))


@student_bp.route('/delete_skill/<string:skill_name>')
def delete_skill(skill_name):
    roll_number = session['roll_number']
    student = db.users.find_one({"roll_number": roll_number})
    # skill_to_delete = 
    # Update the document to remove the skill
    db.users.update_one(
        {"roll_number": roll_number},
        {"$pull": {"student_skills": {"skill_name": skill_name}}}
    )
    return redirect(url_for('log.profile'))
# ---------------------------------------------------------------------

@student_bp.route('/add_projects', methods=['GET', 'POST'])
def add_projects():
    if request.method == 'POST':
        # Get project data from the form (project_name and project_details will be lists)
        project_names = request.form.getlist('project_name[]')
        project_details = request.form.getlist('project_details[]')

        # Create a list of project dictionaries
        projects = [{"project_name": name, "project_details": details} for name, details in zip(project_names, project_details)]

        # Find the student document and add the projects to their 'projects' array
        roll_number = session['roll_number']

        result = db.users.update_one(
            {"roll_number": roll_number},
            {"$push": {"projects": {"$each": projects}}}
        )

        return redirect(url_for('log.profile'))
    

# ----------------------------------------------------------------------

@student_bp.route('/add_skills', methods=['GET', 'POST'])
def add_skills():
    if request.method == 'POST':
        # Get project data from the form (project_name and project_details will be lists)
        skill_names = request.form.getlist('skill_name[]')
        # project_details = request.form.getlist('project_details[]')

        # Create a list of project dictionaries
        skills = [{"skill_name": name} for name in skill_names]

        # Find the student document and add the projects to their 'projects' array
        roll_number = session['roll_number']

        result = db.users.update_one(
            {"roll_number": roll_number},
            {"$push": {"student_skills": {"$each": skills}}}
        )

        return redirect(url_for('log.profile'))


@student_bp.route('/delete_student/<string:roll_number>')
def delete_student(roll_number):
    db.users.delete_one({'roll_number':roll_number})
    return redirect(url_for('admin.student_list'))


@student_bp.route('/delete_company/<string:company_name>')
def delete_company(company_name):
    db.companies.delete_one({'company_name':company_name})
    return redirect(url_for('admin.admin_profile'))

@student_bp.route('/apply/<string:company_name>')
def apply(company_name):
    roll_number = session['roll_number']
    if roll_number != 'admin':
        db.users.update_one({"roll_number": roll_number},{"$set": {company_name: "True"}})
        db.companies.update_one({"company_name": company_name},{"$push": {"Applied": roll_number}})
        return redirect(url_for('company.company_info',cname = company_name))
    else:
        company_data = db.companies.find_one({'company_name': company_name})
        students_list = company_data
        return render_template('Applied_Students.html',cname = company_name, students_list = students_list )
        #


#/delete_project/{{ user.roll_number }}/{{ project_index }}

    # Check if the student exists
    # if student:
    #     # Check if the project index is valid
    #     if 0 <= counter < len(student.get("projects", [])):
    #         # Remove the specified project from the list
    #         deleted_project = student["projects"].pop(counter)

    #         # Update the student document in MongoDB
    #         db.users.update({"roll_number": roll_number}, {"$set": student})

    # return redirect(url_for('log.profile'))
#             # Optionally, you can redirect back to the student profile page


# @student_bp.route('/save', methods=['POST'])
# def save_data():
#     data = {}
#     # d1 = {}
#     # print(request.form.items())


#     for key, value in request.form.items():
#         print(key)
#         data[key] = value
#         # data.append(data)

#         roll_number = session['roll_number']
#         # new_data = {'projects':data}
#         print("DATA => ",data)
#         # projects =[data]
#         # Insert the data into MongoDB
#     db.users.update_one({"roll_number": roll_number}, {"$push": {"project":data}})
#     # collection.insert_one(data)

#     return redirect(url_for('log.profile'))