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
from datetime import datetime, date
from constant import ROLE_USER, MALE, TOKEN_EXPIRE
from appdemo import db
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.orm import with_polymorphic, MapperExtension
from constant import PRSN_CAT as p_c, POSITION as po, DEPARTMENT as de, \
    SERVICE as se, TRNEE_RANK as t_r, RELATION as re, RELIGION as rel, \
    GENDER as ge, MARRIAGE as ma, PPRT_TYPE as p_t, CERT_TYPE as c_t, EDU as edu

### 这是为了last_updated
class MixinExtension(MapperExtension):
    def before_insert(self, mapper, connection, instance):
        instance.created_at = datetime.now()
        instance.last_updated = datetime.now()

    def before_update(self, mapper, connection, instance):
        instance.created_at = instance.created_at
        instance.last_updated = datetime.now()

# 使用db实例中的app属性
app = db.app

dbSession = db.session

def get_u_id_from_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None
    except BadSignature:
        return None

    return data['id']

def fetech_profile_foreigner(uId, category):
    entity = {
        '5': lambda: with_polymorphic(Foreigner, Trainee),
        '6': lambda: with_polymorphic(Foreigner, TraineeFamily),
        '7': lambda: with_polymorphic(Foreigner, ExternalForeigner)
    }[category]()

    return dbSession.query(entity).filter_by(u_id=uId).first().to_dict

def fetech_profile_chinese(uId, category):
    entity = {
        '0': lambda: with_polymorphic(Chinese, Staff),
        '1': lambda: with_polymorphic(Chinese, StaffFamily),
        '2': lambda: with_polymorphic(Chinese, ExternalChinese)
    }[category]()

    return dbSession.query(entity).filter_by(u_id=uId).first().to_dict

def create_profile(firstName, lastName, uId, idNumber, sexality, \
                   passportNumber, category):
    return {
        '0': lambda: Staff(u_id=uId, id_number=idNumber, f_name=firstName, \
                           l_name=lastName),
        '1': lambda: StaffFamily(u_id=uId, id_number=idNumber, f_name=firstName, \
                                 l_name=lastName),
        '2': lambda: ExternalChinese(u_id=uId, id_number=idNumber, \
                                     f_name=firstName, l_name=lastName),
        '5': lambda: Trainee(u_id=uId, gender=sexality, \
                             passport_number=passportNumber, \
                             f_name=firstName, l_name=lastName),
        '6': lambda: TraineeFamily(u_id=uId, gender=sexality, \
                                   passport_number=passportNumber, \
                                   f_name=firstName, l_name=lastName),
        '7': lambda: ExternalForeigner(u_id=uId, gender=sexality, \
                                       passport_number=passportNumber, \
                                       f_name=firstName, l_name=lastName)
    }[category]()

