# -*-coding: utf-8 -*-
from flask import Flask, jsonify
import types

from flask_restful import Api, Resource, reqparse
from model import db, City, Province, Language, Country, Chinese, Foreigner
from model import Account as User
from constant import PRSN_CAT as p_c, POSITION as po, DEPARTMENT as de, \
    SERVICE as se, TRNEE_RANK as t_r, RELATION as re, RELIGION as rel, \
    GENDER as ge, MARRIAGE as ma, PPRT_TYPE as p_t, CERT_TYPE as c_t, \
    EDU as edu
# ----------使用 HTTPBasicAuth-----------------
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
# ---------------------------------------------

app = Flask(__name__)
app.config.from_object('config.Config')

api = Api(app)

# ------实现装饰器@api.route的有用代码小片段--------
#
def api_route(self, *args, **kwargs):
    def wrapper(cls):
        self.add_resource(cls, *args, **kwargs)
        return cls
    return wrapper

api.route = types.MethodType(api_route, api)
# --------------------------------------------------

db.init_app(app)

# -------------- 使用 HTTPBasicAuth ----------------------------
@auth.verify_password
def verify_token(username_or_token, password=''):
    user = User.verify_auth_token(username_or_token)

    if not user:
        user = User.query.filter_by(username=username_or_token).first()

        if not user or not user.verify_password(password):
            return False

        else:
            return True
    else:
        return True

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
        parser.add_argument('firstName', required=True, location='json')
        parser.add_argument('lastName', required=True, location='json')
        parser.add_argument('idNumber', type=str, location='json', default='')
        parser.add_argument('passportNumber', type=str, location='json',
                            default='')
        parser.add_argument('gender', type=str, location='json', default='1')
        parser.add_argument('countryId', type=int, location='json')

        args = parser.parse_args()

        return User.create(args['username'], args['password'],
                           args['category'], args['firstName'],
                           args['lastName'], args['idNumber'], args['gender'],
                           args['countryId'], args['passportNumber'],
                           args['locale'])


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


@api.route('/api/profile/exists')
class ProfileExists(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('category', type=str, location='json',
                            required=True)
        parser.add_argument('idNumber', type=str, location='json', default='')
        parser.add_argument('passportNumber', type=str, location='json',
                            default='')

        args = parser.parse_args()

        return User.profile_existed(category=args['category'],
                                    idNumber=args['idNumber'],
                                    passportNumber=args['passportNumber'])


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
    #method_decorators = [auth.login_required]
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

@api.route('/api/country/<int:country_id>')
class GetCountry(Resource):
    def get(self, country_id):
        return Country.get_by_id(country_id)

@api.route('/api/countries')
class Countries(Resource):
    def get(self):
        return Country.get_list()

if __name__ == 'main':
    app.run()
