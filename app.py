from flask import Flask
from index import *
from student import *
from company import *
from registration import *
from admin import *
from resume import *
from flask_session import Session
from login import *
from edit_student_info import *

# Create a Flask web application instance
app = Flask(__name__)

app.register_blueprint(bp)
app.register_blueprint(student_bp)
app.register_blueprint(company_bp)
app.register_blueprint(resumeBP)
app.register_blueprint(regisBP)
app.register_blueprint(loginBP)
app.register_blueprint(admin_bp)
app.register_blueprint(edit_info_BP)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