#db = SQLAlchemy()

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
### http://stackoverflow.com/questions/15534147/python-inheritance-in-sqlalchemy
### the mixin must come first!!!
class User(ModelMixin, db.Model):
    '''
    用户表，存储了用户名、一卡通卡号、密码，用户角色。与个人资料相关联。
    '''
    __tablename__ = 'user_table'
    id = db.Column(db.Integer, primary_key=True)

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

    # 同时建立到Chinese及Foreigner的所属关系
    foreigners = db.relationship('Foreigner')
    chinese = db.relationship('Chinese')

    # 到Media的关系
    medias = db.relationship('Media')

    def generate_auth_token(self, expiration=TOKEN_EXPIRE):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @classmethod
    def verify_auth_token(self, token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None

        user = self.query.get(data['id'])

        return user

    ### 为何这里必须用静态方法？
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
    def check_username(self, testUsername):
        r = {}
        r['success'] = True
        if(self.query.filter_by(username=testUsername).first() != None):
            r['exists'] = True
        else:
            r['exists'] = False

        return jsonify(r)

    @classmethod
    def get_by_credential(self, cred, locale):
        r = {}

        token = cred[0:-7]

        try:
            r['user'] = self.verify_auth_token(token).to_dict
            r['user']['category'] = p_c.get_by_id(r['user']['person_type'], locale)
            r['success'] = True
            r['message'] = lang.get_item('GetUserAccountInfoSuccessfully', locale)

        except:
            r['success'] = False
            r['message'] = lang.get_item('FailedtoGetUserAccountInfo', locale)

        return jsonify(r)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    @classmethod
    def create(self, username, password, category, firstName, lastName, \
               idNumber, gender, passportNumber, locale):
        r = {}
        try:
            u = self(username, password, category)

            try:
                dbSession.add(u)
                dbSession.commit()
                uId = u.id

                try:
                    p = create_profile(firstName, lastName, uId, idNumber, \
                                       gender, passportNumber, category)
                    try:
                        dbSession.add(p)
                        dbSession.commit()

                        r['success'] = True
                        r['message'] = lang.get_item('createUserSuccessfully', locale)

                    except:
                        r['success'] = False
                        r['message'] = lang.get_item('ProfileInsertionError', locale)
                        dbSession.delete(u)
                        dbSession.commit()

                except:
                    r['success'] = False
                    r['message'] = lang.get_item('makeProfileInstanceFail', locale)
                    dbSession.delete(u)
                    dbSession.commit()

            except:
                r['success'] = False
                r['message'] = lang.get_item('UserInsertionError', locale)

        except:
            r['success'] = False
            r['message'] = lang.get_item('makeUserInstanceError', locale)

        return jsonify(r)


    __mapper_args__ = {
        'extension': MixinExtension(),
    }

class Media(ModelMixin, db.Model):
    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='cascade'))
    title = db.Column(db.String(64), default='')
    description = db.Column(db.String(140), default='')
    filesize = db.Column(db.Integer, default=0)
    uri = db.Column(db.String(255), nullable=False)

    __mapper_args__ = {
        'extension': MixinExtension(),
        'polymorphic_identity': 'media',
    }

class Image(Media):
    __tablename__ = 'image'

    id = db.Column(db.Integer, db.ForeignKey(Media.id, ondelete='cascade'), \
                   primary_key=True)

    width = db.Column(db.SmallInteger)
    height = db.Column(db.SmallInteger)

    __mapper_args__ = {
        'polymorphic_identity': 'image'
    }

class Audio(Media):
    __tablename__ = 'audio'

    id = db.Column(db.Integer, db.ForeignKey(Media.id, ondelete='cascade'), \
                   primary_key=True)

    duration = db.Column(db.DECIMAL('9,2'))

    __mapper_args__ = {
        'polymorphic_identity': 'audio'
    }

class Video(Media):
    __tablename__ = 'video'

    id = db.Column(db.Integer, db.ForeignKey(Media.id, ondelete='cascade'), \
                   primary_key=True)

    duration = db.Column(db.DECIMAL('9,2'))

    __mapper_args__ = {
        'polymorphic_identity': 'video'
    }

class Province(ModelMixin, db.Model):
    __tablename__ = 'province'
    id = db.Column(db.Integer, primary_key=True)

    pinyin = db.Column(db.String(64))
    hanzi = db.Column(db.String(64))

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

class City(ModelMixin, db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)

    #province
    province_id = db.Column(db.Integer, \
                            db.ForeignKey(Province.id, ondelete='cascade'))
    province = db.relationship('Province')

    pinyin = db.Column(db.String(64))
    hanzi = db.Column(db.String(64))

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

class CustomPort(ModelMixin, db.Model):
    '''
    中国的出入境口岸。
    '''
    __tablename__ = 'customport'
    id = db.Column(db.Integer, primary_key=True)

    en_simp = db.Column(db.String(128))
    en_full = db.Column(db.String(255))
    zh_simp = db.Column(db.String(32))
    alpha_3 = db.Column(db.String(3))
    alpha_4 = db.Column(db.String(4))

    def __init__(self, en_simp, en_full, zh_simp, alpha_3, alpha_4):
        self.en_simp = en_simp
        self.en_full = en_full
        self.zh_simp = zh_simp
        self.alpha_3 = alpha_3
        self.alpha_4 = alpha_4

