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
