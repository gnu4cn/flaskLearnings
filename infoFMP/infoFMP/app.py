# -*-coding: utf-8 -*-
from flask import Flask, jsonify
import types
import os

from flask_restful import Api, Resource, reqparse
from model import db, City, Province, Language, Country
from model import Account as User
from model import Staff, Sfamily, Trainee, Tfamily, Image
from constant import PRSN_CAT as p_c, POSITION as po, DEPARTMENT as de, \
    SERVICE as se, TRNEE_RANK as t_r, RELATION as re, RELIGION as rel, \
    GENDER as ge, MARRIAGE as ma, PPRT_TYPE as p_t, CERT_TYPE as c_t, \
    EDU as edu
from sqlalchemy import or_, and_
from werkzeug.datastructures import FileStorage
from PIL import Image as IMG
from cStringIO import StringIO
import hashlib
# ----------使用 HTTPBasicAuth-----------------
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
# ---------------------------------------------

STAFF_CAT = '0'
SFAMILY_CAT = '1'
TRAINEE_CAT = '5'
TFAMILY_CAT = '6'
ALLOWED_FORMATS_IMG = set(['jpeg', 'png', 'gif', 'bmp'])

THUMBNAIL_SIZE = 120, 120

app = Flask(__name__)
app.config.from_object('config.Config')

api = Api(app)


# ------实现装饰器@api.route的有用代码小片段--------
def api_route(self, *args, **kwargs):
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls
    return wrapper

api.route = types.MethodType(api_route, api)
# --------------------------------------------------

db.init_app(app)
dbSession = db.session


# -------------- 使用 HTTPBasicAuth ----------------------------
@auth.verify_password
def verify_token(username_or_token, password):
    user = User.verify_auth_token(username_or_token)

    if user is None:
        user = User.query.filter_by(username=username_or_token).first()

        if user is None or not user.verify_password(password):
            return False

        else:
            return True
    else:
        return True


def save_uploaded_image(f, user_id):
    # 这里专注于上传文件的保存了
    content = StringIO(f.read())

    try:
        im = IMG.open(content)

        if im.format.lower() not in ALLOWED_FORMATS_IMG:
            raise IOError()

        else:
            user = User.query.get(user_id)
            # 这里先查看是否已有此图
            try:
                hash_sha1 = hashlib.sha1(content.getvalue()).hexdigest()

                ex_im = Image.query.filter_by(hash_value=hash_sha1).first()

                if ex_im is not None:
                    raise IOError()

                else:
                    # 保存原图片文件
                    _origin = os.path.join(
                        app.config['UPLOAD_FOLDER_IMG'],
                        hash_sha1+'.png')

                    ratio = float(im.size[0])/float(im.size[1])
                    origin = im.resize((1024, int(1024/ratio)), IMG.ANTIALIAS)

                    origin.save(_origin, 'PNG', optimized=True)

                    # 存入数据库
                    width, height = im.size
                    filesize = os.path.getsize(_origin)

                    original_instance = Image(original=True, width=width,
                                              height=height,
                                              hash_value=hash_sha1,
                                              filesize=filesize, uri=_origin)

                    dbSession.add(original_instance)
                    dbSession.commit()

                    user._images(original_instance)

                    # 保存缩略图
                    im.thumbnail(THUMBNAIL_SIZE, IMG.ANTIALIAS)

                    tmp_output = StringIO()
                    im.save(tmp_output, 'PNG')

                    hash_sha1 = hashlib.sha1(tmp_output.getvalue()).hexdigest()

                    _thumbnail = os.path.join(app.config['UPLOAD_FOLDER_IMG'],
                                              hash_sha1+'.png')

                    im.save(_thumbnail, 'PNG')

                    # 存入数据库
                    width, height = im.size
                    filesize = os.path.getsize(_thumbnail)

                    thumbnail_instance = Image(width=width, height=height,
                                               hash_value=hash_sha1,
                                               filesize=filesize,
                                               uri=_thumbnail)

                    dbSession.add(thumbnail_instance)
                    dbSession.commit()

                    user._images(thumbnail_instance)
                    original_instance._sized_versions(thumbnail_instance)

                    return True

            except IOError:
                notAppended = True

                for image in user.images:

                    if image.hash_value == hash_sha1:
                        notAppended = False
                        break

                if notAppended:
                    user._images(ex_im)

                return True

    except IOError:
        return False


