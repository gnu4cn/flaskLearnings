from sqlalchemy import MetaData
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

convention = {
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constrant_names)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
        }

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)

