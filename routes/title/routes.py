import os

from werkzeug.utils import secure_filename

from app import app, db, ALLOWED_EXTENSIONS
from models import User, Message, Title
from flask import render_template, redirect, url_for, request, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           # return redirect(url_for('upload_file', ilename=filename))
            return filename

    return render_template('upload.html')

@app.route('/title', methods=["GET"] )
@login_required
def title():
    title = Title.query.all()
    return render_template('title.html', title=title)

@app.route('/title_create', methods=['POST'])
def title_create():
    id_user = current_user.get_id()
    description = request.form.get('description')
    filename = upload_file()

    title = Title(id_user=id_user, description=description, filename=filename)
    db.session.add(title)
    db.session.commit()

    return redirect(url_for('title'))