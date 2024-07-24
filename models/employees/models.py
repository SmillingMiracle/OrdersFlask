from app import db

class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(300), nullable=False)
    phone_number = db.Column(db.String(300), nullable=False)
    hire_date = db.Column(db.Integer, default=False)
    job_id = db.Column(db.Integer, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    comission_pct = db.Column(db.Integer, nullable=False)
    manager_id = db.Column(db.Integer, nullable=False)
    departament_id = db.Column(db.Integer, nullable=False)
    #висвітлення рядка
    def __repr__(self):
        return '<Employees %r>' % self.id
