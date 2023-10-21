#main code
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)

class Shortage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, nullable=False)
    staff_type = db.Column(db.String(20), nullable=False)
    details = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text)
    waiting_time = db.Column(db.String(20))

# For simplicity, assume there are two roles: 'Principal' and 'Secretary'
# You can expand upon this as needed

@app.route('/')
def index():
    users = User.query.all()
    shortages = Shortage.query.all()
    return render_template('index.html', users=users, shortages=shortages)

@app.route('/report_shortage', methods=['POST'])
def report_shortage():
    school_id = request.form['school_id']
    staff_type = request.form['staff_type']
    details = request.form['details']

    new_shortage = Shortage(school_id=school_id, staff_type=staff_type, details=details)
    db.session.add(new_shortage)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

#html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shortage Report System</title>
</head>
<body>
    <h1>Shortage Report System</h1>

    <h2>Users</h2>
    <ul>
        {% for user in users %}
            <li>{{ user.username }} ({{ user.role }})</li>
        {% endfor %}
    </ul>

    <h2>Reported Shortages</h2>
    <ul>
        {% for shortage in shortages %}
            <li>
                School ID: {{ shortage.school_id }} |
                Staff Type: {{ shortage.staff_type }} |
                Details: {{ shortage.details }}
            </li>
        {% endfor %}
    </ul>

    <h2>Report Shortage</h2>
    <form action="{{ url_for('report_shortage') }}" method="post">
        <label for="school_id">School ID:</label>
        <input type="text" id="school_id" name="school_id" required><br>

        <label for="staff_type">Staff Type:</label>
        <input type="text" id="staff_type" name="staff_type" required><br>

        <label for="details">Details:</label>
        <textarea id="details" name="details" required></textarea><br>

        <button type="submit">Submit</button>
    </form>
</body>
</html>

#generating data analysis

from flask import Flask, render_template, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from io import StringIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Shortage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, nullable=False)
    staff_type = db.Column(db.String(20), nullable=False)
    details = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text)
    waiting_time = db.Column(db.String(20))

@app.route('/generate_quarterly_report')
def generate_quarterly_report():
    # Fetch data from the database
    shortages = Shortage.query.all()

    # Convert data to a Pandas DataFrame
    df = pd.DataFrame([(s.id, s.school_id, s.staff_type, s.details, s.response, s.waiting_time) for s in shortages],
                      columns=['ID', 'School ID', 'Staff Type', 'Details', 'Response', 'Waiting Time'])

    # Generate CSV from the DataFrame
    csv_data = df.to_csv(index=False)

    # Create a response object with the CSV data
    response = Response(
        csv_data,
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=quarterly_report.csv'}
    )

    return response

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

