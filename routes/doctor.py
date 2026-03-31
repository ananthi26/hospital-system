from flask import Blueprint, request, session, redirect
from models import mysql

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/add_doctor', methods=['POST'])
def add_doctor():
    name = request.form['name']
    specialization = request.form['specialization']
    tenant_id = session.get('tenant_id')

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO doctors(name, specialization, tenant_id) VALUES(%s,%s,%s)",
        (name, specialization, tenant_id)
    )
    mysql.connection.commit()

    return redirect('/dashboard')