from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def model_to_dict(inst, cls):
    convert = dict()
    d = dict()
    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error: Failed to convert using ", str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v
    return d


class ModelMixin(object):
    def __repr__(self):
        return unicode(self.__dict__)

    @property
    def to_dict(self):
        return model_to_dict(self, self.__class__)

class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)

    def __init__(self, username):
        self.username = username
