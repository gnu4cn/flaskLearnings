# -*- coding: utf-8 -*-
class lang(object):
    data = {
        'UsernameNotExistorPasswordNotCorrect': {
            'zh-cn': '用户名不存在或密码不正确, 请重新输入用户名密码。',
            'en': 'Username not exist, or password not correct, please input again. '
        },
        'LoginedSuccessful': {
            'zh-cn': '登入成功，前往首页......',
            'en': 'Logined successfully, moving to index page... '
        },
        'createUserSuccessfully': {
            'zh-cn': "成功创建用户，前往登入页面......",
            'en': "User created successfully, moving to the login page... "
        },
        'databaseInsertionError': {
            'en': 'Error occured when insert the instance into database. ',
            'zh-cn': '在存入数据库时出错。',
        },
        'makeInstanceError': {
            'zh-cn': '服务器错误：实例化对象出错。',
            'en': 'Server error: making Object instance failed. '
        },
        'usernameOrpasswordOrcategoryIsBlank': {
            'zh-cn': '用户名或密码或人员类别为空。',
            'en': 'Username or password or person category is blank. '
        },
        'FailedtoGetUserAccountInfo': {
            'zh-cn': '获取用户帐号信息失败。',
            'en': 'Failed to get user account infomation. '
        },
        'GetUserAccountInfoSuccessfully': {
            'zh-cn': '成功获取到用户帐号信息。',
            'en': 'Get user account infomation successfully. '
        },
        'CredentialExpired': {
            'zh-cn': '用户凭据已过期，请重新登入。',
            'en': 'User credential expired, please login again. '
        },
        'IncorrectCredential': {
            'zh-cn': '凭据错误，请重新登入。',
            'en': 'Incorrect user credential, please login again. '
        },
        'usernameAlreadyExist': {
            'zh-cn': '用户名已存在。',
            'en': 'Username already exist. '
        },
    }

    @classmethod
    def get_item(self, item, lang):
        return self.data[item][lang]
