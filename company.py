from flask import Blueprint, render_template, request,url_for, redirect, session
from flask_pymongo import MongoClient
import datetime
from dbconnect import * 

company_bp = Blueprint('company', __name__)

# Set up MongoDB connection
client = MongoClient(mongoclient)
db = client[dbname]
print(db)
companies = db.companies.find()

# companies = [
#     {'name': 'Company A', 'description': 'A software development company'},
#     {'name': 'Company B', 'description': 'An e-commerce platform'},
#     {'name': 'Company C', 'description': 'A renewable energy company'}
# ]

@company_bp.route('/company_list')
def company_list():
    companies = db.companies.find()
    roll_number = session['roll_number']
    data = db.users.find_one({"roll_number": roll_number})
    return render_template('company_list.html',companies = companies, data = data)

@company_bp.route('/addCompany', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        company_name = request.form['company_name']
        website = request.form['website']
        qualification = request.form['qualification']
        job_profile = request.form['job_profile']
        role = request.form['role']
        skills = request.form['skills']
        location = request.form['location']
        benefits = request.form['benefits']
        salary = request.form['salary']


        dateTime = str(datetime.datetime.now())
        company_data = {'date':dateTime[0:10], 'company_name':company_name,'website':website,'qualification':qualification,'job_profile':job_profile,'role':role,'skills':skills,'location':location,'benefits':benefits,'salary':salary}

        db.companies.insert_one(company_data)
        print("company data saved")

        # company_Data =  db.companies.find_one({'name': company_name}) # code to fetch the company data using company name
        # # print(company_Data)
        # return render_template('companyInfo.html', companydata = company_Data)

        # return(render_template('companyInfo.html',))
        # return url_for(company_info(company_name))
        # return company_info(company_name)
        # return url_for("/viewCompany/{{company['company_name']}}")

        return redirect(url_for('company.company_info', cname=company_name))
    

    return render_template('companyDataEntry.html')

# @company_bp.route('/viewCompany/<string:cname>')
# def company_info(cname):
#     # print(cname)
#     company_Data =  db.companies.find_one({'company_name': cname}) # code to fetch the company data using company name
#     # print(company_Data)
#     return render_template('companyInfo.html', companydata = company_Data)

@company_bp.route('/viewCompany/<string:cname>')
def company_info(cname):
    
    company_Data =  db.companies.find_one({'company_name': cname}) # code to fetch the company data using company name
    roll_number = session['roll_number']
    if roll_number == 'admin':
        return render_template('companyInfo.html', companydata = company_Data, apply = 'View Applied Students')
    
    result = db.users.find_one({ "roll_number": roll_number, cname: { "$exists": True } })
    if result != None:
        return render_template('companyInfo.html', companydata = company_Data, apply = 'Applied')
    else:
        return render_template('companyInfo.html', companydata = company_Data, apply = 'Apply')


# @company_bp.route('/CompanyAppliedList')
# def companyAppliedList():
#     roll_number = session['roll_number']
#     student = db.users.find_one({"roll_number": roll_number})


# @company_bp.route('/addCompanySubmit', methods=['GET', 'POST'])
# def add_company_submit():
#     if request.method == 'POST':
#         company_name = request.form['company_name']
#         website = request.form['website']
#         qualification = request.form['qualification']
#         job_profile = request.form['job_profile']
#         role = request.form['role']
#         skills = request.form['skills']
#         location = request.form['location']
#         benefits = request.form['benefits']
#         salary = request.form['salary']

#         company_data = {'company_name':company_name,'website':website,'qualification':qualification,'job_profile':job_profile,'role':role,'skills':skills,'location':location,'benefits':benefits,'salary':salary}

#         db.companies.insert_one(company_data)
#         print("company data saved")

#         return company_info(company_name)
#     return url_for('company.add_company')