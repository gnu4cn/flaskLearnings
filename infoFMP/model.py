# -*- coding: utf-8 -*-
#
# 机关人员可以建立员工数据，使用建立的数据，根据规则可自动生成用户名和默认密码
#
# 学员队可建立学员、学员家属数据，使用建立的数据，根据规则可自动生成用户名和密码
#
# 学员可建立家属数据，使用建立的数据，根据规则自动生成用户名和密码
#
# 各类人员可自主注册，添加自己的数据（在注册页面前，可让其提供一些信息，经由
# 这些信息，查找是否已有其用户名和密码，若尚无，则转至注册页面，否则显示出已
# 生成的用户名密码并转至登入页面）
#
#from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from languages import lang
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, \
    SignatureExpired, BadSignature
from flask import jsonify
from datetime import datetime
from constant import ROLE_USER, MALE, TOKEN_EXPIRE
from constant import PRSN_CAT as p_c
from appdemo import db
from passlib.apps import custom_app_context as pwd_context

# 使用db实例中的app属性
app = db.app

#db = SQLAlchemy()

#def create_military_officer_user(r, username, password, \
    #                                 category, firstName, lastName, idNumber, \
    #                                 passportNumber, locale):
#    try:
#        u = User(username, password, category)
#        p = MilitaryOfficer()




# The final model_to_dict
def model_to_dict(inst, cls):
    convert = dict()
    d = dict()

    if (super(cls, inst) != None) & (hasattr(super(cls, inst), '__table__')):
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

class ModelMixin(object):
    @declared_attr
    def id(cls):
        return db.Column(db.Integer, primary_key=True)

    @declared_attr
    def last_updated(cls):
        return db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)

    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=datetime.now)

    @property
    def to_dict(self):
        return model_to_dict(self, self.__class__)

    @classmethod
    def get_by_id(self, r_id):
        q = self.query.filter_by(id=r_id).first()
        return jsonify(q.to_dict)

    @classmethod
    def get_list(self):
        r = []
        qs = self.query.all()

        for q in qs:
            r.append(q.to_dict)

        return jsonify(r)

##用户表
class User(db.Model, ModelMixin):
    '''
    用户表，存储了用户名、一卡通卡号、密码，用户角色。与个人资料相关联。
    '''
    __tablename__ = 'user_table'

    card_number = db.Column(db.String(64), index=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.SmallInteger, default=ROLE_USER)
    person_type = db.Column(db.String(1))

    # 为导入现有数据、管理员建立个人资料、外军学员建立家属资料而设置的一个
    # 初始化标志。该标志初始值为0表明是系统自动建立的帐号，在对应的用户自主注册后
    # 设置为1，表明该用户已自主注册。
    #
    # 经由注册页面建立的帐号，此字段都设置为True，而系统自动建立的帐号，都设置为
    # False

    is_registered = db.Column(db.Boolean, default=False)

    def generate_auth_token(self, expiration=TOKEN_EXPIRE):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        user = User.query.get(data['id'])

        return user

    @staticmethod
    def check_auth_token_expired(cred, locale):
        r = {}

        token = cred[0:-7]

        r['success'] = True

        s = Serializer(app.config['SECRET_KEY'])
        try:
            s.loads(token)
        except SignatureExpired:
            r['success'] = False
            r['message'] = lang.get_item('CredentialExpired', locale)
        except BadSignature:
            r['success'] = False
            r['message'] = lang.get_item('IncorrectCredential', locale)

        return jsonify(r)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @classmethod
    def login(self, username, password, locale):
        r = {}

        user = self.query.filter_by(username=username).first()

        if not user or not user.verify_password(password):
            r['success'] = False
            r['message'] = lang.get_item('UsernameNotExistorPasswordNotCorrect', locale)

        else:
            r['success'] = True
            r['token'] = user.generate_auth_token()
            r['message'] = lang.get_item('LoginedSuccessful', locale)

        return jsonify(r)

    @classmethod
    def create(self, username, password, category, firstName, lastName, \
               idNumber, passportNumber, locale):
        r = {}
        if username is None or password is None or category is None:
            r['success'] = False
            r['message'] = lang.get_item('usernameOrpasswordOrcategoryIsBlank', locale)

        if self.query.filter_by(username=username).first() is not None:
            r['success'] = False
            r['message'] = lang.get_item('usernameAlreadyExist', locale)