class Language(ModelMixin, db.Model):
    __tablename__ = 'language'
    id = db.Column(db.Integer, primary_key=True)

    code = db.Column(db.String(3))
    en_name = db.Column(db.String(256))
    zh_name = db.Column(db.String(256))
    native_name = db.Column(db.String(128))

    def __init__(self, code, en_name, zh_name, native_name):
        self.code = code
        self.en_name = en_name
        self.zh_name = zh_name
        self.native_name = native_name

class Country(ModelMixin, db.Model):
    '''
    国家表（国旗和国歌都保存在Media表中）。
    '''
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)

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

    # 建立到Foreigner的one-to-many关系，以便今后从Country查询到foreigners
    foreigners = db.relationship('Foreigner', back_populates='country')

    # 建立一个到Trainingexperience的关系，以便查询到在该国所提供的Training
    training_experiences = db.relationship('TrainingExperience')

    # for the flag of country
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
    def mobile(cls):
        return db.Column(db.String(11), default='')

    @declared_attr
    def f_name(cls):
        return db.Column(db.String(64), default='')

    @declared_attr
    def l_name(cls):
        return db.Column(db.String(80), default='')

ChinesePhoto = db.Table(
    'chinese_photo',
    db.Column('chinese_id', db.Integer, \
              db.ForeignKey('chinese.id', ondelete='cascade'), primary_key=True),
    db.Column('photo_id', db.Integer, db.ForeignKey(Image.id, ondelete='cascade'), \
              primary_key=True),
)

# 这里使用了数据表映射
class Chinese(PersonMixin, db.Model):
    __tablename__ = 'chinese'
    id = db.Column(db.Integer, primary_key=True)

    # 这里很有意思，原来是人拥有帐号，帐号属于人所拥有，就决定了先要建立人
    # 员资料，然后在建立
    # 帐号！！那么在建立人员资料前就应检查是否已有其资料，在之后的建立帐号
    # 中，就要检查是否已有要求建立的用户名的帐号，已有就要求修改密码，若无
    # 就建立新的帐号
    #
    # 然而又可以作为帐号拥有个人资料，则情况就完全不同了，这里就无需建立
    # db.relationship
    #
    # 最后这里还可以有双向关系，互为parent
    #
    # 考虑个人资料部分用到了Mixin，就采取人员拥有帐号的做法，以降低复杂度
    #
    # 但是如果能从User同时建立到Chinese及Foreigner的关系，则问题就可解决了
    # 这样做可以带来后期非常大的便利, 值得为之一试！！
    #
    #
    #这里无需到User的关系
    u_id = db.Column(db.Integer, \
                     db.ForeignKey(User.id, ondelete='cascade'), unique=True)

    id_number = db.Column(db.String(18), default='')

    ChinesePhoto = db.relationship('Image', secondary=ChinesePhoto, \
                                     lazy='dynamic', \
                                     backref=db.backref('chinese', lazy='dynamic'))

    @classmethod
    def get_by_credential(self, locale, cred, category):
        r = {}
        u_id = get_u_id_from_token(cred[0:-7])
        if (u_id is not None):
            try:
                profile = fetech_profile_chinese(u_id, category)

                if (int(category)==0):
                    profile['position_detail'] = po.get_by_id(profile['position'], locale)

                r['success'] = True
                r['profile'] = profile

            except:
                r['success'] = False
                r['message'] = lang.get_item('fetchChineseProfileFailed', locale)
        else:
            r['success'] = False
            r['message'] = lang.get_item('IncorrectCredential', locale)

        return jsonify(r)

    def save_photo():
        pass

    def fetch_photo():
        pass

    __mapper_args__ = {
        'extension': MixinExtension(),
        'polymorphic_identity': 'chinese',
    }

