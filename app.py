from flask import Flask, render_template, request, redirect, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'carts'

def create_connection():
    try:
        con = mysql.connector.connect(
            host='localhost',
            database='enrollment',
            user='root',
            password=''
        )
        if con.is_connected():
            return con
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/enroll', methods=['POST'])
def enroll():
    name = request.form['name'].upper()
    age = request.form['age']
    gender = request.form['gender'].upper()
    address = request.form['address'].upper()
    birthdate = request.form['birthdate']
    email = request.form['email']
    course = request.form['course']
    balance = request.form['balance']

    # Connect to the database
    con = create_connection()
    if con is None:
        flash('Could not connect to the database!', 'error')
        return redirect('/')

    cur = con.cursor()

    try:
        # Check if student is already enrolled
        cur.execute("SELECT COUNT(*) FROM students_enroll WHERE Fullname = %s", (name,))
        if cur.fetchone()[0] > 0:
            flash('This student is already enrolled!', 'error')
            return redirect('/')

        # Insert the new student
        cur.execute(""" 
            INSERT INTO students_enroll (Fullname, Age, Gender, Address, Birtdate, Email, Course, Balance) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
        """, (name, age, gender, address, birthdate, email, course, balance))

        con.commit()
        flash('Enrollment successful!', 'success')
    except Error as e:
        flash(f"Error: {e}", 'error')
    finally:
        cur.close()
        con.close()

    return redirect('/')

@app.route('/show')
def show_student():
    # Connect to the database
    con = create_connection()
    if con is None:
        flash('Could not connect to the database!', 'error')
        return redirect('/')

    cur = con.cursor()

    try:
        # Fetch all students
        cur.execute("SELECT * FROM students_enroll")
        students = cur.fetchall()
    except Error as e:
        flash(f"Error: {e}", 'error')
        students = []
    finally:
        cur.close()
        con.close()

    return render_template('show.html', students=students)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