#        {
#            0: lambda:
#
#        }[int(category)]()

#        if int(category) <= 5:
        try:
            u = User('', username, password, category)
            try:
                db.session.add(u)
                db.session.commit()
                r['success'] = True
                r['message'] = lang.get_item('createUserSuccessfully', locale)

            except:
                r['success'] = False
                r['message'] = lang.get_item('databaseInsertionError', locale)
        except:
            r['success'] = False
            r['message'] = lang.get_item('makeInstanceError', locale)

        return r

    @classmethod
    def check_username(self, testUsername):
        r = {}
        r['success'] = True
        if(self.query.filter_by(username=testUsername).first() != None):
            r['exists'] = True
        else:
            r['exists'] = False

        return jsonify(r)

    @staticmethod
    def get_by_credential(cred, locale):
        r = {}

        token = cred[0:-7]

        try:
            r['user'] = User.verify_auth_token(token).to_dict
            r['user']['category'] = p_c.get_by_id(r['user']['person_type'], locale)
            r['success'] = True
            r['message'] = lang.get_item('GetUserAccountInfoSuccessfully', locale)

        except:
            r['success'] = False
            r['message'] = lang.get_item('FailedtoGetUserAccountInfo', locale)

        return jsonify(r)


    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def __init__(self, username, password, person_type, card_number='', \
                 role='0', is_registered=False):
        self.card_number = card_number
        self.username = username
        self.password_hash = pwd_context.encrypt(password)
        self.role = role
        self.person_type = person_type
        self.is_registered = is_registered

class MediaMixin(ModelMixin):
    '''
    媒体数据表，可存储图片、音乐、视频等内容。国家表、人员表都用到此表的数据。
    '''
    @declared_attr
    def u_id(cls):
        return db.Column(db.Integer, db.ForeignKey(User.id))
        user = db.relationship('User', cascade="all, delete-orphan", \
                               single_parent=True)

    @declared_attr
    def title(cls):
        return db.Column(db.Unicode(64))

    @declared_attr
    def description(cls):
        return db.Column(db.Unicode(140))

    @declared_attr
    def filesize(cls):
        return db.Column(db.Integer)

    @declared_attr
    def uri(cls):
        return db.Column(db.String(255), nullable=False)

    def __init__(self, u_id, title, description, filesize, uri, *args, **kwargs):
        self.title = title
        self.description = description
        self.uri = uri
        self.filesize = filesize
        self.u_id = u_id

class Media(db.Model, MediaMixin):

    __tablename__ = 'media'

    type = db.Column(db.String(32))

    def __init__(self, *args, **kwargs):
        super(Media, self).__init__(*args, **kwargs)


    __mapper_args__ = {
        'polymorphic_identity': 'media',
        'polymorphic_on': type
    }

class Image(Media):

    __tablename__ = 'image'

    id = db.Column(db.Integer, db.ForeignKey(Media.id, ondelete='cascade'), \
                   primary_key=True)

    width = db.Column(db.SmallInteger)
    height = db.Column(db.SmallInteger)

    def __init__(self, width, height, *args, **kwargs):
        super(Image, self).__init__(*args, **kwargs)
        self.width = width
        self.height = height

    __mapper_args__ = {
        'polymorphic_identity': 'image'
    }

class Audio(Media):

    __tablename__ = 'audio'

    id = db.Column(db.Integer, db.ForeignKey(Media.id, ondelete='cascade'), \
                   primary_key=True)

    duration = db.Column(db.DECIMAL('9,2'))


    def __init__(self, duration, *args, **kwargs):
        super(Audio, self).__init__(*args, **kwargs)
        self.duration = duration

    __mapper_args__ = {
        'polymorphic_identity': 'audio'
    }

