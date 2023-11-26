from flask import Blueprint, render_template,request,session
from flask_pymongo import MongoClient
from dbconnect import * 

resumeBP = Blueprint('resume', __name__)

# Set up MongoDB connection
client = MongoClient(mongoclient)
db = client[dbname]
print(db)



@resumeBP.route('/resume',methods=['GET', 'POST'])
def generate_resume():
    print("INSIDE")
    # if request.method == 'POST':
    roll_number = session['roll_number']
    user_data = db.users.find_one({"roll_number": roll_number})
    # textA = request.form['textA']
    return render_template('resumeReady.html', user=user_data )
    # return render_template('resume.html')

