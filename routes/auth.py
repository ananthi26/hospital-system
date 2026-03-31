from flask import Blueprint, render_template, request, redirect, session
from models import mysql

auth_bp = Blueprint('auth', __name__)

# LOGIN
@auth_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email, password)
        )
        user = cur.fetchone()

        if user:
            session['user_id'] = user[0]
            session['tenant_id'] = user[5]
            return redirect('/dashboard')

    return render_template('login.html')


# DASHBOARD (VERY IMPORTANT)
@auth_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    tenant_id = session.get('tenant_id')

    cur = mysql.connection.cursor()

    # 🔹 Fetch Patients
    cur.execute("SELECT * FROM patients WHERE tenant_id=%s", (tenant_id,))
    patients = cur.fetchall()

    # 🔹 Fetch Doctors
    cur.execute("SELECT * FROM doctors WHERE tenant_id=%s", (tenant_id,))
    doctors = cur.fetchall()

    # 🔹 Fetch Appointments
    cur.execute("SELECT * FROM appointments WHERE tenant_id=%s", (tenant_id,))
    appointments = cur.fetchall()

    return render_template(
        'dashboard.html',
        patients=patients,
        doctors=doctors,
        appointments=appointments
    )


# LOGOUT
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/')