class Video(Media):

    __tablename__ = 'video'

    id = db.Column(db.Integer, db.ForeignKey(Media.id, ondelete='cascade'), \
                   primary_key=True)

    duration = db.Column(db.DECIMAL('9,2'))

    video = db.relationship('Video', cascade='all, delete-orphan', \
                               single_parent=True)

    def __init__(self, duration, *args, **kwargs):
        super(Video, self).__init__(*args, **kwargs)
        self.duration = duration

    __mapper_args__ = {
        'polymorphic_identity': 'video'
    }

class Province(db.Model, ModelMixin):

    __tablename__ = 'province'

    pinyin = db.Column(db.String(64))
    hanzi = db.Column(db.Unicode(64))

    @staticmethod
    def get_its_cities(province_id):
        r = []

        cities = City.query.filter_by(province_id=province_id)

        for city in cities:
            r.append(city.to_dict)

        return r

    def __init__(self, pinyin, hanzi):
        self.pinyin = pinyin
        self.hanzi = hanzi

class City(db.Model, ModelMixin):

    __tablename__ = 'city'

    #province
    province_id = db.Column(db.Integer, \
                            db.ForeignKey(Province.id, ondelete='cascade'))
    province = db.relationship('Province')

    pinyin = db.Column(db.String(64))
    hanzi = db.Column(db.Unicode(64))

    @staticmethod
    def get_by_id(city_id):
        r = {}

        city = City.query.filter_by(id=city_id).first()

        r['city'] = city.to_dict

        province = Province.query.filter_by(id=city.province_id).first()

        r['province'] = province.to_dict

        return r

    def __init__(self, province_id, pinyin, hanzi):
        self.province_id = province_id
        self.pinyin = pinyin
        self.hanzi = hanzi

class CustomPort(db.Model, ModelMixin):
    '''
    中国的出入境口岸。
    '''
    __tablename__ = 'customport'

    en_simp = db.Column(db.String(128))
    en_full = db.Column(db.String(255))
    zh_simp = db.Column(db.Unicode(32))
    alpha_3 = db.Column(db.String(3))
    alpha_4 = db.Column(db.String(4))

    def __init__(self, en_simp, en_full, zh_simp, alpha_3, alpha_4):
        self.en_simp = en_simp
        self.en_full = en_full
        self.zh_simp = zh_simp
        self.alpha_3 = alpha_3
        self.alpha_4 = alpha_4

class Language(db.Model, ModelMixin):

    __tablename__ = 'language'

    code = db.Column(db.String(3))
    en_name = db.Column(db.String(256))
    zh_name = db.Column(db.Unicode(256))
    native_name = db.Column(db.Unicode(128))


    def __init__(self, code, en_name, zh_name, native_name):
        self.code = code
        self.en_name = en_name
        self.zh_name = zh_name
        self.native_name = native_name

class Country(db.Model, ModelMixin):
    '''
    国家表（国旗和国歌都保存在Media表中）。
    '''
    __tablename__ = 'country'

    code = db.Column(db.String(3), unique=True)
    en_simp = db.Column(db.String(256), unique=True)
    en_full = db.Column(db.String(256), unique=True)
    zh_simp = db.Column(db.String(256), unique=True)
    zh_full = db.Column(db.String(256), unique=True)
    alias = db.Column(db.String(256), unique=True)
    alpha_2 = db.Column(db.String(2), unique=True)
    alpha_3 = db.Column(db.String(3), unique=True)
    zoneprefix = db.Column(db.String(5))
    nationalDay = db.Column(db.Date)

    # for the flag of country
    image = db.relationship('Image', cascade="all, delete-orphan", single_parent=True)
    flag_id = db.Column(db.Integer, \
                        db.ForeignKey(Image.id, ondelete='cascade'), unique=True)

    #for the anthem
    audio = db.relationship('Audio', cascade="all, delete-orphan", single_parent=True)
    anthem_id = db.Column(db.Integer, \
                          db.ForeignKey(Audio.id, ondelete='cascade'), unique=True)

    def __repr__(self):
        return '<Country %r>' % self.zh_simp

