from flask import Flask, render_template, request, flash  # Import Flask modules for creating the web app
from flask_sqlalchemy import SQLAlchemy  # Import SQLAlchemy for database operations
from datetime import datetime  # Import datetime for handling date objects
import os
from flask_mail import Mail, Message

# Create the Flask application
app = Flask(__name__)

# Set the secret key for session security and other cryptographic purposes
app.config["SECRET_KEY"] = "myapp321"

# Configure the database URI for SQLite using SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"

app.config["MAIL_PORT"] = 465
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "ikedichukwu1993@gmail.com"
app.config["MAIL_PASSWORD"] = os.getenv("PASSWORD")

# Initialize SQLAlchemy with the Flask app
db = SQLAlchemy(app)

mail = Mail(app)


# Define the Form model, representing the database table
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each record
    first_name = db.Column(db.String(80))  # First name field
    last_name = db.Column(db.String(80))  # Last name field
    email = db.Column(db.String(80))  # Email field
    date = db.Column(db.Date)  # Date field for storing dates
    occupation = db.Column(db.String(80))  # Occupation field


# Define the route for the home page, supporting both GET and POST requests
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":  # Handle form submission via POST request
        # Retrieve form data from the request object
        first_name = request.form.get("first_name")  # Get the first name
        last_name = request.form.get("last_name")  # Get the last name
        email = request.form.get("email")  # Get the email
        date = request.form.get("date")  # Get the date string from the form
        date_obj = datetime.strptime(date, "%Y-%m-%d")  # Convert date string to datetime object
        occupation = request.form.get("occupation")  # Get the occupation

        # Create a new Form object with the submitted data
        form = Form(first_name=first_name, last_name=last_name, email=email,
                    date=date_obj, occupation=occupation)

        # Add the new record to the database session
        db.session.add(form)

        # Commit the session to save changes to the database
        db.session.commit()

        message_body = f"{first_name} Thank you for your submission"
        message = Message(subject="New form submission", sender=app.config["MAIL_USERNAME"],
                          recipients=[email], body=message_body)

        mail.send(message)
        flash(f"{first_name} Your form was sent successfully!", "success")

        # Print the form data to the console (for debugging purposes)


    # Render the index.html template for GET requests or after handling POST
    return render_template("index.html")


# Main entry point for running the Flask app
if __name__ == "__main__":
    with app.app_context():  # Ensure the app context is available for database setup
        db.create_all()  # Create all database tables based on the models
        app.run(debug=True, port=5001)  # Start the app with debugging enabled, on port 5001
