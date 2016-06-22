# -*- coding: utf-8 -*-
# from flask_sqlalchemy import SQLAlchemy
from languages import lang
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, \
    SignatureExpired, BadSignature
from flask import jsonify
from datetime import datetime, date
from constant import ROLE_USER, MALE, TOKEN_EXPIRE
from appdemo import db
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.orm import MapperExtension
# from sqlalchemy.ext.declarative import declared_attr
from constant import PRSN_CAT as p_c, POSITION as po, DEPARTMENT as de, \
    SERVICE as se, TRNEE_RANK as t_r, RELATION as re, RELIGION as rel, \
    GENDER as ge, MARRIAGE as ma, PPRT_TYPE as p_t, CERT_TYPE as c_t, \
    EDU as edu
# 引入名词复数形式
from inflect import engine as inflectEngine


# 这是为了last_updated
class MapperExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        instance.created_at = datetime.now()
        instance.last_updated = datetime.now()

    def before_update(self, mapper, connection, instance):
        instance.created_at = instance.created_at
        instance.last_updated = datetime.now()

# 使用db实例中的app属性
app = db.app

dbSession = db.session


def get_u_id_from_cred(cred):
    token = cred[0:-7]
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None
    except BadSignature:
        return None

    return data['id']


def foreign_key(table):
    '''类修饰器，将一个外键加入到某个SQLAlchemy模型。
    参数table是一个one-to-many关系的目的数据表，而数据表table就是'one'侧。
    '''
    def ref_table(cls):
        pl = inflectEngine().plural
        setattr(cls, '{0}_id'.format(table),
                db.Column(db.Integer, db.ForeignKey('{0}.id'.format(table))))
        setattr(cls, table,
                db.relationship(table.capitalize(),
                                backref=db.backref(pl(cls.__name__.lower()),
                                                   lazy='dynamic')))
        return cls

    return ref_table


def foreign_key_one_to_one(table):
    '''类修饰器，将一个外键加入到某个SQLAlchemy模型。
    参数table是一个one-to-one关系的parent数据表。
    注意：无需在parent表中加入关系了。
    '''
    def ref_table(cls):
        setattr(cls, '{0}_id'.format(table),
                db.Column(db.Integer, db.ForeignKey('{0}.id'.format(table))))
        setattr(cls, table,
                db.relationship(table.capitalize(),
                                backref=db.backref(cls.__name__.lower(),
                                                   uselist=False)))
        return cls

    return ref_table


# db = SQLAlchemy()


# The final model_to_dict
def model_to_dict(inst, cls):
    convert = dict()
    d = dict()

    if (super(cls, inst) is not None) & \
            (hasattr(super(cls, inst), '__table__')):

        for c in super(cls, inst).__table__.columns:
            v = getattr(inst, c.name)
            if c.type in convert.keys() and v is not None:
                try:
                    d[c.name] = convert[c.type](v)
                except:
                    d[c.name] = "Error: Failed to convert using ", \
                        str(convert[c.type])
            elif v is None:
                d[c.name] = str()
            else:
                d[c.name] = v

    for c in cls.__table__.columns:
        v = getattr(inst, c.name)
        if c.type in convert.keys() and v is not None:
            try:
                d[c.name] = convert[c.type](v)
            except:
                d[c.name] = "Error: Failed to convert using ", \
                    str(convert[c.type])
        elif v is None:
            d[c.name] = str()
        else:
            d[c.name] = v

    return d


class BaseMixin(object):
    id = db.Column(db.Integer, primary_key=True)
    last_updated = db.Column(db.DateTime, onupdate=datetime.now,
                             default=datetime.now)

    created_at = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return model_to_dict(self, self.__class__)

    @classmethod
    def get_by_id(self, r_id):
        q = self.query.get(r_id)
        return jsonify(q.to_dict())

    @classmethod
    def get_list(self):
        r = []
        qs = self.query.all()

        for q in qs:
            r.append(q.to_dict())

        return jsonify(r)