class Staff(Chinese):
    __tablename__ = 'staff'

    id = db.Column(db.Integer, \
                   db.ForeignKey(Chinese.id, ondelete='cascade'), primary_key=True)

    position = db.Column(db.String(2))

    # 这里也很有意思，需要建立Staff和StaffFamily的双向关系，一边后期既可以从
    # Staff查询到其家属，又可以从StaffFamily查询到其所属Staff

    families = db.relationship('StaffFamily', secondary='staff_stafffamily', \
                               lazy='dynamic', \
                               backref=db.backref('staff', lazy='dynamic'))

    __mapper_args__ = {
        'polymorphic_identity': 'staff'
    }

Staff_StaffFamily = db.Table(
    'staff_stafffamily',
    db.Column('staff_id', db.Integer, db.ForeignKey('staff.id', ondelete='cascade'), \
              primary_key=True),
    db.Column('stafffamily_id', db.Integer, \
              db.ForeignKey('staff_family.id', ondelete='cascade'), primary_key=True)
)

##员工家属表
class StaffFamily(Chinese):
    __tablename__ = 'staff_family'

    id = db.Column(db.Integer, \
                   db.ForeignKey(Chinese.id, ondelete='cascade'), primary_key=True)

    # 建立了到Staff的关系
    Staff_StaffFamily = db.relationship('Staff', secondary=Staff_StaffFamily, \
                                        lazy='dynamic', \
                                        backref=db.backref('staff_family', lazy='dynamic'))

    __mapper_args__ = {
        'polymorphic_identity': 'staff_family',
    }

class ExternalChinese(Chinese):
    __tablename__ = 'external_chinese'

    id = db.Column(db.Integer, \
                   db.ForeignKey(Chinese.id, ondelete='cascade'), primary_key=True)

    work_place = db.Column(db.String(255), default='')

    __mapper_args__ = {
        'polymorphic_identity': 'external_chinese',
    }

ForeignerPhoto = db.Table(
    'foreigner_photo',
    db.Column('foreigner_id', db.Integer, \
              db.ForeignKey('foreigner.id', ondelete='cascade'), primary_key=True),
    db.Column('photo_id', db.Integer, \
              db.ForeignKey(Image.id, ondelete='cascade'), primary_key=True),
)

class Foreigner(PersonMixin, db.Model):
    __tablename__ = 'foreigner'
    id = db.Column(db.Integer, primary_key=True)

    # 建立到User的关系，可以不是双向所属关系
    # user = db.relationship('User', back_populates='chinese')
    u_id = db.Column(db.Integer, \
                     db.ForeignKey(User.id, ondelete='cascade'), unique=True)

    # 到国家的所属关系，可查询到国家信息, 是many-to-one
    # 国家到Foreigner的所属关系呢？one-to-many
    #
    # 加入到Country的关系后，在建立帐号是就务必要提供国籍信息了
    #
    country = db.relationship('Country', back_populates='foreigners')
    country_id = db.Column(db.Integer, db.ForeignKey('country.id', ondelete='cascade'))
    gender = db.Column(db.String(1), default=MALE)
    passport_number = db.Column(db.String(12), default='')
    visa_number = db.Column(db.String(10), default='')

    ForeignerPhoto = db.relationship('Image', secondary=ForeignerPhoto, \
                                     lazy='dynamic', \
                                     backref = db.backref('foreigner', lazy='dynamic'))

    @classmethod
    def get_by_credential(self, locale, cred, category):
        r = {}
        u_id = get_u_id_from_token(cred[0:-7])
        if (u_id is not None):
            try:
                profile = fetech_profile_foreigner(u_id, category)
                profile['gender'] = ge.get_by_id(profile['gender'], locale)
                if (int(category)==5):
                    profile['passport_type'] = p_t.get_by_id(profile['passport_type'], locale)
                    profile['visa_type'] = c_t.get_by_id(profile['visa_type'], locale)
                    profile['religion'] = rel.get_by_id(profile['religion'], locale)
                    profile['edu'] = edu.get_by_id(profile['education'], locale)
                    profile['marriage'] = ma.get_by_id(profile['marriage'], locale)
                    profile['rank'] = t_r.get_by_id(profile['rank'], locale)

                if (int(category)==6):
                    profile['passport_type'] = p_t.get_by_id(profile['passport_type'], locale)
                    profile['visa_type'] = c_t.get_by_id(profile['visa_type'], locale)

                r['success'] = True
                r['profile'] = profile

            except:
                r['success'] = False
                r['message'] = lang.get_item('fetchChineseProfileFailed', locale)
        else:
            r['success'] = False
            r['message'] = lang.get_item('IncorrectCredential', locale)

        return jsonify(r)

    def save_photo():
        pass

    def fetch_photo():
        pass

    def save_nationality():
        pass

    def fetch_nationality():
        pass

    def __init__(self, *args, **kwargs):
        super(Foreigner, self).__init__(*args, **kwargs)

    __mapper_args__ = {
        'extension': MixinExtension(),
        'polymorphic_identity': 'foreigner',
    }

