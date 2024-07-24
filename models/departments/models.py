from app import db


class Departaments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    departaments_name = db.Column(db.String(100), nullable=False)
    manager_id = db.Column(db.Integer, nullable=False)
    location_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Departaments %r>' % self.id