## Mixins 部分
class PersonMixin(ModelMixin):
    @declared_attr
    def gender(cls):
        return db.Column(db.String(1), default=MALE)

    @declared_attr
    def f_name(cls):
        return db.Column(db.String(64))

    @declared_attr
    def l_name(cls):
        return db.Column(db.String(80))

class ProfileMixin(PersonMixin):
    # relationship to User
    @declared_attr
    def u_id(cls):
        user = db.relationship('User', cascade="all, delete-orphan", single_parent=True)
        return db.Column(db.Integer, \
                         db.ForeignKey(User.id, ondelete='cascade'), unique=True)

class ChineseMixin(ProfileMixin):
    @declared_attr
    def type_(cls):
        return db.Column(db.String(32))

    @declared_attr
    def ID_Number(cls):
        return db.Column(db.String(18))

    def __init__(self, gender, f_name, l_name, u_id, ID_Number, *args, **kwargs):
        super(ChineseMixin, self).__init__(*args, **kwargs)
        self.gender = gender
        self.f_name = f_name
        self.l_name = l_name
        self.u_id = u_id
        self.ID_Number = ID_Number

    __mapper_args__ = {
        'polymorphic_on': type_
    }

# 这里使用了数据表映射
class Chinese(db.Model, ChineseMixin):
    __tablename__ = 'chinese'

    def __init__(*args, **kwargs):
        super(Chinese, self).__init__(*args, **kwargs)

    __mapper_args__ = {
        'polymorphic_identity': 'chinese',
    }

ChinesePhoto = db.Table(
    'chinese_photo',
    db.Column('chinese_id', db.Integer, db.ForeignKey(Chinese.id, ondelete='cascade'), \
              primary_key=True),
    db.Column('photo_id', db.Integer, db.ForeignKey(Image.id, ondelete='cascade'), \
              primary_key=True),
)

class Staff(Chinese):
    __tablename__ = 'staff'

    id = db.Column(db.Integer, \
                   db.ForeignKey(Chinese.id, ondelete='cascade'), primary_key=True)

    position = db.Column(db.String(2))

    mobile = db.Column(db.String(11))

    def __init__(self, position, mobile, *args, **kwargs):
        super(Staff, self).__init__(*args, **kwargs)
        self.position = position
        self.mobile = mobile

    __mapper_args__ = {
        'polymorphic_identity': 'staff'
    }

##员工家属表
class StaffFamily(Chinese):
    __tablename__ = 'staff_family'

    id = db.Column(db.Integer, \
                   db.ForeignKey(Chinese.id, ondelete='cascade'), primary_key=True)

    staff = db.relationship('Staff', foreign_keys='StaffFamily.staff_id')
    staff_id = db.Column(db.Integer, db.ForeignKey(Staff.id, ondelete='cascade'))

    def __init__(self, staff_id, *args, **kwargs):
        super(StaffFamily, self).__init__(*args, **kwargs)
        self.staff_id = staff_id

    __mapper_args__ = {
        'polymorphic_identity': 'staff_family',
    }

class ExternalChinese(Chinese):
    __tablename__ = 'external_chinese'

    id = db.Column(db.Integer, \
                   db.ForeignKey(Chinese.id, ondelete='cascade'), primary_key=True)

    mobile = db.Column(db.String(11))

    work_place = db.Column(db.String(255))

    def __init__(self, mobile, work_place, *args, **kwargs):
        super(ExternalChinese, self).__init__(*args, **kwargs)
        self.mobile = mobile
        self.work_place = work_place

    __mapper_args__ = {
        'polymorphic_identity': 'external_chinese',
    }

class ForeignerMixin(ProfileMixin):
    @declared_attr
    def type_(cls):
        return db.Column(db.String(32))

    @declared_attr
    def visa_number(cls):
        return db.Column(db.String(10))

    @declared_attr
    def passport_number(cls):
        return db.Column(db.String(12))

    def __init__(self, gender, f_name, l_name, u_id, passport_number, \
                 visa_number, *args, **kwargs):
        self.gender = gender
        self.f_name = f_name
        self.l_name = l_name
        self.u_id = u_id
        self.passport_number = passport_number
        self.visa_number = visa_number

    __mapper_args__ = {
        'polymorphic_on': type_
    }