@api.route('/api/image/by_thumbnail_id/<int:thumbnailId>')
class ServeImagebyThumbnailId(Resource):
    @auth.login_required
    def get(self, thumbnailId):
        return jsonify(Image.query.get(thumbnailId).origin.to_dict())


@api.route('/api/profile/photo')
class ProfilePhoto(Resource):
    @auth.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, location='json',
                            required=True)
        parser.add_argument('thumbnail_id', type=int, location='json',
                            required=True)
        args = parser.parse_args()

        r = {}
        r['success'] = True
        r['set'] = False

        user = User.query.get(args['user_id'])
        photo = Image.query.get(args['thumbnail_id']).origin

        try:
            {
                STAFF_CAT: lambda: user.staff._photo(photo),
                SFAMILY_CAT: lambda: user.sfamily._photo(photo),
                TRAINEE_CAT: lambda: user.trainee._photo(photo),
                TFAMILY_CAT: lambda: user.tfamily._photo(photo)
            }[user.person_type]()

            r['set'] = True

        except:
            r['set'] = False

        return jsonify(r)


@api.route('/api/image/thumbnails')
class Thumbnails(Resource):
    @auth.login_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, location='json',
                            required=True)
        args = parser.parse_args()
        r = {}
        r['success'] = True
        r['months'] = []

        user = User.query.get(args['user_id'])

        thumbnails = user.images.filter(
            and_(
                or_(Image.width == 120, Image.height == 120),
                Image.original == False)
        ).order_by(Image.last_updated.desc())

        month = 0
        tmp = {}
        tmp['monthly_thumbnails'] = []

        for thumbnail in thumbnails:
            if month != thumbnail.last_updated.month:
                tmp = {}
                tmp['monthly_thumbnails'] = []

                month = thumbnail.last_updated.month
                tmp['year'] = thumbnail.last_updated.year
                tmp['month'] = month
                tmp['monthly_thumbnails'].append(thumbnail.to_dict())
            else:
                tmp['monthly_thumbnails'].append(thumbnail.to_dict())

            if thumbnail == thumbnails[-1]:
                r['months'].append(tmp)

        return jsonify(r)


@api.route('/api/upload/image/<string:user_id>')
class ImageUpload(Resource):
    @auth.login_required
    def post(self, user_id):
        parser = reqparse.RequestParser()
        # From file uploads
        parser.add_argument('file', type=FileStorage, location='files')

        args = parser.parse_args()

        r = {}
        r['success'] = True
        r['uploaded'] = False

        if args['file'] is not None:
            r['uploaded'] = save_uploaded_image(args['file'], user_id)

        return jsonify(r)


# ---------------------User APIs--------------------
@api.route('/api/users')
class UsersApi(Resource):
    @auth.login_required
    def get(self):
        return User.get_list()

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True,
                            location='json')
        parser.add_argument('password', type=str, required=True,
                            location='json')
        parser.add_argument('locale', type=str, location='json',
                            default='zh-cn')
        parser.add_argument('category', type=str, location='json',
                            required=True)
        # 这里在JSON中出现汉字的做法
        parser.add_argument('firstName', required=True, location='json')
        parser.add_argument('lastName', required=True, location='json')
        parser.add_argument('idNumber', type=str, location='json', default='')
        parser.add_argument('passportNumber', type=str, location='json',
                            default='')
        parser.add_argument('gender', type=str, location='json', default='1')
        parser.add_argument('country_id', type=int, location='json', default=0)
        parser.add_argument('profile_id', type=int, location='json', default=0)

        args = parser.parse_args()

        return User.create(args['username'], args['password'],
                           args['profile_id'], args['category'],
                           args['firstName'], args['lastName'],
                           args['idNumber'], args['gender'],
                           args['country_id'],
                           args['passportNumber'], args['locale'])


