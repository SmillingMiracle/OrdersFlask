from app import app, db
from models import Employees
from flask import render_template, request, redirect, session
from flask_login import login_user, login_required, logout_user

@app.route('/create-employee', methods=['POST','GET'])
@login_required
def create_employee():
    #отримує дані з реквесту
    if request.method == 'POST':

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        job_id = request.form['job_id']
        salary = request.form['salary']
        comission_pct = request.form['comission_pct']
        manager_id = request.form['manager_id']
        departament_id = request.form['departament_id']

        employee = Employees(first_name=first_name,
                             last_name=last_name,
                             email=email,
                             phone_number=phone_number,
                             job_id=job_id,
                             salary=salary,
                             comission_pct=comission_pct,
                             manager_id=manager_id,
                             departament_id=departament_id)

        try:
            #добавити в базу даних
            db.session.add(employee)
            #зберегти
            db.session.commit()
            return redirect('/employees')
        except:
            return "Error Employee Add"
    else:
        return render_template('create-employee.html')


@app.route('/employees', methods=["GET"] )
def employees():
    employees = Employees.query.order_by(Employees.id.desc()).all()
    return render_template('employees.html', employees=employees)

@app.route('/employee/<int:id>', methods=["GET"] )
def employee_detail(id):
    employee = Employees.query.get(id)
    return render_template('employee_detail.html', employee=employee)

@app.route('/employee/<int:id>/delete', methods=["GET"] )
def employee_delete(id):
    employee = Employees.query.get_or_404(id)
    try:
        db.session.delete(employee)
        db.session.commit()
        return redirect('/employees')
    except:
        return "Error for delete Employee"

@app.route('/employee/<int:id>/update', methods=['POST','GET'])
def employee_update(id):

    employee = Employees.query.get(id)
    #отримує дані з реквесту
    if request.method == 'POST':
        employee.first_name = request.form['first_name']
        employee.last_name = request.form['last_name']
        employee.email = request.form['email']
        employee.phone_number = request.form['phone_number']
        employee.job_id = request.form['job_id']
        employee.salary = request.form['salary']
        employee.comission_pct = request.form['comission_pct']
        employee.manager_id = request.form['manager_id']
        employee.departament_id = request.form['departament_id']

        try:
            #зберегти
            db.session.commit()
            return redirect('/employees')
        except:
            return "Error update employees "
    else:
        employee = Employees.query.get(id)
        return render_template('employee_update.html', employee=employee)

