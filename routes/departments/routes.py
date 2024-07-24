from app import app, db
from models import Departaments, Employees
from flask import render_template, request, redirect
from flask_login import login_user, login_required, logout_user


@app.route('/create-departament', methods=['POST','GET'])
@login_required
def create_department():
    #отримує дані з реквесту
    if request.method == 'POST':

        departaments_name=request.form['departaments_name']
        manager_id=request.form['manager_id']
        location_id=request.form['location_id']
        department =(
            Departaments(
                departaments_name=departaments_name,
                manager_id=manager_id,
                location_id=location_id
            ))

        try:
            #добавити в базу даних
            db.session.add(department)
            #зберегти
            db.session.commit()
            return redirect('/departments')
        except:
            return "Error"
    else:
        return render_template('create-departament.html')

@app.route('/departments', methods=["GET"] )
def departments():
    departments = Departaments.query.all()
    return render_template('departments.html', departments=departments)


@app.route('/departments/<int:id>', methods=["GET"] )
def department_detail(id):
    department = Departaments.query.get(id)
    return render_template('post-detail.html', departments=departments)

@app.route('/departments/<int:id>/delete', methods=["GET"] )
def department_delete(id):
    department = Departaments.query.get_or_404(id)
    try:
        db.session.delete(department)
        db.session.commit()
        return redirect('/departments')
    except:
        return "Error for delete departments"

@app.route('/departments/<int:id>/update', methods=['POST','GET'])
def department_update(id):
    department = Departaments.query.get(id)
    #отримує дані з реквесту
    if request.method == 'POST':
        department.departaments_name=request.form['departaments_name']
        department.manager_id=request.form['manager_id']
        department.location_id=request.form['location_id']

        try:
            #зберегти
            db.session.commit()
            return redirect('/departments')
        except:
            return "Error update department"
    else:
        department = Departaments.query.get(id)
        return render_template('department_update.html', department=department)
