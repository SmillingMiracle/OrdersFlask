from app import app, db
from models import User, Message
from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user

@app.route('/user', methods=["GET"] )
@login_required
def user():
    user = User.query.order_by(User.id.desc()).all()
    return render_template('user.html', user=user)

@app.route('/user/<int:id>/delete', methods=["GET"] )
@login_required
def user_delete(id):
    user = User.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect('/user')
    except:
        return "Error for delete User"


@app.route('/user/<int:id>/update', methods=['POST','GET'])
@login_required
def user_update(id):

    user = User.query.get(id)
    #отримує дані з реквесту
    if request.method == 'POST':
        user.login = request.form['login']
        user.password = generate_password_hash(request.form['password'])
        try:
            #зберегти
            db.session.commit()
            return redirect('/user')
        except:
            return "Error update user "
    else:
        user = User.query.get(id)
        return render_template('user_update.html', user=user)