@api.route('/api/user/password')
class UpdatePassword(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cred', type=str, required=True,
                            location='json')
        parser.add_argument('oldPassword', type=str, required=True,
                            location='json')
        parser.add_argument('newPassword', type=str, required=True,
                            location='json')
        parser.add_argument('locale', type=str, location='json',
                            default='en-us')

        args = parser.parse_args()

        return User.update_password(args['cred'], args['oldPassword'],
                                    args['newPassword'], args['locale'])


@api.route('/api/user/profile/passportvisa')
class PassportVISAOperation(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cred', type=str, required=True, location='json')
        parser.add_argument('locale', type=str, location='json',
                            default='en-us')
        parser.add_argument('passport_type', type=str, location='json',
                            required=True)
        parser.add_argument('visa_type', type=str, location='json',
                            required=True)
        # 含有Unicode字符‘无’
        parser.add_argument('VISANumber', location='json',
                            required=True)
        parser.add_argument('visa_valid_date', type=str, location='json',
                            required=True)
        parser.add_argument('arrive_date', type=str, location='json',
                            default='')
        parser.add_argument('return_date', type=str, location='json',
                            default='')
        parser.add_argument('arrive_flight', type=str, location='json',
                            default='')
        parser.add_argument('return_flight', type=str, location='json',
                            default='')

        args = parser.parse_args()

        return User.passport_visa_operation(args['cred'],
                                            args['passport_type'],
                                            args['visa_type'],
                                            args['VISANumber'],
                                            args['visa_valid_date'],
                                            args['arrive_date'],
                                            args['return_date'],
                                            args['arrive_flight'],
                                            args['return_flight'],
                                            args['locale'])


@api.route('/api/user/profile/basic')
class UpdateBasicProfile(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('cred', type=str, required=True, location='json')
        parser.add_argument('firstName', location='json', required=True)
        parser.add_argument('lastName', location='json',  required=True)
        parser.add_argument('mobile', type=str, location='json', required=True)
        parser.add_argument('idNumber', type=str, location='json', default='')
        parser.add_argument('position', type=str, location='json', default='')
        parser.add_argument('passportNumber', type=str, location='json',
                            default='')
        parser.add_argument('gender', type=str, location='json', default='')
        parser.add_argument('country_id', type=int, location='json',
                            default=138)
        parser.add_argument('xingming', location='json', default='')
        parser.add_argument('birthday', type=str, location='json', default='')
        parser.add_argument('home_number', type=str, location='json',
                            default='')
        # 地址可能有Unicode字符
        parser.add_argument('home_address', location='json', default='')
        parser.add_argument('category', type=str, location='json',
                            required=True)
        parser.add_argument('locale', type=str, location='json',
                            default='en-us')
        args = parser.parse_args()

        return User.update_basic_profile(args['cred'], args['firstName'],
                                         args['lastName'], args['mobile'],
                                         args['idNumber'], args['position'],
                                         args['passportNumber'],
                                         args['gender'], args['country_id'],
                                         args['xingming'], args['birthday'],
                                         args['home_number'],
                                         args['home_address'],
                                         args['category'], args['locale'])


@api.route('/api/profile/exists')
class ProfileExists(Resource):
    # method_decorators = [auth.login_required]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('category', type=str, location='json',
                            required=True)
        parser.add_argument('idNumber', type=str, location='json', default='')
        parser.add_argument('passportNumber', type=str, location='json',
                            default='')
        parser.add_argument('cred', type=str, location='json', default='')

        args = parser.parse_args()

        return User.profile_existed(category=args['category'],
                                    toSomeone_cred=args['cred'],
                                    idNumber=args['idNumber'],
                                    passportNumber=args['passportNumber'])


@api.route('/api/family/append')
class FamilyAppend(Resource):
    method_decorators = [auth.login_required]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('firstName', required=True, location='json')
        parser.add_argument('lastName', required=True, location='json')
        parser.add_argument('own_category', required=True, type=str,
                            location='json')
        parser.add_argument('idNumber', type=str, location='json', default='')
        parser.add_argument('passportNumber', type=str, location='json',
                            default='')
        parser.add_argument('family_id', type=int, location='json')
        parser.add_argument('own_id', type=int, location='json', required=True)
        parser.add_argument('mobile', type=str, location='json', required=True)
        parser.add_argument('country_id', type=int, location='json')
        parser.add_argument('gender', type=str, location='json')

        args = parser.parse_args()

        r = {}
        r['success'] = True
        r['appended'] = False

        toSomeone = {
            STAFF_CAT: lambda: Staff.query.get(args['own_id']),
            TRAINEE_CAT: lambda: Trainee.query.get(args['own_id'])
        }[args['own_category']]()

        if args['family_id'] is not None:
            try:
                family = {
                    STAFF_CAT: lambda: Sfamily.query.get(args['family_id']),
                    TRAINEE_CAT: lambda: Tfamily.query.get(args['family_id'])
                }[args['own_category']]()

                # 全部更新
                {
                    STAFF_CAT: lambda: family.update(
                        firstName=args['firstName'],
                        lastName=args['lastName'], idNumber=args['idNumber'],
                        mobile=args['mobile']),
                    TRAINEE_CAT: lambda: family.update(
                        firstName=args['firstName'],
                        lastName=args['lastName'],
                        passportNumber=args['passportNumber'],
                        mobile=args['mobile'], gender=args['gender'],
                        country_id=args['country_id'])
                }[args['own_category']]()

                toSomeone._families(family)

                r['appended'] = True

            except:
                r['appended'] = False

        else:
            try:
                {
                    STAFF_CAT: lambda: toSomeone._families(
                        Sfamily(id_number=args['idNumber'],
                                f_name=args['firstName'],
                                l_name=args['lastName'],
                                mobile=args['mobile'])),
                    TRAINEE_CAT: lambda: toSomeone._families(
                        Tfamily(country_id=args['country_id'],
                                gender=args['gender'],
                                passport_number=args['passportNumber'],
                                f_name=args['firstName'],
                                l_name=args['lastName'],
                                mobile=args['mobile']))
                }[args['own_category']]()

                r['appended'] = True

            except:
                r['appended'] = False

        return jsonify(r)


@api.route('/api/user/<string:locale>/<string:cred>')
class GetUserByCredential(Resource):
    def get(self, locale, cred):
        return User.get_by_credential(cred, locale)


@api.route('/api/user/checkcredentialvalid/<string:locale>/<string:cred>')
class CheckUserCredentialExpired(Resource):
    def get(self, locale, cred):
        return User.check_auth_token_expired(cred, locale)


@api.route('/api/user/exist/<string:r_username>')
class CheckUsername(Resource):
    def get(self, r_username):
        return User.check_username(r_username)


@api.route('/api/user/login')
class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True,
                            location='json')
        parser.add_argument('password', type=str, location='json',
                            required=True)
        parser.add_argument('locale', type=str, location='json',
                            default='zh-cn')
        args = parser.parse_args()

        return User.login(args['username'], args['password'], args['locale'])