class Trainee(Foreigner):
    __tablename__ = 'trainee'

    id = db.Column(db.Integer, \
                   db.ForeignKey(Foreigner.id, ondelete='cascade'), primary_key=True)

    birthday = db.Column(db.Date, default=date(1900, 1, 1))
    student_id = db.Column(db.String(10), default='')
    #中文名字
    xingming = db.Column(db.String(24), default=u'张三')

    career_records = db.relationship("Career")
    social_edu_records = db.relationship('SocialEdu')
    physical_condition_records = db.relationship('PhysicalCondition')
    entrance_exit_records = db.relationship('TraineeEntranceExit')
    relatives = db.relationship('Relative')
    training_experiences = db.relationship('TrainingExperience')
    working_experiences = db.relationship('WorkingExperience')
    study_abroad_experiences = db.relationship('StudyAbroadExperience', \
                                           back_populates='trainee')
    contacts = db.relationship('Contact')

    # 实际上是与Staff的Family类似的
    families = db.relationship('TraineeFamily', secondary='trainee_traineefamily', \
                               lazy='dynamic', \
                               backref=db.backref('staff', lazy='dynamic'))

    def save_entrance_port():
        pass

    def fetch_entrance_port():
        pass

    def save_exit_port():
        pass

    def fetch_exit_port():
        pass

    def save_language():
        pass

    def fetch_language():
        pass

    __mapper_args__ = {
        'polymorphic_identity': 'trainee'
    }

class Career(ModelMixin, db.Model):
    __tablename__ = 'career'
    id = db.Column(db.Integer, primary_key=True)

    trainee_id = db.Column(db.Integer, db.ForeignKey(Trainee.id, ondelete='cascade'))
    department = db.Column(db.String(255))

    #职务
    position = db.Column(db.String(255))

    #任职日期
    position_date = db.Column(db.Date)

    #未来从事工作
    future_position = db.Column(db.String(255))

    # 军衔军种
    rank = db.Column(db.String(4))


    __mapper_args__ = {
        'extension': MixinExtension(),
    }

#学员语言表
TraineeLanguage = db.Table(
    'trainee_language',
    db.Column('social_edu_id', db.Integer, db.ForeignKey('social_edu.id', ondelete='cascade'), \
              primary_key=True),
    db.Column('language_id', db.Integer, db.ForeignKey(Language.id, ondelete='cascade'), \
              primary_key=True),
)

