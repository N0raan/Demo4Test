from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy  
import sqlite3
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///School.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subject = db.Column(db.String(120), nullable=False)
    webURL = db.Column(db.String(120), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<contact {self.name}>'
        
def get_db_connection():
    conn = sqlite3.connect('DemoII.db')
    conn.row_factory = sqlite3.Row
    return conn
    
def init_db():
    with app.app_context():
        db.create_all()
        conn = get_db_connection()
        with app.open_resource('DBModel.sql', mode='r') as f:
            conn.executescript(f.read())
        conn.close()

@app.route('/')
def home():
    return render_template('index.html', title='Home Page')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        webURL = request.form['webURL']
        text = request.form['text']
        
        new_contact = Contact(name=name, email=email, subject=subject, webURL=webURL, text=text)
        
        db.session.add(new_contact)
        db.session.commit()

        return redirect(url_for('home'))
    else:
        return render_template('contact.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True,port=8080)