# ------------------------------------------------------
@api.route('/api/cert_type/<string:locale>/<string:c_id>')
class CERT_type(Resource):
    def get(self, c_id, locale):
        return jsonify(c_t.get_by_id(c_id, locale))


@api.route('/api/cert_types/<string:locale>')
class CertTypes(Resource):
    def get(self, locale):
        return jsonify(c_t.get_list(locale))


@api.route('/api/edu/<string:locale>/<string:e_id>')
class EDU(Resource):
    def get(self, e_id, locale):
        return jsonify(edu.get_by_id(e_id, locale))


@api.route('/api/edus/<string:locale>')
class EDUs(Resource):
    method_decorators = [auth.login_required]

    def get(self, locale):
        return jsonify(edu.get_list(locale))


@api.route('/api/pp_type/<string:locale>/<string:pp_id>')
class PPRT_Type(Resource):
    def get(self, pp_id, locale):
        return jsonify(p_t.get_by_id(pp_id, locale))


@api.route('/api/pp_types/<string:locale>')
class PPRT_Types(Resource):
    def get(self, locale):
        return jsonify(p_t.get_list(locale))


@api.route('/api/gender/<string:locale>/<string:g_id>')
class Gender(Resource):
    def get(self, g_id, locale):
        return jsonify(ge.get_by_id(g_id, locale))