class SocialEdu(ModelMixin, db.Model):
    __tablename__ = 'social_edu'
    id = db.Column(db.Integer, primary_key=True)

    trainee_id = db.Column(db.Integer, db.ForeignKey(Trainee.id))

    #婚姻状况
    marriage = db.Column(db.String(1), default='0')

    #宗教代码
    religion = db.Column(db.String(2), default='00')

    #教育程度代码
    education = db.Column(db.String(1), default='3')

    major = db.Column(db.String(255), default='')

    college = db.Column(db.String(255), default='')

    languages= db.relationship('Language', secondary=TraineeLanguage, \
                               lazy='dynamic', \
                               backref=db.backref('socical_edu', lazy='dynamic'))

    __mapper_args__ = {
        'extension': MixinExtension(),
    }

class PhysicalCondition(ModelMixin, db.Model):
    __tablename__ = 'physical_condition'
    id = db.Column(db.Integer, primary_key=True)

    trainee_id = db.Column(db.Integer, db.ForeignKey(Trainee.id))
    height = db.Column(db.DECIMAL(4,1), default=0)
    weight = db.Column(db.DECIMAL(4,1), default=0)
    shoesize = db.Column(db.SmallInteger, default=0)

    speciality = db.relationship('Speciality')

    __mapper_args__ = {
        'extension': MixinExtension(),
    }

class Speciality(ModelMixin, db.Model):
    __tablename__ = 'trainee_speciality'
    id = db.Column(db.Integer, primary_key=True)

    physical_condition_id = db.Column(db.Integer, \
                                      db.ForeignKey(PhysicalCondition.id, ondelete='cascade'))

    speciality = db.Column(db.String(255), default='')

    __mapper_args__ = {
        'extension': MixinExtension(),
    }

class PassportVISAMixin(ModelMixin):
    #护照类型代码
    @declared_attr
    def passport_type(cls):
        return db.Column(db.String(1), default='1')

    #签证类型代码
    @declared_attr
    def visa_type(cls):
        return db.Column(db.String(1), default='2')

    @declared_attr
    def visa_valid_date(cls):
        return db.Column(db.Date, default=date(1900, 1, 1))

class TraineeEntranceExit(PassportVISAMixin, db.Model):
    __tablename__ = 'trainee_entrance_exit'
    id = db.Column(db.Integer, primary_key=True)

    trainee_id = db.Column(db.Integer, db.ForeignKey(Trainee.id, ondelete='cascade'))
    entrance_date = db.Column(db.Date)
    exit_date = db.Column(db.Date)
    # 入境航班号，可使用公开API查询到到达的各种信息
    entrance_flight = db.Column(db.String(8))

    # 出境航班号，可使用公开API查询到出发的各种信息
    exit_flight = db.Column(db.String(8))

    __mapper_args__ = {
        'extension': MixinExtension(),
    }

#学员亲属表
class Relative(PersonMixin, db.Model):
    __tablename__ = 'relative'
    id = db.Column(db.Integer, primary_key=True)

    # 这里无需建立到Trainee的双向关系，因为无需从这里查询Trainee
    trainee_id = db.Column(db.Integer, \
                           db.ForeignKey(Trainee.id, ondelete='cascade'), primary_key=True)

    #关系类型代码
    relation = db.Column(db.String(1), default='0')

    __mapper_args__ = {
        'extension': MixinExtension(),
    }

class ExperienceMixin(ModelMixin):

    @declared_attr
    def start_date(cls):
        return db.Column(db.Date, default=date(1900, 1, 1))

    @declared_attr
    def end_date(cls):
        return db.Column(db.Date, default=date(1900, 1, 1))

    @declared_attr
    def detail(cls):
        return db.Column(db.String(1024), default='')

class TrainingExperience(ExperienceMixin, db.Model):
    __tablename__ = 'training_experience'
    id = db.Column(db.Integer, primary_key=True)

    trainee_id = db.Column(db.Integer, \
                           db.ForeignKey(Trainee.id, ondelete='cascade'), \
                           primary_key=True)

    __mapper_args__ = {
        'extension': MixinExtension(),
        'polymorphic_identity': 'training_experience',
    }

