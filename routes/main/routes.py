from app import app, db
from models import Departaments, Employees
from flask import render_template, request, redirect

@app.route('/', methods=["GET"] )
def index():
    return render_template('index.html')