@api.route('/api/genders/<string:locale>')
class Genders(Resource):
    def get(self, locale):
        return jsonify(ge.get_list(locale))


@api.route('/api/marriage/<string:locale>/<string:m_id>')
class Marriage(Resource):
    def get(self, m_id, locale):
        return jsonify(ma.get_by_id(m_id, locale))


@api.route('/api/marriages/<string:locale>')
class Marriages(Resource):
    def get(self, locale):
        return jsonify(ma.get_list(locale))


@api.route('/api/religion/<string:locale>/<string:r_id>')
class Religion(Resource):
    def get(self, r_id, locale):
        return jsonify(rel.get_by_id(r_id, locale))


@api.route('/api/religions/<string:locale>')
class Religions(Resource):
    def get(self, locale):
        return jsonify(rel.get_list(locale))


@api.route('/api/relation/<string:locale>/<string:r_id>')
class Relation(Resource):
    def get(self, r_id, locale):
        return jsonify(re.get_by_id(r_id, locale))


@api.route('/api/relations/<string:locale>')
class Relations(Resource):
    def get(self, locale):
        return jsonify(re.get_list(locale))


@api.route('/api/trnee_rank/<string:locale>/<string:t_r_id>')
class TRNEE_RANK(Resource):
    def get(self, t_r_id, locale):
        return jsonify(t_r.get_by_id(t_r_id, locale))


@api.route('/api/services/<string:locale>')
class Services(Resource):
    def get(self, locale):
        return jsonify(se.get_list(locale))


@api.route('/api/service/<string:s_id>/<string:locale>/ranks')
class ServiceRank(Resource):
    def get(self, s_id, locale):
        return jsonify(se.get_sub_list(s_id, locale))


@api.route('/api/service/<string:locale>/<string:s_id>')
class Service(Resource):
    def get(self, s_id, locale):
        return jsonify(se.get_by_id(s_id, locale))


@api.route('/api/pcategory/<string:locale>/<string:p_c_id>')
class PersonCategory(Resource):
    def get(self, p_c_id, locale):
        return jsonify(p_c.get_by_id(p_c_id, locale))


@api.route('/api/pcategories/<string:locale>')
class PersonCategories(Resource):
    def get(self, locale):
        return jsonify(p_c.get_list(locale))


@api.route('/api/department/<string:locale>/<string:d_id>')
class Department(Resource):
    def get(self, d_id, locale):
        return jsonify(de.get_by_id(d_id, locale))


@api.route('/api/departments/<string:locale>')
class Departments(Resource):
    def get(self, locale):
        return jsonify(de.get_list(locale))


@api.route('/api/department/<string:d_id>/<string:locale>/positions')
class DepartmentPositions(Resource):
    def get(self, d_id, locale):
        return jsonify(de.get_sub_list(d_id, locale))


# 职位
@api.route('/api/position/<string:locale>/<string:p_id>')
class Position(Resource):
    def get(self, p_id, locale):
        return jsonify(po.get_by_id(p_id, locale))


@api.route('/api/city/<int:city_id>')
class GetCity(Resource):
    def get(self, city_id):
        return City.get_by_id(city_id)


@api.route('/api/province/<int:province_id>/cities')
class ProvinceCities(Resource):
    def get(self, province_id):
        return Province.get_its_cities(province_id)


@api.route('/api/province/<int:province_id>')
class GetProvince(Resource):
    def get(self, province_id):
        return Province.get_by_id(province_id)


@api.route('/api/provinces')
class Provinces(Resource):
    def get(self):
        return Province.get_list()


@api.route('/api/language/<int:language_id>')
class GetLanguage(Resource):
    def get(self, language_id):
        return Language.get_by_id(language_id)


@api.route('/api/languages')
class Languages(Resource):
    def get(self):
        return Language.get_list()


@api.route('/api/countries')
class Countries(Resource):
    def get(self):
        return Country.get_list()

if __name__ == 'main':
    app.run()