class Foreigner(db.Model, ForeignerMixin):
    __tablename__ = 'foreigner'

    type = db.Column(db.String(32))

    def __init__(self, *args, **kwargs):
        super(Foreigner, self).__init__(*args, **kwargs)

    __mapper_args__ = {
        'polymorphic_identity': 'foreigner',
    }

ForeignerPhoto = db.Table(
    'foreigner_photo',
    db.Column('foreigner_id', db.Integer, \
              db.ForeignKey(Foreigner.id, ondelete='cascade'), primary_key=True),
    db.Column('photo_id', db.Integer, \
              db.ForeignKey(Image.id, ondelete='cascade'), primary_key=True),
)

#外国人国籍
ForeignerCountry = db.Table(
    'foreigner_country',
    db.Column('foreigner_id', db.Integer, db.ForeignKey(Foreigner.id, ondelete='cascade'), \
              primary_key=True),
    db.Column('country_id', db.Integer, db.ForeignKey(Country.id, ondelete='cascade'), \
              primary_key=True),
)

class Trainee(Foreigner):
    __tablename__ = 'trainee'

    id = db.Column(db.Integer, \
                   db.ForeignKey(Foreigner.id, ondelete='cascade'), primary_key=True)

    entrance_date = db.Column(db.Date)
    exit_date = db.Column(db.Date)

    #护照类型代码
    passport_type = db.Column(db.String(1))
    passport_valid_date = db.Column(db.Date)

    #签证类型代码
    visa_type = db.Column(db.String(1))
    visa_valid_date = db.Column(db.Date)

    mobile = db.Column(db.String(11))

    student_id = db.Column(db.String(10))
    height = db.Column(db.DECIMAL(4,1))
    weight = db.Column(db.DECIMAL(4,1))
    shoesize = db.Column(db.SmallInteger)

    #宗教代码
    religion = db.Column(db.String(2))

    #教育程度代码
    education = db.Column(db.String(1))

    #当前工作部门
    department = db.Column(db.Unicode(256))

    #职务
    position = db.Column(db.Unicode(256))

    #任职日期
    position_date = db.Column(db.Date)

    #未来从事工作
    future_position = db.Column(db.Unicode(256))

    #婚姻状况
    marriage = db.Column(db.Boolean)

    #中文名字
    xingming = db.Column(db.Unicode(24))

    # 两位整数表示班级，除十取整为年级，求模为班级
    grade_class = db.Column(db.SmallInteger)

    # 军衔军种
    rank = db.Column(db.String(4))


    def __init__(self, entrance_date, exit_date, passport_type, \
                 passport_valid_date, visa_type, visa_valid_date, mobile, \
                 student_id, height, weight, shoesize, religion, education, \
                 department, position, position_date, future_position, \
                 marriage, xingming, grade_class, rank, *args, **kwargs):
        super(Trainee, self).__init__(*args, **kwargs)
        self.entrance_date = entrance_date
        self.exit_date = exit_date
        self.passport_type = passport_type
        self.passport_valid_date = self.passport_valid_date
        self.visa_type = visa_type
        self.visa_valid_date = visa_valid_date
        self.mobile = mobile
        self.student_id = student_id
        self.height = height
        self.weight = weight
        self.shoesize = shoesize
        self.religion = religion
        self.education = education
        self.department = department
        self.position = position
        self.position_date = position_date
        self.future_position = future_position
        self.marriage = marriage
        self.xingming = xingming
        self.grade_class = grade_class
        self.rank = rank

    __mapper_args__ = {
        'polymorphic_identity': 'trainee'
    }

#学员入境口岸
TraineeEntrancePort = db.Table(
    'trainee_entrance_port',
    db.Column('trainee_id', db.Integer, db.ForeignKey(Trainee.id, ondelete='cascade'), \
              primary_key=True),
    db.Column('custom_port_id', db.Integer, db.ForeignKey(CustomPort.id, ondelete='cascade'), \
              primary_key=True),
)

