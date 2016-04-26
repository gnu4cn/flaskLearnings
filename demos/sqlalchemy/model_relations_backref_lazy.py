class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    addresses = ad.relationship('Address',
            backref=db.backref('person', lazy='joined'), lazy='dynamic')
