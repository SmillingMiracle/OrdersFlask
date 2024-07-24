from app import app, db
from models import User, Message
from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        #перший вже і так унікальний юзер
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            # момент вже авторизованого юзера
            login_user(user)

            #повертає на сторінку яка була до реєстрації
            next_page = request.args.get('next')

            return redirect(next_page)


        else:
            #flash - висвітлює помилки з центру коду
            flash('Login or password is not correct')
    else:
        flash('Please fill login and password fields')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # get оскільки поле може бути пустим
    login = request.form.get('login')
    password = request.form.get('password')
    password_repeat = request.form.get('password_repeat')

    if request.method == 'POST':
        if not (login or password or password_repeat):
            flash('Please, fill all fields!')
        elif password != password_repeat:
            print(password, password_repeat)
            flash('Passwords are not equal!')
        else:
            # хешування паролю
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()
            #перевод користувача на вхіж
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/logout', methods=['GET', 'POST'])
# потребує бути авторизованим
@login_required
def logout():
    logout_user()
    flash("You leave your account see u later!")
    return redirect(url_for('login_page'))


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    return render_template('profile.html')
    #return f"""user info: {current_user.get_id()} """



@app.route('/main', methods=['GET'])
@login_required
def main():
    return render_template('main.html', messages=Message.query.all())


@app.route('/add_message', methods=['POST'])
@login_required
def add_message():
    text = request.form['text']
    tag = request.form['tag']

    db.session.add(Message(text, tag))
    db.session.commit()

    return redirect(url_for('main'))