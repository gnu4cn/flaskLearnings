# -*- coding: utf-8 -*-
class lang(object):
    data = {
        'UsernameNotExistorPasswordNotCorrect': {
            'zh-cn': '用户名不存在或密码不正确, 请重新输入用户名密码。',
            'en-us': 'Username not exist, or password not correct, please input again. '
        },
        'LoginedSuccessful': {
            'zh-cn': '登入成功，前往首页......',
            'en-us': 'Logined successfully, moving to index page... '
        },
        'createUserSuccessfully': {
            'zh-cn': "成功创建用户，前往登入页面......",
            'en-us': "User created successfully, moving to the login page... "
        },
        'ProfileInsertionError': {
            'en-us': 'Error occured when insert the Profile instance into database. ',
            'zh-cn': '在将 Profile 实例存入数据库时出错。',
        },
        'UserInsertionError': {
            'en-us': 'Error occured when insert the User instance into database. ',
            'zh-cn': '在 User 实例存入数据库时出错。',
        },
        'makeUserInstanceError': {
            'zh-cn': '服务器错误：实例化 User 对象出错。',
            'en-us': 'Server error: making User Object instance failed. '
        },
        'makeProfileInstanceFail': {
            'zh-cn': '实例化 Profile 对象出错',
            'en-us': 'Make Profile instance Failed'
        },
        'usernameOrpasswordOrcategoryIsBlank': {
            'zh-cn': '用户名或密码或人员类别为空。',
            'en-us': 'Username or password or person category is blank. '
        },
        'FailedtoGetUserAccountInfo': {
            'zh-cn': '获取用户帐号信息失败。',
            'en-us': 'Failed to get user account infomation. '
        },
        'GetUserAccountInfoSuccessfully': {
            'zh-cn': '成功获取到用户帐号信息。',
            'en-us': 'Get user account infomation successfully. '
        },
        'CredentialExpired': {
            'zh-cn': '用户凭据已过期，请重新登入。',
            'en-us': 'User credential expired, please login again. '
        },
        'IncorrectCredential': {
            'zh-cn': '凭据错误，请重新登入。',
            'en-us': 'Incorrect user credential, please login again. '
        },
        'usernameAlreadyExist': {
            'zh-cn': '用户名已存在。',
            'en-us': 'Username already exist. '
        },
    }

    @classmethod
    def get_item(self, item, lang):
        return self.data[item][lang]