#学员工作记录
class WorkingExperience(ExperienceMixin, db.Model):
    __tablename__ = 'working_experience'
    id = db.Column(db.Integer, primary_key=True)

    trainee_id = db.Column(db.Integer, \
                           db.ForeignKey(Trainee.id, ondelete='cascade'), \
                           primary_key=True)

    department = db.Column(db.String(255), default='')

    __mapper_args__ = {
        'extension': MixinExtension(),
        'polymorphic_identity': 'working_experience',
    }

#学员其它国家学习记录
class StudyAbroadExperience(ExperienceMixin, db.Model):
    __tablename__ = 'study_abroad_experience'
    id = db.Column(db.Integer, primary_key=True)

    # 是否要建立到Country的关系呢？
    # 建立！
    # 建立后又要能查询到Trainee, 所以又要建立到Trainee的双向关系
    #
    trainee = db.relationship('Trainee', \
                              back_populates='study_abroad_experiences')
    trainee_id = db.Column(db.Integer, \
                           db.ForeignKey('trainee.id', ondelete='cascade'), \
                           primary_key=True)

    country_id = db.Column(db.Integer, \
                           db.ForeignKey(Country.id, ondelete='cascade'), primary_key=True)
    __mapper_args__ = {
        'extension': MixinExtension(),
        'polymorphic_identity': 'study_abroad_experience',
    }

class Contact(PersonMixin, db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)

    trainee_id = db.Column(db.Integer, \
                           db.ForeignKey(Trainee.id, ondelete='cascade'), primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey(City.id, ondelete='cascade'))
    address = db.Column(db.String(128), default='')

    __mapper_args__ = {
        'extension': MixinExtension(),
    }

# 这个数据表很特殊，要建立到两个parent的关系：Trainee、TraineeFamily
Trainee_TraineeFamily = db.Table(
    'trainee_traineefamily',
    db.Column('trainee_id', db.ForeignKey(Trainee.id, ondelete='cascade'), \
              primary_key=True),
    db.Column('traineefamily_id', \
              db.ForeignKey('trainee_family.id', ondelete='cascade'), primary_key=True)
)

class TraineeFamily(Foreigner):
    __tablename__ = 'trainee_family'

    id = db.Column(db.Integer, \
                   db.ForeignKey(Foreigner.id, ondelete='cascade'), primary_key=True)

    trainee = db.relationship('Trainee', secondary=Trainee_TraineeFamily, \
                              lazy='dynamic', \
                              backref=db.backref('trainee_family', lazy='dynamic'))
    # 建立了到TraineeFamilyPassportVISA的所属关系，以后的passport
    # visa数据建立就会
    # 十分方便
    passport_visa = db.relationship('TraineeFamilyPassportVISA')

    def save_trainee():
        pass

    def fetch_trainee():
        pass

    __mapper_args__ = {
        'polymorphic_identity': 'trainee_family'
    }

class TraineeFamilyPassportVISA(PassportVISAMixin, db.Model):
    __tablename__ = 'trainee_family_passport_visa'
    id = db.Column(db.Integer, primary_key=True)

    trainee_family_id = db.Column(db.Integer, db.ForeignKey(TraineeFamily.id, \
                                                            ondelete='cascade'))

class ExternalForeigner(Foreigner):
    __tablename__ = 'external_foreigner'

    id = db.Column(db.Integer, \
                   db.ForeignKey(Foreigner.id, ondelete='cascade'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'external_foreigner'
    }

class ArticleCategory(ModelMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255))

class Article(ModelMixin, db.Model):
    __tablename__ = 'article'

    #
    # 要不要建立到User的反向关系呢？
    # 不需要！
    id = db.Column(db.Integer, primary_key=True)

    u_id = db.Column(db.Integer, db.ForeignKey(User.id, ondelete='cascade'), \
                     primary_key=True)
    category = db.Column(db.Integer, \
                         db.ForeignKey(ArticleCategory.id, ondelete='cascade'))
    abstract = db.Column(db.String(140), default='')
    content = db.Column(db.Text)

    __mapper_args__ = {
        'extension': MixinExtension(),
    }
