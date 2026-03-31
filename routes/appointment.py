from flask import Blueprint, request, session, redirect
from models import mysql

appointment_bp = Blueprint('appointment', __name__)

@appointment_bp.route('/add_appointment', methods=['POST'])
def add_appointment():
    patient_id = request.form['patient_id']
    doctor_id = request.form['doctor_id']
    date = request.form['date']
    tenant_id = session.get('tenant_id')

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO appointments(patient_id, doctor_id, date, tenant_id) VALUES(%s,%s,%s,%s)",
        (patient_id, doctor_id, date, tenant_id)
    )
    mysql.connection.commit()

    return redirect('/dashboard')