#学员出境口岸
TraineeExitPort = db.Table(
    'trainee_exit_port',
    db.Column('trainee_id', db.Integer, db.ForeignKey(Trainee.id, ondelete='cascade'), \
              primary_key=True),
    db.Column('custom_port_id', db.Integer, db.ForeignKey(CustomPort.id, ondelete='cascade'), \
              primary_key=True),
)
#学员语言表
TraineeLanguage = db.Table(
    'trainee_language',
    db.Column('trainee_id', db.Integer, db.ForeignKey(Trainee.id, ondelete='cascade'), \
              primary_key=True),
    db.Column('language_id', db.Integer, db.ForeignKey(Language.id, ondelete='cascade'), \
              primary_key=True),
)

#学员亲属表
class RelativeMixin(PersonMixin):
    @declared_attr
    def type_(cls):
        return db.Column(db.String(32))

    @declared_attr
    def trainee_id(cls):
        trainee = db.relationship('Trainee')
        return db.Column(db.Integer, \
                         db.ForeignKey(Trainee.id, ondelete='cascade'), primary_key=True)

    #关系类型代码
    @declared_attr
    def relation(cls):
        return db.Column(db.String(1))

    def __init__(self, gender, f_name, l_name, trainee_id, relation, \
                 *args, **kwargs):
        super(RelativeMixin, self).__init__(*args, **kwargs)
        self.gender = gender
        self.f_name = f_name
        self.l_name = l_name
        self.trainee_id = trainee_id
        self.relation = relation

    __mapper_args__ = {
        'polymorphic_on': type_
    }

class Relative(db.Model, RelativeMixin):
    __tablename__ = 'relative'

    def __init__(self, *args, **kwargs):
        super(Relative, self).__init__(*args, **kwargs)

    __mapper_args__ = {
        'polymorphic_identity': 'relative',
    }

class ExperienceMixin(ModelMixin):
    @declared_attr
    def type_(cls):
        return db.Column(db.String(32))

    @declared_attr
    def trainee_id(cls):
        trainee = db.relationship('Trainee')
        return db.Column(db.Integer, \
                         db.ForeignKey(Trainee.id, ondelete='cascade'), primary_key=True)

    @declared_attr
    def start_date(cls):
        return db.Column(db.Date)

    @declared_attr
    def end_date(cls):
        return db.Column(db.Date)

    @declared_attr
    def detail(cls):
        return db.Column(db.Unicode(1024))

    def __init__(self, trainee_id, start_date, end_date, detail, *args, **kwargs):
        super(ExperienceMixin, self).__init__(*args, **kwargs)
        self.trainee_id = trainee_id
        self.start_date = start_date
        self.end_date = end_date
        self.detail = detail

    __mapper_args__ = {
        'polymorphic_on': type_
    }

class TrainingExperience(db.Model, ExperienceMixin):
    __tablename__ = 'training_experience'

    def __init__(self, *args, **kwargs):
        super(TrainingExperience, self).__init__(*args, **kwargs)

    __mapper_args__ = {
        'polymorphic_identity': 'training_experience',
    }

#学员工作记录
class WorkingExperience(db.Model, ExperienceMixin):
    __tablename__ = 'working_experience'

    department = db.Column(db.String(255))

    def __init__(self, department, *args, **kwargs):
        super(WorkingExperience, self).__init__(*args, **kwargs)
        self.department = department

    __mapper_args__ = {
        'polymorphic_identity': 'working_experience',
    }

#学员其它国家学习记录
class StudyAbroadExperience(db.Model, ExperienceMixin):
    __tablename__ = 'study_abroad_experience'

    country = db.relationship('Country')
    country_id = db.Column(db.Integer, \
                           db.ForeignKey(Country.id, ondelete='cascade'), primary_key=True)

    def __init__(self, country_id, *args, **kwargs):
        super(StudyAbroadExperience, self).__init__(*args, **kwargs)
        self.country_id = country_id

    __mapper_args__ = {
        'polymorphic_identity': 'study_abroad_experience',
    }