# http://stackoverflow.com/questions/15534147/python-inheritance-in-sqlalchemy
# the mixin must come first!!!
class Account(BaseMixin, db.Model):
    '''
    用户表，存储了用户名、一卡通卡号、密码，用户角色。与个人资料相关联。
    '''
    username = db.Column(db.String(32), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    person_type = db.Column(db.String(1))

    def generate_auth_token(self, expiration=TOKEN_EXPIRE):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @classmethod
    def verify_auth_cred(self, cred):
        user_id = get_u_id_from_cred(cred)
        if user_id is not None:
            return self.query.get(user_id)
        return None

    # 为何这里必须用静态方法？
    @staticmethod
    def check_auth_token_expired(cred, locale):
        r = {}

        if get_u_id_from_cred(cred) is not None:
            r['success'] = True
        else:
            r['success'] = False
            r['message'] = lang.get_item('CredentialIncorrectOrExpired',
                                         locale)

        return jsonify(r)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @classmethod
    def login(self, username, password, locale):
        r = {}
        user = self.query.filter_by(username=username).first()

        if not user or not user.verify_password(password):
            r['success'] = False
            r['message'] = lang.get_item('UsernameNotExistorPasswordNotCorrect',
                                         locale)

        else:
            r['success'] = True
            r['token'] = user.generate_auth_token()
            r['message'] = lang.get_item('LoginedSuccessful', locale)

        return jsonify(r)

    @classmethod
    def check_username(self, testUsername):
        r = {}
        r['success'] = True
        if(self.query.filter_by(username=testUsername).first() is not None):
            r['exists'] = True
        else:
            r['exists'] = False

        return jsonify(r)

    @classmethod
    def get_by_credential(self, cred, locale):
        r = {}

        user = self.verify_auth_cred(cred)
        if user is not None:
            r['user'] = user.to_dict()
            r['user']['category'] = p_c.get_by_id(user.person_type, locale)
            r['profile'] = {
                '0': lambda: user.staff.profile(locale),
                '1': lambda: user.sfamily.profile(locale),
                '5': lambda: user.trainee.profile(locale),
                '6': lambda: user.tfamily.profile(locale)
            }[user.person_type]()

            r['success'] = True
            r['message'] = lang.get_item('GetUserAccountInfoSuccessfully',
                                         locale)

        else:
            r['success'] = False
            r['message'] = lang.get_item('FailedtoGetUserAccountInfo', locale)

        return jsonify(r)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    @classmethod
    def profile_existed(self, category, idNumber='', passportNumber=''):
        return {
            '0': lambda: Staff.is_existed(idNumber),
            '1': lambda: Sfamily.is_existed(idNumber),
            '5': lambda: Trainee.is_existed(passportNumber),
            '6': lambda: Tfamily.is_existed(passportNumber),
        }[category]()

    def _staff(self, staff):
        self.staff = staff

    def _sfamily(self, sfamily):
        self.sfamily = sfamily

    def _trainee(self, trainee):
        self.trainee = trainee

    def _tfamily(self, tfamily):
        self.tfamily = tfamily

    @classmethod
    def create(self, username, password, category, firstName, lastName,
               idNumber, sexality, countryId, pNumber, locale):
        '''
        这里要建立帐号、及初始化用户个人资料。
        '''
        '''先检查是否已存在个人资料所管理的帐号，这要在用户输入身份证或护照号时
        去检查比较好。
        '''
        r = {}
        u = Account(username, password, category)
        dbSession.add(u)
        {
            '0': lambda: u._staff(Staff(id_number=idNumber,
                                        f_name=firstName,
                                        l_name=lastName)),
            '1': lambda: u._sfamily(Sfamily(id_number=idNumber,
                                            f_name=firstName,
                                            l_name=lastName)),
            '5': lambda: u._trainee(Trainee(country_id=countryId,
                                            gender=sexality,
                                            passport_number=pNumber,
                                            f_name=firstName,
                                            l_name=lastName)),
            '6': lambda: u._tfamily(Tfamily(country_id=countryId,
                                            gender=sexality,
                                            passport_number=pNumber,
                                            f_name=firstName,
                                            l_name=lastName)),
        }[category]()

        try:
            dbSession.commit()
            r['success'] = True
            r['message'] = lang.get_item('createUserSuccessfully', locale)
        except:
            r['success'] = False
            r['message'] = lang.get_item('ErrorOccuredWhenWriteDB', locale)

        return jsonify(r)

    def __init__(self, username, password, category):
        self.username = username
        self.hash_password(password)
        self.person_type = category

    __mapper_args__ = {
        'extension': MapperExtension(),
    }


@foreign_key('account')
class Media(BaseMixin, db.Model):
    title = db.Column(db.String(64))
    description = db.Column(db.String(140))
    filesize = db.Column(db.Integer)
    uri = db.Column(db.String(255), nullable=False)

    def __init__(self, title='', description='', filesize=0, uri=0):
        self.title = title
        self.description = description
        self.filesize = filesize
        self.uri = uri

    __mapper_args__ = {
        'extension': MapperExtension(),
        'polymorphic_identity': 'media'
    }


class Image(Media):
    id = db.Column(db.Integer, db.ForeignKey(Media.id, ondelete='cascade'),
                   primary_key=True)
    width = db.Column(db.SmallInteger)
    height = db.Column(db.SmallInteger)

    def __init__(self, width=0, height=0, *args, **kwargs):
        super(Image, self).__init__(*args, **kwargs)
        self.width = width
        self.height = height

    __mapper_args__ = {
        'polymorphic_identity': 'image'
    }


class Audio(Media):
    id = db.Column(db.Integer, db.ForeignKey(Media.id, ondelete='cascade'),
                   primary_key=True)
    duration = db.Column(db.DECIMAL('9,2'))

    def __init__(self, duration=0, *args, **kwargs):
        super(Audio, self).__init__(*args, **kwargs)
        self.duration = duration

    __mapper_args__ = {
        'polymorphic_identity': 'audio'
    }


class Video(Media):
    id = db.Column(db.Integer, db.ForeignKey(Media.id, ondelete='cascade'),
                   primary_key=True)
    duration = db.Column(db.DECIMAL('9,2'))

    def __init__(self, duration=0, *args, **kwargs):
        super(Video, self).__init__(*args, **kwargs)
        self.duration = duration

    __mapper_args__ = {
        'polymorphic_identity': 'video'
    }


class Province(BaseMixin, db.Model):
    pinyin = db.Column(db.String(64))
    hanzi = db.Column(db.String(64))

    def __init__(self, pinyin, hanzi):
        self.pinyin = pinyin
        self.hanzi = hanzi


@foreign_key('province')
class City(BaseMixin, db.Model):
    pinyin = db.Column(db.String(64))
    hanzi = db.Column(db.String(64))

    def get(self):
        r = {}
        r = self.to_dict()
        r['province'] = self.province.to_dict()

        return r


class Language(BaseMixin, db.Model):
    code = db.Column(db.String(3))
    en_name = db.Column(db.String(256))
    zh_name = db.Column(db.String(256))
    native_name = db.Column(db.String(128))

    # 建立一个到TraineeLanguage的父关系，以便对Trainee的语言情况进行统计
    social_edu_records = db.relationship('SocialEdu',
                                         secondary='trainee_language',
                                         lazy='dynamic',
                                         backref=db.backref('language',
                                                            lazy='dynamic'))

    def __init__(self, code='', en_name='', zh_name='', native_name=''):
        self.code = code
        self.en_name = en_name
        self.zh_name = zh_name
        self.native_name = native_name


@foreign_key('audio')
class Country(BaseMixin, db.Model):
    '''
    国家表（国歌都保存在Audio表中）。
    '''
    code = db.Column(db.String(3), unique=True)
    en_simp = db.Column(db.String(256), unique=True)
    en_full = db.Column(db.String(256), unique=True)
    zh_simp = db.Column(db.String(256), unique=True)
    zh_full = db.Column(db.String(256), unique=True)
    native_name = db.Column(db.String(256), unique=True)
    alpha_2 = db.Column(db.String(2), unique=True)
    alpha_3 = db.Column(db.String(3), unique=True)
    zoneprefix = db.Column(db.String(5))
    nationalDay = db.Column(db.Date)


class PersonMixin(BaseMixin):
    mobile = db.Column(db.String(11))
    f_name = db.Column(db.String(64))
    l_name = db.Column(db.String(80))


class IssuedCardPersonMixin(PersonMixin):
    card_number = db.Column(db.String(12))

ChinesePhoto = db.Table(
    'chinese_photo',
    db.Column('chinese_id', db.Integer,
              db.ForeignKey('chinese.id', ondelete='cascade'),
              primary_key=True),
    db.Column('photo_id',
              db.Integer, db.ForeignKey(Image.id, ondelete='cascade'),
              primary_key=True),
)


class Chinese(IssuedCardPersonMixin, db.Model):
    id_number = db.Column(db.String(18))
    photo = db.relationship('Image', secondary=ChinesePhoto,
                            lazy='dynamic',
                            backref=db.backref('chinese', lazy='dynamic'))

    @classmethod
    def is_existed(self, idNumber):
        r = {}

        r['success'] = True
        r['existed'] = False

        entity = self.query.filter_by(id_number=idNumber).first()

        if entity is not None:
            r['existed'] = True
            r['username'] = entity.account.username
            return jsonify(r)

        return jsonify(r)

    def __init__(self, id_number='', card_number='', mobile='', f_name='',
                 l_name=''):
        self.card_number = card_number
        self.id_number = id_number
        self.mobile = mobile
        self.f_name = f_name
        self.l_name = l_name

    __mapper_args__ = {
        'extension': MapperExtension(),
        'polymorphic_identity': 'chinese'
    }


@foreign_key_one_to_one('account')
class Staff(Chinese):
    id = db.Column(db.Integer,
                   db.ForeignKey(Chinese.id, ondelete='cascade'),
                   primary_key=True)

    position = db.Column(db.String(2))
    families = db.relationship('Sfamily', secondary='staff_sfamily',
                               lazy='dynamic',
                               backref=db.backref('staff', uselist=False))

    def _families(self, family):
        self.families.append(family)

    def profile(self, locale):
        r = {}
        r = self.to_dict()
        r['position'] = po.get_by_id(self.position, locale)

        r['families'] = []
        families = self.families
        if families is not None:
            for family in families:
                r['families'].append(family.to_dict())
        return r

    def __init__(self, position='00', *args, **kwargs):
        super(Staff, self).__init__(*args, **kwargs)
        self.position = position

    __mapper_args__ = {
        'extension': MapperExtension(),
        'polymorphic_identity': 'staff'
    }

Staff_Sfamily = db.Table(
    'staff_sfamily',
    db.Column('staff_id', db.Integer,
              db.ForeignKey('staff.id', ondelete='cascade'),
              primary_key=True),
    db.Column('sfamily_id', db.Integer,
              db.ForeignKey('sfamily.id', ondelete='cascade'),
              primary_key=True)
)


@foreign_key_one_to_one('account')
class Sfamily(Chinese):
    id = db.Column(db.Integer,
                   db.ForeignKey(Chinese.id, ondelete='cascade'),
                   primary_key=True)

    toStaff = db.relationship('Staff', secondary=Staff_Sfamily,
                              backref=db.backref('sfamily'))

    def _staff(self, staff):
        self.staff = staff

    def profile(self, locale):
        r = {}
        r = self.to_dict()

        staff = self.staff
        if staff is not None:
            r['staff'] = staff.to_dict()

        return r

    def __init__(self, *args, **kwargs):
        super(Sfamily, self).__init__(*args, **kwargs)

    __mapper_args__ = {
        'extension': MapperExtension(),
        'polymorphic_identity': 'staff_family',
    }

# 在此表登记来访国内人员
class ExternalChinese(Chinese):
    id = db.Column(db.Integer, db.ForeignKey(Chinese.id, ondelete='cascade'),
                   primary_key=True)
    work_place = db.Column(db.String(255))

    def __init__(self, work_place='', *args, **kwargs):
        super(ExternalChinese, self).__init__(*args, **kwargs)
        self.work_place = work_place

    __mapper_args__ = {
        'extension': MapperExtension(),
        'polymorphic_identity': 'external_chinese',
    }

ForeignerPhoto = db.Table(
    'foreigner_photo',
    db.Column('foreigner_id', db.Integer,
              db.ForeignKey('foreigner.id', ondelete='cascade'),
              primary_key=True),
    db.Column('photo_id', db.Integer,
              db.ForeignKey(Image.id, ondelete='cascade'), primary_key=True),
)


@foreign_key('country')
class Foreigner(IssuedCardPersonMixin, db.Model):
    gender = db.Column(db.String(1))
    passport_number = db.Column(db.String(12))
    visa_number = db.Column(db.String(10))
    photo = db.relationship('Image', secondary=ForeignerPhoto,
                            lazy='dynamic',
                            backref=db.backref('foreigner', lazy='dynamic'))

    @classmethod
    def is_existed(self, passportNumber):
        r = {}

        r['success'] = True
        r['existed'] = False

        entity = self.query.filter_by(passport_number=passportNumber).first()

        if entity is not None:
            r['existed'] = True
            r['username'] = entity.account.username
            return jsonify(r)

        return jsonify(r)

    def __init__(self, country_id=138, gender=MALE, passport_number='',
                 visa_number='', card_number='', mobile='', f_name='',
                 l_name=''):
        self.country_id = country_id
        self.gender = gender
        self.passport_number = passport_number
        self.visa_number = visa_number
        self.mobile = mobile
        self.f_name = f_name
        self.l_name = l_name

    __mapper_args__ = {
        'extension': MapperExtension(),
        'polymorphic_identity': 'foreigner',
    }


@foreign_key_one_to_one('account')
class Trainee(Foreigner):
    id = db.Column(db.Integer,
                   db.ForeignKey(Foreigner.id, ondelete='cascade'),
                   primary_key=True)
    birthday = db.Column(db.Date)
    student_id = db.Column(db.String(10))
    xingming = db.Column(db.String(24))

    families = db.relationship('Tfamily',
                               secondary='trainee_tfamily', lazy='dynamic',
                               backref=db.backref('trainee', uselist=False))

    def _career(self, career):
        self.career = career

    def _families(self, tfamily):
        self.families.append(tfamily)

    def _social_edu(self, social_edu):
        self.social_edu = social_edu

    def _physical(self, physical):
        self.physical = physical

    def _tpassport_visa(self, tpassport_visa):
        self.tpassport_visa = tpassport_visa

    def _relatives(self, relative):
        self.relatives.append(relative)

    def _trainings(self, training):
        self.trainings.append(training)

    def _workings(self, working):
        self.workings.append(working)

    def _abroadstudies(self, abroadstudy):
        self.abroadstudies.append(abroadstudy)

    def _contacts(self, contact):
        self.contacts.append(contact)

    def get(self, locale):
        r = {}
        r = self.to_dict()

        r['families'] = []
        families = self.families
        if families is not None:
            for family in families:
                r['families'].append(family.to_dict())

        career = self.career
        if career is not None:
            r['career'] = career

        social_edu = self.socialedu
        if social_edu is not None:
            r['social_edu'] = social_edu

        physical = self.physical
        if physical is not None:
            r['physical'] = physical

        tpassport_visa = self.tpassport_visa
        if tpassport_visa is not None:
            r['passport_visa'] = tpassport_visa

        r['relatives'] = []
        relatives = self.relatives
        if relatives is not None:
            for relative in relatives:
                r['relatives'].append(relative.get(locale))

        r['trainings'] = []
        trainings = self.trainings
        if trainings is not None:
            for training in trainings:
                r['trainings'].append(training.to_dict())

        r['workings'] = []
        workings = self.workings
        if workings is not None:
            for working in workings:
                r['workings'].append(working.to_dict())

        r['studys_abroad'] = []
        abroadstudies = self.abroadstudies
        if abroadstudies is not None:
            for study_abroad in abroadstudies:
                r['studys_abroad'].append(study_abroad.get())

        r['contacts'] = []
        contacts = self.contacts
        if contacts is not None:
            for contact in contacts:
                r['contacts'].append(contact.get())

        return r

    def __init__(self, country_id, birthday=date(1900, 1, 1),
                 student_id='', xingming='', *args, **kwargs):
        super(Trainee, self).__init__(*args, **kwargs)
        self.country_id = country_id
        self.birthday = birthday
        self.student_id = student_id
        self.xingming = xingming

    __mapper_args__ = {
        'extension': MapperExtension(),
        'polymorphic_identity': 'trainee'
    }


@foreign_key_one_to_one('trainee')
class Career(BaseMixin, db.Model):
    department = db.Column(db.String(255))
    position = db.Column(db.String(255))
    position_date = db.Column(db.Date)
    future_position = db.Column(db.String(255))
    rank = db.Column(db.String(4))

    def get(self, locale):
        r = {}
        r = self.to_dict()
        r['rank'] = t_r.get_by_id(self.rank, locale)

        return r

    def __init__(self, department='', position='',
                 position_date=date(1900, 1, 1), future_position='',
                 rank='0010'):
        self.department = department
        self.position = position
        self.position_date = position_date
        self.future_position = future_position
        self.rank = rank

    __mapper_args__ = {
        'extension': MapperExtension(),
    }

TraineeLanguage = db.Table(
    'trainee_language',
    db.Column('social_edu_id',
              db.Integer, db.ForeignKey('social_edu.id', ondelete='cascade'),
              primary_key=True),
    db.Column('language_id',
              db.Integer, db.ForeignKey('language.id', ondelete='cascade'),
              primary_key=True),
)


@foreign_key_one_to_one('trainee')
class SocialEdu(BaseMixin, db.Model):
    marriage = db.Column(db.String(1))
    religion = db.Column(db.String(2))
    education = db.Column(db.String(1))
    major = db.Column(db.String(255))
    college = db.Column(db.String(255))

    languages = db.relationship('Language', secondary=TraineeLanguage,
                                backref=db.backref('socical_edu',
                                                   uselist=False))

    def get(self, locale):
        r = {}
        r = self.to_dict()
        r['marriage'] = ma.get_by_id(self.marriage, locale)
        r['religion'] = rel.get_by_id(self.religion, locale)

        r['languages'] = []
        languages = self.languages
        if languages is not None:
            for language in languages:
                r['languages'].append(language.to_dict())

        return r

    def __init__(self, marriage='0', religion='00', education='3',
                 major='', college='', *args, **kwargs):
        self.marriage = marriage
        self.religion = religion
        self.education = education
        self.major = major
        self.college = college

    __mapper_args__ = {
        'extension': MapperExtension(),
    }


@foreign_key_one_to_one('trainee')
class Physical(BaseMixin, db.Model):
    height = db.Column(db.DECIMAL(4, 1))
    weight = db.Column(db.DECIMAL(4, 1))
    shoesize = db.Column(db.SmallInteger)

    def get(self):
        r = {}
        r = self.to_dict()

        r['specialities'] = []
        specialities = self.specialities
        if specialities is not None:
            for speciality in specialities:
                r['specialities'].append(speciality.to_dict())

        return r

    def __init__(self, height=0, weight=0, shoesize=0):
        self.height = height
        self.weight = weight
        self.shoesize = shoesize

    __mapper_args__ = {
        'extension': MapperExtension(),
    }


@foreign_key('physical')
class Speciality(BaseMixin, db.Model):
    speciality = db.Column(db.String(255))

    def __init__(self, speciality=''):
        self.speciality = speciality

    __mapper_args__ = {
        'extension': MapperExtension(),
    }


class PassportVISA(BaseMixin, db.Model):
    __tablename__ = 'passport_visa'

    passport_type = db.Column(db.String(1))
    visa_type = db.Column(db.String(1))
    visa_valid_date = db.Column(db.Date)

    def get(self, locale):
        r = {}
        r = self.to_dict()

        r['passport_type'] = p_t.get_by_id(self.passport_type, locale)
        r['visa_type'] = c_t.get_by_id(self.visa_type, locale)

        return r

    def __init__(self, passport_type='1', visa_type='2',
                 visa_valid_date=date(1900, 1, 1)):
        self.passport_type = passport_type
        self.visa_type = visa_type
        self.visa_valid_date = visa_valid_date

    __mapper_args__ = {
        'extension': MapperExtension(),
        'polymorphic_identity': 'passport_visa'
    }


@foreign_key_one_to_one('trainee')
class Tpassport_visa(PassportVISA):
    id = db.Column(db.Integer,
                   db.ForeignKey(PassportVISA.id, ondelete='cascade'),
                   primary_key=True)

    entrance_date = db.Column(db.Date)
    exit_date = db.Column(db.Date)
    entrance_flight = db.Column(db.String(8))
    exit_flight = db.Column(db.String(8))

    def __init__(self, entrance_date=date(1900, 1, 1),
                 exit_date=date(1900, 1, 1), entrance_flight='',
                 exit_flight='', *args, **kwargs):
        super(Tpassport_visa, self).__init__(*args, **kwargs)
        self.entrance_date = entrance_date
        self.exit_date = exit_date
        self.entrance_flight = entrance_flight
        self.exit_flight = exit_flight

    __mapper_args__ = {
        'extension': MapperExtension(),
        'polymorphic_identity': 'trainee_passport_visa'
    }


@foreign_key('trainee')
class Relative(PersonMixin, db.Model):
    relation = db.Column(db.String(1))

    def get(self, locale):
        r = {}
        r = self.to_dict()
        r['relation'] = re.get_by_id(self.relation, locale)

        return r

    def __init__(self, relation='0', mobile='', f_name='', l_name=''):
        self.relation = relation
        self.mobile = mobile
        self.f_name = f_name
        self.l_name = l_name

    __mapper_args__ = {
        'extension': MapperExtension(),
    }


class Experience(BaseMixin, db.Model):
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    detail = db.Column(db.String(1024))

    def __init__(self, start_date=date(1900, 1, 1), end_date=date(1900, 1, 1),
                 detail=''):
        self.start_date = start_date
        self.end_date = end_date
        self.detail = detail

    __mapper_args__ = {
        'extension': MapperExtension(),
        'polymorphic_identity': 'experience'
    }


@foreign_key('trainee')
class Training(Experience):
    id = db.Column(db.Integer,
                   db.ForeignKey(Experience.id, ondelete='cascade'),
                   primary_key=True)

    def __init__(self, *args, **kwargs):
        super(Training, self).__init__(*args, **kwargs)

    __mapper_args__ = {
        'extension': MapperExtension(),
        'polymorphic_identity': 'training'
    }


@foreign_key('trainee')
class Working(Experience):
    id = db.Column(db.Integer, db.ForeignKey(Experience.id, ondelete='cascade'),
                   primary_key=True)
    department = db.Column(db.String(255))
    job = db.Column(db.String(255))

    def __init__(self, department='', job='', *args, **kwargs):
        super(Working, self).__init__(*args, **kwargs)
        self.department = department
        self.job = job

    __mapper_args__ = {
        'extension': MapperExtension(),
        'polymorphic_identity': 'working'
    }


@foreign_key('trainee')
@foreign_key('country')
class AbroadStudy(Experience):
    id = db.Column(db.Integer,
                   db.ForeignKey(Experience.id, ondelete='cascade'),
                   primary_key=True)

    def get(self):
        r = {}
        r = self.to_dict()
        r['country'] = self.country.to_dict()

        return r

    def __init__(self, country_id=138, *args, **kwargs):
        super(AbroadStudy, self).__init__(*args, **kwargs)
        self.country_id = country_id

    __mapper_args__ = {
        'extension': MapperExtension(),
        'polymorphic_identity': 'study_abroad'
    }


@foreign_key('trainee')
@foreign_key('city')
class Contact(PersonMixin, db.Model):
    address = db.Column(db.String(128))

    def __init__(self, city_id, address='', mobile='', f_name='', l_name=''):
        self.city_id = city_id
        self.address = address
        self.mobile = mobile
        self.f_name = f_name
        self.l_name = l_name

    def get(self):
        r = {}
        r = self.to_dict()

        r['city'] = self.city.get()

        return r

    __mapper_args__ = {
        'extension': MapperExtension(),
    }

# 这里的trainee.id及tfamily.id都是用的表名。而不是backref
Trainee_Tfamily = db.Table(
    'trainee_tfamily',
    db.Column('trainee_id', db.Integer,
              db.ForeignKey('trainee.id', ondelete='cascade'),
              primary_key=True),
    db.Column('tfamily_id', db.Integer,
              db.ForeignKey('tfamily.id', ondelete='cascade'),
              primary_key=True)
)


@foreign_key_one_to_one('account')
class Tfamily(Foreigner):
    id = db.Column(db.Integer,
                   db.ForeignKey(Foreigner.id, ondelete='cascade'),
                   primary_key=True)

    toTrainee = db.relationship('Trainee', secondary=Trainee_Tfamily,
                                backref=db.backref('tfamily'))

    def _trainee(self, trainee):
        self.trainee = trainee

    def _tfpassport_visa(self, passport_visa):
        self.tfpassport_visa = passport_visa

    def get(self, locale):
        r = {}
        r = self.to_dict()

        trainee = self.trainee
        if trainee is not None:
            r['trainee'] = trainee.to_dict()

        passport_visa = self.tfpassport_visa
        if passport_visa is not None:
            r['PassportVISA'] = passport_visa.to_dict()

        return r

    def __init__(self, *args, **kwargs):
        super(Tfamily, self).__init__(*args, **kwargs)

    __mapper_args__ = {
        'extension': MapperExtension(),
        'polymorphic_identity': 'trainee_family'
    }


@foreign_key_one_to_one('tfamily')
class TFpassport_visa(PassportVISA):
    id = db.Column(db.Integer,
                   db.ForeignKey(PassportVISA.id, ondelete='cascade'),
                   primary_key=True)

    def __init__(self, *args, **kwargs):
        super(TFpassport_visa, self).__init__(*args, **kwargs)

    __mapper_args__ = {
        'extension': MapperExtension(),
        'polymorphic_identity': 'trainee_family_passport_visa'
    }


# 此表是存储来访外国人的
class ExternalForeigner(Foreigner):
    id = db.Column(db.Integer,
                   db.ForeignKey(Foreigner.id, ondelete='cascade'),
                   primary_key=True)

    def __init__(self, country_id, *args, **kwargs):
        super(ExternalForeigner, self).__init__(*args, **kwargs)
        self.country_id = country_id

    __mapper_args__ = {
        'extension': MapperExtension(),
        'polymorphic_identity': 'external_foreigner'
    }


class Acategory(BaseMixin, db.Model):
    #
    # Articlecategory 是 Article 的 parent
    #
    name = db.Column(db.String(255))

    def __init__(self, name=''):
        self.name = name

    __mapper_args__ = {
        'extension': MapperExtension(),
    }


@foreign_key('account')
@foreign_key('acategory')
class Article(BaseMixin, db.Model):
    abstract = db.Column(db.String(140))
    content = db.Column(db.Text)

    def __init__(self, acategory_id, abstract='', content=''):
        self.acategory_id = acategory_id
        self.abstract = abstract
        self.content = content

    __mapper_args__ = {
        'extension': MapperExtension(),
    }
