from flask import Blueprint, render_template, request, session, redirect
from models import mysql

patient_bp = Blueprint('patient', __name__)

@patient_bp.route('/dashboard')
def dashboard():
    tenant_id = session.get('tenant_id')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patients WHERE tenant_id=%s", (tenant_id,))
    patients = cur.fetchall()

    return render_template('dashboard.html', patients=patients)


@patient_bp.route('/add_patient', methods=['POST'])
def add_patient():
    name = request.form['name']
    age = request.form['age']
    disease = request.form['disease']
    tenant_id = session.get('tenant_id')

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO patients(name, age, disease, tenant_id) VALUES(%s,%s,%s,%s)",
        (name, age, disease, tenant_id)
    )
    mysql.connection.commit()

    return redirect('/dashboard')