class ContactMixin(PersonMixin):
    @declared_attr
    def type_(cls):
        return db.Column(db.String(32))

    @declared_attr
    def trainee_id(cls):
        trainee = db.relationship('Trainee')
        return db.Column(db.Integer, \
                         db.ForeignKey(Trainee.id, ondelete='cascade'), primary_key=True)

    @declared_attr
    def city_id(cls):
        city = db.relationship('City')
        return db.Column(db.Integer, db.ForeignKey(City.id, ondelete='cascade'))

    @declared_attr
    def mobile(cls):
        return db.Column(db.String(11))

    @declared_attr
    def address(cls):
        return db.Column(db.Unicode(128))

    def __init__(self, trainee_id, city_id, gender, f_name, l_name, mobile, \
                 address, *args, **kwargs):
        super(ContactMixin, self).__init__(*args, **kwargs)
        self.trainee_id = trainee_id
        self.gender = gender
        self.f_name = f_name
        self.l_name = l_name
        self.mobile = mobile
        self.city_id = city_id
        self.address = address

    __mapper_args__ = {
        'polymorphic_on': type_
    }

#学员在中国的联系人
class Contact(db.Model, ContactMixin):
    __tablename__ = 'contact'

    def __init__(self, *args, **kwargs):
        super(Contact, self).__init__(*args, **kwargs)

    __mapper_args__ = {
        'polymorphic_identity': 'contact',
    }


class TraineeFamily(Foreigner):
    __tablename__ = 'trainee_family'

    id = db.Column(db.Integer, \
                   db.ForeignKey(Foreigner.id, ondelete='cascade'), primary_key=True)

    entrance_date = db.Column(db.Date)
    exit_date = db.Column(db.Date)

    #护照类型代码
    passport_type = db.Column(db.String(1))
    passport_valid_date = db.Column(db.Date)

    #签证类型代码
    visa_type = db.Column(db.String(1))
    visa_valid_date = db.Column(db.Date)

    trainee = db.relationship('Trainee', foreign_keys='TraineeFamily.trainee_id')
    trainee_id = db.Column(db.Integer, db.ForeignKey(Trainee.id, ondelete='cascade'))

    def __init__(self, entrance_date, exit_date, passport_type, \
                 passport_valid_date, visa_type, visa_valid_date, *args, **kwargs):
        super(Trainee, self).__init__(*args, **kwargs)
        self.entrance_date = entrance_date
        self.exit_date = exit_date
        self.passport_type = passport_type
        self.passport_valid_date = self.passport_valid_date
        self.visa_type = visa_type
        self.visa_valid_date = visa_valid_date

    __mapper_args__ = {
        'polymorphic_identity': 'trainee_family'
    }

class ExternalForeigner(Foreigner):
    __tablename__ = 'external_foreigner'

    id = db.Column(db.Integer, \
                   db.ForeignKey(Foreigner.id, ondelete='cascade'), primary_key=True)

    def __init__(self, *args, **kwargs):
        super(ExternalForeigner, self).__init__(*args, **kwargs)

    __mapper_args__ = {
        'polymorphic_identity': 'external_foreigner'
    }
class ArticleMixin(ModelMixin):
    @declared_attr
    def type_(cls):
        return db.Column(db.String(32))

    @declared_attr
    def u_id(cls):
        user = db.relationship('User')
        return db.Column(db.Integer, \
                         db.ForeignKey(User.id, ondelete='cascade'), primary_key=True)

    @declared_attr
    def abstract(cls):
        return db.Column(db.Unicode(140))

    @declared_attr
    def content(cls):
        return db.Column(db.Text)

    @declared_attr
    def category(cls):
        return db.Column(db.String(1))

    def __init__(self, u_id, abstract, content, category, *args, **kwargs):
        super(ArticleMixin, self).__init__(*args, **kwargs)
        self.u_id = u_id
        self.abstract = abstract
        self.content = content
        self.category = category

    __mapper_args__ = {
        'polymorphic_on': type_
    }

class Article(db.Model, ArticleMixin):
    __tablename__ = 'article'

    def __init__(self, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)

    __mapper_args__ = {
        'polymorphic_identity': 'article',
    }
